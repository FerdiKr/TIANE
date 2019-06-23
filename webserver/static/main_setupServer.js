function finalizeConfig() {
  // freeze all input-boxes and buttons
  $("#mainContentBox input").addClass("disabled").attr("disabled", "disabled");
  $("#mainContentBox button").addClass("disabled").attr("onclick", "");
  $("#button_execute")
    .removeClass("btn-success")
    .addClass("btn-warning")
    .html("aktualisiere…");
  // fetch all data
  data = {
      "tianeName": $("#tianeName").val(),
      "tianeSystem": $("#tianeSystem").val(),
      "tianeActivation": $("#tianeActivation").val(),
      "keyLength": $("#keyLength").val(),
      "homeLocation": $("#homeLocation").val(),
      "telegramBotId": $("#telegramSupport").val(),
      "useCameras": ($("#useCameras").val() == "Ja") ? true : false,
      "useFaceRec": ($("#useFaceRec").val() == "Ja") ? true : false,
      "useInterface": ($("#useInterface").val() == "Ja") ? true : false,
  }
  // push data to server
  $.get("/api/writeConfig/server", data, function(data) {
    window.location.replace("/index");
  });
}
