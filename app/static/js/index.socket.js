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
    });
    socket.on('getHumidity', function(data) {
        setData(data, "humidityData");
    });
    socket.on('getAirQuality', function(data) {
        setData(data, "airQualityData");
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