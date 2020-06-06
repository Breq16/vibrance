window.onload = function() {
  var input_type = document.getElementById("input_type")

  input_type.onchange = function() {
  	var value = input_type.options[input_type.selectedIndex].value

    if (value == "MIDI") {
      document.getElementById("MIDI-settings").style.display = "block"
      document.getElementById("UART-settings").style.display = "none"
    } else if (value == "UART") {
      document.getElementById("UART-settings").style.display = "block"
      document.getElementById("MIDI-settings").style.display = "none"
    } else {
      document.getElementById("MIDI-settings").style.display = "none"
      document.getElementById("UART-settings").style.display = "none"
    }
  }

  var relayButton = document.getElementById("relayButton")

  relayButton.onclick = function() {
    var relayInput = document.getElementById("relayHost")
    var relayPsk = document.getElementById("relayPsk")
    var data = {"host": relayInput.value, "psk": relayPsk.value}

    var request = new XMLHttpRequest()
    request.onreadystatechange = function() {}
    request.open("POST", "/relay", true)
    request.setRequestHeader("Content-Type", "application/json;charset=UTF-8")
    request.send(JSON.stringify(data))
  }

  var relayStatus = document.getElementById("relayStatus")

  function updateStatus() {
    var request = new XMLHttpRequest()
    request.onload = function() {
      var data = JSON.parse(request.response)
      if (data["relay"]["enabled"] === false) {
        relayStatus.className = "inactive"
        relayStatus.innerText = "Inactive"
      } else if (data["relay"]["enabled"] === true) {
        if (data["relay"]["connected"] === false) {
          relayStatus.className = "failure"
          relayStatus.innerText = "Disconnected"
        } else if (data["relay"]["connected"] === true) {
          relayStatus.className = "success"
          relayStatus.innerText = "Connected"
        }
      }
      setTimeout(updateStatus, 1000)
    }
    request.open("GET", "/status", true)
    request.send()
  }

  updateStatus()
}
