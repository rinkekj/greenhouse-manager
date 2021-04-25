$("#family_select").change(function() {
  var make_id = $(this).find(":selected").val();
  var request = $.ajax({
    type: 'GET',
    url: '/plants/_family_select',
  });
  request.done(function(data){
    var option_list = [["", "--- Select One ---"]].concat(data);

$("#genus_select").empty();
  for (var i = 0; i < option_list.length; i++) {
    $("#genus_select").append(
      $("<option></option>").attr(
        "value", option_list[i][0]).text(option_list[i][1])
       );
     }
  });
});
