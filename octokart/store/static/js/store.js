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

function generate_table_item(item, key) {
    open="<tr><td>";
    //content=key+"</td><td>";
    content=item['name']+"</td><td>";
    content+=item['desc']+"</td><td>";
    content+=item['upvotes']+"</td><td>";
    content+="<button class=\"upvote_btn\" key="+key+">Upvote</button></td><td>";
    content+="<input class=\"input item-num\" type=\"text\" value=\"1\" id=\""+key+"\">"+"</td><td>";
    content+="<button class=\"buy_btn\" key="+key+">Buy</button>";
    close="</td></tr>";
    return open+content+close;
}


$(document).ready(function(){
    
    selected_items={}
    $(document).on('click','.upvote_btn',function(){
        console.log("upvoted "+$(this).attr("key"));
    });
    $(document).on('click','.buy_btn',function(){
        item_id = $(this).attr("key");
        quantity = $('#'+item_id).val();
        console.log("buyed item "+item_id+ "quantity=" +  quantity);
        

        var my_data = {
                        id: item_id,

                        //name: "its me",
                    };
        var ajaxRequest = $.ajax({
                    type: "PUT",
                    url: url_main ,
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
    var ajaxRequest = $.ajax({
                        url : "http://127.0.0.1:5000/seller/get_catalogue/", // the endpoint
                        type : "GET", // http method
                        contentType: "application/json",
                        success : function(catalogue) {
                            $('#t1 > tbody').html("");
                            for (var key in catalogue) {
                                console.log('a'+ key);
                                console.log(catalogue[key]);
                                table_item=generate_table_item(catalogue[key],key);
                                $('#t1 > tbody').append(table_item);
                                console.log($('#t1 > tbody'));
                                selected_items[key]=0;
                            }
                        },
                
                        error : function(xhr,errmsg,err) {
                            console.log("error");
                        }
                    });
    
    

    $('#refreshcat').click(function(event){
        var ajaxRequest = $.ajax({
                        url : url_main+ "seller/get_catalogue/", // the endpoint
                        type : "GET", // http method
                        contentType: "application/json",
                        success : function(catalogue) {
                            $('#t1 > tbody').html("");
                            for (var key in catalogue) {
                                console.log('b'+ key);
                                table_item=generate_table_item(catalogue[key], key);
                                $('#t1 > tbody').append(table_item);
                                selected_items[key]=0;
                            }
                        },
                
                        error : function(xhr,errmsg,err) {
                            console.log("error");
                        }
                    });
        });
    
    
    $('#synccat').click(function(event){
          var ajaxRequest = $.ajax({
                        url : "http://127.0.0.1:5000/seller/sync_catalogue/", // the endpoint
                        type : "GET", // http method
                        contentType: "application/json",
                        data : selected_items,
                        success : function(){
                            $('#synccat').html("Re-Sync");
                        },
                
                        error : function(xhr,errmsg,err) {
                            console.log("error");
                        }
                    }); 
        });    
    });