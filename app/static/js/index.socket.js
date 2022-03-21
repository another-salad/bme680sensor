// Element colours
function setTempColor(value)
{   
    let bgcolor;
    if (value < 18) {
        bgcolor = "#87CEEB";
    }
    else if (value > 18 && value < 24) {
        bgcolor = "#198754";
    }
    else
    {
        bgcolor = "#CB4335";
    }
    document.getElementById("tempDataCol").style.backgroundColor = bgcolor;
}

let airQualityValues = [];
function setAirValue(airValue)
{
    airQualityValues.push(airValue);
    minVal = Math.min(...airQualityValues);
    maxVal = Math.max(...airQualityValues);
    if (maxVal - minVal <= 500) {
        document.getElementById("airQualCol").style.backgroundColor = "#5dade2";
    }
    else
    {
        document.getElementById("airQualCol").style.backgroundColor = "#f39c12";
    }
    document.getElementById("airQualityData").textContent = "".concat("Lowest: ", minVal, ". Highest: ", maxVal, ". Current: ", airValue);
}

// Simple socket behaviours for index page
$(document).ready(function() {
    // Connect to the Socket.IO server.
    var waitTime = 60000;
    var socket = io();
    function setData(data, elementID) {
        var element = document.getElementById(elementID);
        element.textContent = data;
    }
    // Event handlers for connections.
    socket.on('connect', function() {
        socket.emit('query');
    });
    socket.on('getTemp', function(data) {
        setData(data, "tempData");
        setTempColor(data);
    });
    socket.on('getHumidity', function(data) {
        setData(data, "humidityData");
    });
    socket.on('getAirQuality', function(data) {
        // setData(data, "airQualityData");
        setAirValue(data);
    });
    socket.on('getPressure', function(data) {
        setData(data, "pressureData");
    });
    socket.on('query', async function() {
        await new Promise(r => setTimeout(r, waitTime));
        socket.emit('query');
    });
    window.onbeforeunload = function() {
        socket.emit('disconnected');
    }
});