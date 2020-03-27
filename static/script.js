function myFunction() {
  /* Get the text field */
  var copyText = document.getElementById("link-text");

  /* Select the text field */
  copyText.select();
  copyText.setSelectionRange(0, 99999); /*For mobile devices*/

  /* Copy the text inside the text field */
  document.execCommand("copy");

  /*
   Alert the copied text */
}

function thisFileUpload() {
  document.getElementById("input_file").click();
}

$(document).ready(function() {
  $("form").each(function() {
    this.reset();
  });
});

$(document).ready(function() {
  $("#input_file").change(function() {
    if ($(this).val()) {
      $("#uploadit").removeAttr("disabled");
      // or, as has been pointed out elsewhere:
      // $('input:submit').removeAttr('disabled');
    }
  });
});
