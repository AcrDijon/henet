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

function post_comment(server, form_id) {

    $.ajax({
        type: "POST",
        url: "http://localhost:8080/comments",
        data: JSON.stringify($('#henet_comment').serializeFormJSON()),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(data){
            alert(data);
        },
        failure: function(err) {
            alert(err);
        }
      });
      return false;
}

