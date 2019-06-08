function refreshInformation() {
  $.get("/api/server/status", function(data) {
    if(data == "running") {
      $("#StartPageServerStatus")
        .removeClass("btn-danger")
        .addClass("btn-success")
        .html("läuft.");
    } else {
      $("#StartPageServerStatus")
      .removeClass("btn-success")
      .addClass("btn-danger")
      .html("gestoppt.");
    }
  });
  $.get("/api/installer/getStatus", function(data) {
    if(data["status"] == "idle") {
      $("#StartPageInstallerStatus")
        .removeClass("btn-success")
        .addClass("btn-danger")
        .html("Nein");
      $("#StartPageInstallerLogs")
        .html("");
    } else {
      console.log(data["log"])
      $("#StartPageInstallerStatus")
      .removeClass("btn-danger")
      .addClass("btn-success")
      .html("Ja.");
      $("#StartPageInstallerLogs")
      .html("" + data["log"] + "");
    }
  });
}

window.onload = function () {
  refreshInformation();
  setInterval(refreshInformation, 3500);
}
