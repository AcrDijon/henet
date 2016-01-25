$(document).ready(function () {
    $.fn.serializeFormJSON = function () {
        var o = {};
        var a = this.serializeArray();
        $.each(a, function () {
            if (o[this.name]) {
                if (!o[this.name].push) {
                    o[this.name] = [o[this.name]];
                }
                o[this.name].push(this.value || '');
            } else {
                o[this.name] = this.value || '';
            }
        });
        return o;
      };
});

function post_comment(form_id, server) {

    $.ajax({
        type: "POST",
        url: server + "/comments",
        data: JSON.stringify($(form_id).serializeFormJSON()),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(data){
            alert("Commentaire soumis à modération.");
            $(form_id).find("input[type=text], textarea").val("");
        },
        failure: function(err) {
            alert("Le commentaire n'a pas pu être soumis.");
        }
      });
      return false;
}

