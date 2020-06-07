window.onload = function() {

  var inputButton = document.getElementById("inputButton")
  var scriptButton = document.getElementById("scriptButton")
  var relayButton = document.getElementById("relayButton")

  inputButton.onclick = function() {
    var inputName = document.getElementById("input_type")
    var data = {"input": inputName.value}

    var request = new XMLHttpRequest()
    request.onreadystatechange = function() {}
    request.open("POST", "/input", true)
    request.setRequestHeader("Content-Type", "application/json;charset=UTF-8")
    request.send(JSON.stringify(data))
  }

  scriptButton.onclick = function() {
    var scriptName = document.getElementById("script")
    var data = {"script": scriptName.value}

    var request = new XMLHttpRequest()
    request.onreadystatechange = function() {}
    request.open("POST", "/script", true)
    request.setRequestHeader("Content-Type", "application/json;charset=UTF-8")
    request.send(JSON.stringify(data))
  }

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
