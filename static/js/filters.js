$(function(){
  $('#escola-select').change(function(){
    let escola_id = $(this).val()
    $('#atividade-select option').each(function(){
      let atividade_escola_id = $(this).data('escola')
      if (atividade_escola_id == escola_id || escola_id === '') {
        $(this).show()
      } else {
        $(this).hide()
      }
    })  

    let opcoes_visiveis = $('#atividade-select option:visible')
    if (opcoes_visiveis.length > 0) {
      opcoes_visiveis.first().prop('selected', true)
    } else {
      $('#atividade-select').val('')
    }
  })
})