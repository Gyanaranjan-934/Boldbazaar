
$(document).ready(function() {
    // Increment button
    $('.increment-button').click(function() {
        var input = $(this).siblings('.qty-input');
        var value = parseInt(input.val());
        if (value < 5) {
            input.val(value + 1);    
        }
        var submitButton = $(this).closest('.product_data').find('.update-button');
        submitButton.show();
    });

    // Decrement button
    $('.decrement-button').click(function() {
        var input = $(this).siblings('.qty-input');
        var value = parseInt(input.val());
        if (value > 1) {
            input.val(value - 1);
        }
        var submitButton = $(this).closest('.product_data').find('.update-button');
        submitButton.show();
    });
    
});


  
  
  
