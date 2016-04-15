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

function generate_table_item(item, key) {
    open="<tr id=\""+key+"\"><td>";
    content=item['name']+"</td><td>";
    content+=item['quantity']+"</td><td>";
    content+="<button class=\"btn-primary buy_btn\" key="+key+">Proceed to Buy</button>";
    close="</td></tr>";
    return open+content+close;
}

$(document).ready(function(){
    selected_items={}
    $(document).on('click','.upvote_btn',function(){
        console.log("upvoted "+$(this).attr("key"));
    });
    $(document).on('click','.buy_btn',function(e){
        item_id = $(this).attr("key");
        window.location.href =  "/store/item/"+item_id;
        var x = document.getElementById("t1").rows[item_id].cells;

    });
    
    var ajaxRequest = $.ajax({
                        url : "/store/get_catalogue/", // the endpoint
                        type : "GET", // http method
                        contentType: "application/json",
                        success : function(catalogue) {
                            console.log("RECEIVED");
                            $('#t1 > tbody').html("");
                            for (var key in catalogue) {
                                console.log( key);
                                console.log(catalogue[key]);
                                table_item = generate_table_item(catalogue[key],key);
                                $('#t1 > tbody').append(table_item);
                                console.log($('#t1 > tbody'));
                                selected_items[key]=0;
                            }
                        },
                
                        error : function(xhr,errmsg,err) {
                            console.log("error");
                        }
                    });
    
    });