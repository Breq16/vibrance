const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);

var enc = new TextEncoder();

function setColor(color) {
    document.getElementById("screen").style.backgroundColor = "#"+color;
    if (color === "000000" || color === "000") {
        document.getElementById("status").style.color = "#FFF";
    } else {
        document.getElementById("status").style.color = "#000";
    }
}

function runApp() {
    var socket;
    if (urlParams.get("ssl") === "0") {
        socket = new WebSocket("ws://"+urlParams.get("host")+":9000",
                               "binary");
    } else {
        socket = new WebSocket("wss://"+urlParams.get("host")+":9000", "binary");
    }
    socket.binaryType = "arraybuffer";

    socket.onopen = function(event) {
        console.log(urlParams.get("zone"));
        socket.send(enc.encode(urlParams.get("zone")));
        document.getElementById("status").innerText = "Connected";

        function sendAcknowledges() {
            if (socket) {
                socket.send(enc.encode("OK"));
                setTimeout(sendAcknowledges, 10000);
            }
        }
        setTimeout(sendAcknowledges, 10000);
    }

    socket.onmessage = function(event) {
        var decodedString = String.fromCharCode.apply(null,
                                                new Uint8Array(event.data));
        var messages = JSON.parse(decodedString);

        messages.forEach(function(message, index) {

            var color = message["color"];
            var delay = message["delay"] | 0;
            var duration = message["duration"];
            var motd = message["motd"];

            if (typeof color !== "undefined") {
                setTimeout(setColor, delay, color);

                if (duration > 0) {
                    setTimeout(setColor, delay+duration, "000");
                }
            }

            if (typeof motd !== "undefined") {
                setTimeout(function(motd) {
                    document.getElementById("status").innerText = motd;
                }, delay, motd);
            }

        });
    }

    socket.onerror = function(event) {
      console.log("ERROR");
    }

    socket.onclose = function(event) {
        console.log("Closed "+event.reason)
        socket = null;
        setColor("000");
        document.getElementById("status").innerText = "Reconnecting";
        setTimeout(runApp, 1000); // Try again in 1s
    }
}

runApp();
