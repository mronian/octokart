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

$('document').ready(function(){
    
    $('.check-connection').click(function(event){
        var id = $(this).attr("conn_id");
        var ajaxRequest = $.ajax({
                        url : "check_connection/", // the endpoint
                        type : "GET", // http method
                        contentType: "application/json",
                        data: {"id":id},
                        success : function(response) {
                            $("#response-"+id).html(response.success);
                        },
                
                        error : function(xhr,errmsg,err) {
                            console.log("error");
                        }
                    });
        });
    });