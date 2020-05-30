// Hide and show relevant tables

$('.table').hide()

$('.dropdown-item').each(function(index){
  return $(this).click(function(){
    $('.table').hide();
    $('.table').eq(index).show()
  })
})

// Make lowest price for each product red

$('tr').not('thead tr').each(function(){
  var $td = $(this).children(':not(:first)');
  var vals = $td.filter(function(){
    return $.isNumeric(+$(this).clone().find('button').remove().end().text())
  }).map(function(){
    return +$(this).clone().find('button').remove().end().text();
  })
  var min = Math.min.apply(Math,vals)
  $td.filter(function(){
    return +$(this).clone().find('button').remove().end().text() === min;
  }).css('color','red')
});

// Shopping cart

if (document.readyState == 'loading') {
  document.addEventListener('DOMContentLoaded',ready)
} else {
  ready
}

function ready() {

    $('.content-section').hide()
    $('.btn-info').on('click',function(){
      $('.helptext').hide()
      $('.dropdown').hide()
      $('.table').hide()
      $('.btn-secondary').eq(2).hide()
      $('.btn-info').hide()
      $('.content-section').show()
    })

    $('#backtoproductlisting').on('click',function(){
      $('.helptext').show()
      $('.dropdown').show()
      $('.btn-secondary').eq(2).show()
      $('.btn-info').show()
      $('.content-section').hide()
    })

    var removeCartItemButtons = document.getElementsByClassName('btn-danger')
    for (var i = 0; i < removeCartItemButtons.length; i++) {
        var button = removeCartItemButtons[i]
        button.addEventListener('click', removeCartItem)
    }

    var quantityInputs = document.getElementsByClassName('cart-quantity-input')
    for (var i = 0; i < quantityInputs.length; i++) {
        var input = quantityInputs[i]
        input.addEventListener('change', quantityChanged)
    }

    $('.btn-success').each(function(){
      return $(this).click(function(){
        var price = $(this).parent().clone().children().remove().end().text()
        var shopname = $(this).parent().attr('id').split('%')[0]
        var shopaddress = $(this).parent().attr('id').split('%')[1]
        var product = $(this).parent().attr('id').split('%')[2]
        var mall = $(this).parent().parent().parent().parent().parent().children('div .helptext:eq(0)').children('p:eq(1)').children('span').children('em').text()
        addItemToCart(mall,shopname,shopaddress,product,price)
        updateCartTotal()
      })
    })

    $('.btn-success').click(function(){
      Disable($(this))
    })

    function Disable(button){
      button.attr('disabled',true)
    }
}

function removeCartItem(event){
  var buttonClicked = event.target
  buttonClicked.parentElement.parentElement.remove()
  updateCartTotal()
}

function quantityChanged(event){
    var input = event.target
    if (isNaN(input.value) || input.value <= 0) {
        input.value = 1
    }
    updateCartTotal()
}

function addItemToCart(mall,shopname,shopaddress,product,price){
  var cartRow = document.createElement('div')
  cartRow.classList.add('cart-row')
  var cartItems = document.getElementsByClassName('cart-items')[0]
  var cartItemNames = cartItems.getElementsByClassName('cart-product')
  var cartItemShops = cartItems.getElementsByClassName('cart-shopname')
  for (var i = 0; i < cartItemNames.length; i++) {
    if (cartItemNames[i].innerText == product && cartItemShops[i].innerText == shopname) {
      alert('This item is already added to the cart')
      return
    }
  }
  var cartRowContents =
      `<span class="cart-mall cart-column">${mall}</span>
      <span class='cart-shopname cart-column'>${shopname}</span>
      <span class='cart-shopaddress cart-column'>${shopaddress}</span>
      <span class='cart-product cart-column'>${product}</span>
      <span class='cart-price cart-column'>${price}</span>
      <div class="cart-quantity cart-column">
        <input class='cart-quantity-input' type='number' value="1">
        <button class='btn btn-danger' type="button">REMOVE</button>
      </div>`
  cartRow.innerHTML = cartRowContents
  cartItems.append(cartRow)
  cartRow.getElementsByClassName('btn-danger')[0].addEventListener('click', removeCartItem)
  cartRow.getElementsByClassName('cart-quantity-input')[0].addEventListener('change', quantityChanged)
}

function updateCartTotal() {
    var cartItemContainer = document.getElementsByClassName('cart-items')[0]
    var cartRows = cartItemContainer.getElementsByClassName('cart-row')
    var total = 0
    for (var i = 0; i < cartRows.length; i++) {
        var cartRow = cartRows[i]
        var priceElement = cartRow.getElementsByClassName('cart-price')[0]
        var quantityElement = cartRow.getElementsByClassName('cart-quantity-input')[0]
        var price = parseFloat(priceElement.innerText.replace('$', ''))
        var quantity = quantityElement.value
        total = total + (price * quantity)
    }
    total = Math.round(total * 100) / 100
    document.getElementsByClassName('cart-total-price')[0].innerText = '$' + total
}



// Make lowest price in product category bold
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
