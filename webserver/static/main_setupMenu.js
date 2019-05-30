function triggerInstallationStatus() {
  $.get("/api/installer/getStatus", function(data) {
    if(data["status"] == "idle") {
      $("#installationAlert").remove();
      $("#installationButtons a").removeClass("disabled");
    } else {
      setTimeout(function() { triggerInstallationStatus();}, 5000);
    }
  });
}

window.onload = function () {
  triggerInstallationStatus();
}
