$(function(){
  $('#parente_option').change(function() {
    let selectedForm = $(this).val()
    $('.optionalRequired').prop('required', selectedForm === "new")
    if (selectedForm === "existing") {
      $("#novoParente").hide()
      $("#existenteParente").show()
    } else if (selectedForm === "new") {
      $("#novoParente").show()
      $("#existenteParente").hide()
    }
  })
})