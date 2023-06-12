$(document).ready(function () {
    $('.payWithRazorpay').click(function (e) { 
        e.preventDefault();

        var fname = $("[name='firstname']").val();
        var lname = $("[name='lastname']").val();
        var email = $("[name='email']").val();
        var phone = $("[name='phone']").val();
        var address = $("[name='address']").val();
        var city = $("[name='city']").val();
        var state = $("[name='state']").val();
        var country = $("[name='country']").val();
        var pincode = $("[name='pincode']").val();
        var token = $("[name='csrfmiddlewaretoken']").val();

        if(fname == '' || lname == '' || email == '' || phone == '' || address == '' || city == '' || state == '' || country == '' || pincode == ''){
            swal("Alert","All the fields are required","error");
            return false;
        }else{
            $.ajax({
                type: "GET",
                url: "/proceed-to-pay",
                success: function (response) {
                    // console.log(response);
                    var options = {
                        "key": "rzp_test_YRYU0PEcovQcFp", // Enter the Key ID generated from the Dashboard
                        "amount": response.total_price*100, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                        "currency": "INR",
                        "name": "BoldBazaar", //your business name
                        "description": "Thank you shopping with us",
                        // "order_id": "order_9A33XWu170gUtm", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
                        "handler": function (responseb){
                            // alert(responseb.razorpay_payment_id);
                            data={
                                "firstname":fname,
                                "lastname":lname,
                                "email":email,
                                "phone":phone,
                                "address":address,
                                "city":city,
                                "state":state,
                                "country":country,
                                "pincode":pincode,
                                "payment_mode":"Razorpay",
                                "payment_id":responseb.razorpay_payment_id,
                                csrfmiddlewaretoken:token
                            }
                            $.ajax({
                                type: "POST",
                                url: "/place-order",
                                data: data,
                                dataType: "json",
                                success: function (responsec) {
                                    swal("Congratulations!", responsec.status , "success").then((value) => {
                                        window.location.href = '/my-orders';
                                    });
                                },
                                error: function (xhr, errmsg, err) {
                                    console.log(xhr.status + ": " + xhr.responseText);
                                    swal("Error", "An error occurred while placing the order.", "error");
                                },
                            });
                        },
                        "prefill": { //We recommend using the prefill parameter to auto-fill customer's contact information, especially their phone number
                            "name": fname+" "+lname, //your customer's name
                            "email": email, 
                            "contact": phone  //Provide the customer's phone number for better conversion rates 
                        },
                        
                        "theme": {
                            "color": "#3399cc"
                        }
                    };
                    var rzp1 = new Razorpay(options);
                    rzp1.open();
                }
            });
            
        }

        
        
    });
});