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
    content=key+"</td><td>";
    content+=item['name']+"</td><td>";
    content+=item['desc']+"</td><td>";
    content+="<input class=\"input item-num\" type=\"text\" value=\"0\" id=\""+key+"\">"+"</td><td>";
    close="</td></tr>";
    return open+content+close;
}

$('document').ready(function(){
    
    selected_items={}
    
    var ajaxRequest = $.ajax({
                        url : "http://127.0.0.1:5000/seller/get_catalogue/", // the endpoint
                        type : "GET", // http method
                        contentType: "application/json",
                        success : function(catalogue) {
                            $('#tablebody').html("");
                            for (var key in catalogue) {
                                table_item=generate_table_item(catalogue[key], key);
                                $('#tablebody').append(table_item);
                                selected_items[key]=0;
                            }
                        },
                
                        error : function(xhr,errmsg,err) {
                            console.log("error");
                        }
                    });
    
    $('#refreshcat').click(function(event){
        var ajaxRequest = $.ajax({
                        url : "http://127.0.0.1:5000/seller/get_catalogue/", // the endpoint
                        type : "GET", // http method
                        contentType: "application/json",
                        success : function(catalogue) {
                            $('#tablebody').html("");
                            for (var key in catalogue) {
                                table_item=generate_table_item(catalogue[key], key);
                                $('#tablebody').append(table_item);
                                selected_items[key]=0;
                            }
                        },
                
                        error : function(xhr,errmsg,err) {
                            console.log("error");
                        }
                    });
        });
    
    $(document).on('blur','.item-num',function(event){
            id=$(this).attr("id");
            selected_items[id]=$(this).val();
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