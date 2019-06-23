function triggerSystemCheck() {
  $.get("/api/installer/listPackages/details", function(data) {
    var disallowCount = 0;
    var html = "";
    for(checkpoint in data) {
      cd = data[checkpoint];
      html += "<tr class=\"tbl_module\">";
      if(cd["status"].includes("(False,")) {
        if(cd["required"] == "partially") {
          color = "warning";
          buttonText = "Nicht installiert";
          install = true;
        } else {
          color = "danger";
          buttonText = "Nicht installiert, zwingend erforderlich";
          install = true;
        }
      } else if (cd["status"].includes("(True,")) {
        color = "success";
        buttonText = "Installiert";
        install = false;
      } else {
        color = "secondary";
        buttonText = "Status unbekannt";
        install = true;
      }
      html += '<td><div class="alert alert-' + color + '">';
      html += buttonText;
      html += '</div></td>';
      html += '<td><p>' + cd["name"] + '</p>';
      html += '<i>' + cd["desc"] + '</i></td>';
      if(install == true) {
        html += '<td><button type="button" class="btn btn-primary" onclick="triggerInstallation(this, \'' + cd["name"] + '\')">';
        html += "Installation starten";
        html += '</button></td>';
      } else {
        html += "<td><span>Modul bereits installiert</span></td>"
      }
    }
    $("#mainTable").html(html).fadeIn(200);
  });
}

function triggerInstallation(e, packageName) {
  $.get("/api/installer/startInstallation/" + packageName, function (data) {
    if(data == true) {
      $(this)
      .removeClass("btn-primary")
      .addClass("btn-secondary")
      .addClass("disabled")
      .attr("onclick", "")
      .html("Installation läuft…")
    } else {
      $(this)
      .removeClass("btn-primary")
      .addClass("btn-danger")
      .html("Fehler!")
    }
  });
}

window.onload = function () {
  triggerSystemCheck()
  setInterval(function() { triggerSystemCheck();}, 5000);
}
