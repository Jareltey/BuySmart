$('.table').hide()

$('.dropdown-item').each(function(index){
  return $(this).click(function(){
    $('.table').hide();
    $('.table').eq(index).show()
  })
})

$('tr').not('thead tr').each(function(){
  var $td = $(this).children(':not(:first)');
  var vals = $td.filter(function(){
    return $.isNumeric(+$(this).text())
  }).map(function(){
    return +$(this).text();
  })
  var min = Math.min.apply(Math,vals)
  $td.filter(function(){
    return +$(this).text() === min;
  }).css('color','red')
});

// $('table').each(function(){
//   var $td = $(this).find('.values');
//   var vals = $td.filter(function(){
//     return $.isNumeric(+$(this).text())
//   }).map(function(){
//     return +$(this).text()
//   })
//   var min = Math.min.apply(Math,vals)
//   $td.filter(function(){
//     return +$(this).text() === min
//   }).css('font-weight','bold')
// })

$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})
