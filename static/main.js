$(document).ready(function () {
  console.log("Hello World")

  $('#valid').on('click', function(event) {
    $(location).attr('href', '/orders?valid=True')
  })

  $('#invalid').on('click', function(event) {
    $(location).attr('href', '/orders?valid=False')
  })

  $('#allOrders').on('click', function(event) {
    $(location).attr('href', '/orders')
  })

  $('#btnFilter').on('click', function(event) {
    var orderId = $('#orderIdFilter').val()
    var orderUrl = ('/orders/').concat(orderId)
    if (orderUrl == '/orders/') {
      $('.innertube ul').append('Enter a valid order')
    }
    else {
    $(location).attr('href', orderUrl)
    };
  })

})
