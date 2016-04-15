url_main = "http://127.0.0.1:5000/"
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
        }
    }
});

$(document).ready(function(){
    $('.buy_btn').click(function(){
        var url = window.location.href;     // Returns full URL
        var ar = url.split('/');
        var item_id = $(this).attr("key");
        var seller_name = $(this).attr("keys");
        var quantity = $("#q-"+seller_name).val()
        var number_items = $("#av-"+seller_name).html();
        console.log("quantity=" + quantity+"number_items="+number_items+"seller_name="+seller_name+"item_id="+item_id);
        if(quantity>number_items) {
            alert("Too many items asked.");
            return;
        }
        var my_data =   {
                            item_id:item_id,
                            seller_name:seller_name,
                            quantity:quantity
                        }
        console.log(my_data);
        var ajaxRequest = $.ajax({
            type: "PUT",
            url: url_main, // enter the url from where to buy (buy request ),
            data: my_data,
            success: function(msg){
                console.log( "Data updated: " + msg );
            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
            alert("some error" );

            console.log(XMLHttpRequest)
            console.log(textStatus);
            console.log(errorThrown);
            }
            });
    });

});