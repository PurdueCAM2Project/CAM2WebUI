$("#APIcontact-authenticated").on("submit", ".js-api-access-form", function () {
  console.log("submitted")

  var form = $(this);
  $.ajax({
    url: form.attr("action"),
    data: form.serialize(),
    type: form.attr("method"),
    dataType: 'json',
    success: function (data) {
      if (data.form_is_valid) {
        alert("Book created!");  // <-- This is just a placeholder for now for testing
      }
      else {
        $("#APIcontact-authenticated .modal-content .modal-body").html(data.html_form);
      }
    }
  });
  return false;
});   

$(function () {

  $(".js-api-access").click(function () {
      $.ajax({
        url: '/api_access/',
        type: 'get',
        dataType: 'json',
        beforeSend: function () {
          $("#APIcontact-authenticated").modal("show");
        },
        error: function(){
            console.log("error");
        },
        success: function (data) {
          $("#APIcontact-authenticated .modal-content .modal-body").html(data.html_form);
          console.log("success");

        }
      });
      
  });

});