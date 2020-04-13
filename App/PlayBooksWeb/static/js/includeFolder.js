

function xhr_data(url, options, callbackSucc, callbackFail, callbackAlways){
    $.ajax(url, options).done(function(data, textStatus, jqxhr){
        if( callbackSucc != null ){
            callbackSucc(data, textStatus, jqxhr);
        }
    }).fail(function(jqXHR, textStatus, errorThrown){
        if( callbackFail != null  ){
            callbackFail(jqXHR, textStatus, errorThrown);
        }
    }).always(function(dataOrJQXhr, textStatus, jqxhr){
        if( callbackAlways != null ){
            callbackAlways(dataOrJQXhr, textStatus, jqxhr);
        }
    });
}

function loadIF(url){
    options = {
        type: "GET",
        processData: false,
        contentType: false,
        cache: false,
        timeout: 600000,
    };
    xhr_data(url, options, function(data, textStatus, jqxhr){
        $("#content").append(data)
    }, function(jqXHR, textStatus, errorThrown){
        // on fail
    })
}

$(document).ready(function(){
    var url = $("#includeFolders").data(url);
    if( url ){
        loadIF(url);
    }
});