window.onload = function() {

  var driverName = document.getElementById("driver_type")
  var scriptName = document.getElementById("script")
  var relayButton = document.getElementById("relayButton")

  function updateDriver() {
    var data = {"driver": driverName.value}

    var request = new XMLHttpRequest()
    request.onreadystatechange = function() {}
    request.open("POST", "/driver", true)
    request.setRequestHeader("Content-Type", "application/json;charset=UTF-8")
    request.send(JSON.stringify(data))
  }

  updateDriver()
  driverName.onchange = updateDriver

  function updateScript() {
    var data = {"script": scriptName.value}

    var request = new XMLHttpRequest()
    request.onreadystatechange = function() {}
    request.open("POST", "/script", true)
    request.setRequestHeader("Content-Type", "application/json;charset=UTF-8")
    request.send(JSON.stringify(data))
  }

  updateScript()
  scriptName.onchange = updateScript

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

      // TODO: do something with the data

      setTimeout(updateStatus, 1000)
    }
    request.open("GET", "/status", true)
    request.send()
  }

  updateStatus()
}
