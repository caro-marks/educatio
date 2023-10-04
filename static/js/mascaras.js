$(function(){
  $('#id_cep').mask('00000-000');
  $('#id_telefone_principal').mask('(00) 0000-0000');
  $('#id_telefone_secundario').mask('(00) 00000-0000');
  $('#id_cnpj').mask('00.000.000/0000-00', {reverse: true});
})