$(function () {

  $(".js-api-access").click(function () {
    $.ajax({
      url: '/api_access/',
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#APIcontact-authenticated").modal("show");
      },
      success: function (data) {
        $("#APIcontact-authenticated .modal-content").html(data.html_form);
      }
    });
  });

});