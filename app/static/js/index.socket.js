// Element colours
let blue = "#5dade2";
let green = "#198754";
let orange = "#f39c12";
let red = "#CB4335";

function setColorIfTrue(elementID, options)
{
    for (let elem of options) {
        if (elem[0]) {
            document.getElementById(elementID).style.backgroundColor = elem[1];
            break;
        }
    }
}

let airQualityValues = [];
function setAirValue(airValue)
{
    airQualityValues.push(airValue);
    minVal = Math.min(...airQualityValues);
    maxVal = Math.max(...airQualityValues);
    let arr = [[(airValue - minVal <= 500), blue], [true, orange]];
    // Set colour and element values
    setColorIfTrue("airQualCol", arr);
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
        let arr = [[(data < 18), blue], [(data > 18 && data < 24), green], [true, red]];
        setColorIfTrue("tempDataCol", arr);
    });
    socket.on('getHumidity', function(data) {
        setData(data, "humidityData");
        let arr = [[(data >= 30 && data <= 60), green], [true, orange]];
        setColorIfTrue("humidityDataCol", arr);
    });
    socket.on('getAirQuality', function(data) {
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