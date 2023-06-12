// $(document).ready(function () {
//     $('.increament-button').click(function (e) { 
//         e.preventDefault();
//         var inc_value = $(this).closest('.product_data').find('.qty-input').val();
//         var value = parseInt(inc_value, 10);
//         value = isNaN(value) ? 0 : value;
//         if(value < 0) {
//             value++;
//             $(this).closest('.product_data').find('.qty-input').val(value);
//         }
//     });
    
// });

$(document).ready(function() {
    // Increment button
    $('.increment-button').click(function() {
        var input = $(this).siblings('.qty-input');
        var value = parseInt(input.val());
        if (value < 10) {
            input.val(value + 1);    
        }
        
    });

    // Decrement button
    $('.decrement-button').click(function() {
        var input = $(this).siblings('.qty-input');
        var value = parseInt(input.val());
        if (value > 1) {
        input.val(value - 1);
        }
    });
});
