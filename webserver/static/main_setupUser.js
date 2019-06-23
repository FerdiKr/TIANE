function finalizeConfig() {
  // freeze all input-boxes and buttons
  $("#mainContentBox input").addClass("disabled").attr("disabled", "disabled");
  $("#mainContentBox button").addClass("disabled").attr("onclick", "");
  $("#button_execute")
    .removeClass("btn-success")
    .addClass("btn-warning")
    .addClass("disabled")
    .attr("disabled", "disabled")
    .html("aktualisiere…");
  // fetch all data
  data = {
      "userName": $("#userName").val(),
      "userRole": $("#userRole").val(),
      "userTelegram": $("#userTelegram").val(),
      "userFullName": $("#userFullName").val(),
      "userFullLastName": $("#userFullLastName").val(),
      "userBirthYear": $("#userBirthYear").val(),
      "userBirthMonth": $("#userBirthMonth").val(),
      "userBirthDay": $("#userBirthDay").val(),
  }
  // push data to server
  $.get("/api/writeConfig/user/" + data["userName"], data, function(data) {
    window.location.replace("/index");
  });
}

window.onload = function() {
  $("#userName").change(function () {
    $.get("/api/loadConfig/user/" + $("#userName").val(), function(data) {
      if(data !== "user not found") {
        var ht = "<div class='alert alert-info'>";
        ht += "<h5>Information:</h5>";
        ht += "<p>Für diesen Namen wurde schon ein <b>bestehender Benutzer</b> gefunden.";
        ht += " Die bestehende Konfiguration wird nun in die Formular-Felder geladen."
        ht += " Bei einer Änderung wird die aktuelle Version <b>überschrieben</b>."
        ht += "</p>"
        ht += "</div>";
        $("#alert-box").html(ht);
        for (var element in data) {
          if (data.hasOwnProperty(element)) {
            $("#" + element).val(data[element]);
          }
        }
      }
    });
  });
}
