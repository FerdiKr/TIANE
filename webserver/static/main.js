function triggerSystemCheck() {
  $.get("/api/checkServerInstallation", function(data) {
    var disallowCount = 0;
    for(checkpoint in data) {
      cd = data[checkpoint];
      $("#tbl_" + checkpoint + " button")
        .removeClass("btn-secondary")
        .html("");
      switch (cd["status"]) {
        case "okay":
          $("#tbl_" + checkpoint + " button")
            .addClass("btn-success")
            .html("Okay");
          break;
        case "partially":
          $("#tbl_" + checkpoint + " button")
            .addClass("btn-warning")
            .html("nicht installiert");
            $("#tbl_" + checkpoint + " i")
              .html(cd["desc"])
          break;
        case "error":
          $("#tbl_" + checkpoint + " button")
            .addClass("btn-danger")
            .html("nicht installiert");
            $("#tbl_" + checkpoint + " i")
              .html(cd["desc"])
          disallowCount += 1;
          break;
        default:
          $("#tbl_" + checkpoint + " button")
            .addClass("btn-primay")
            .html("Fehler.");
      }
    }
    if(disallowCount == 0) {
      $("#button_next")
        .removeClass("disabled").attr("href", "setup_3")
    }
  });
}

window.onload = function () {
  triggerSystemCheck()
}
