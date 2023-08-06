
function alertsuccess(message, id){
    console.log("allersuccess: " + message);
    html = '<div class="alert alert-success fade in"><button type="button" class="close" data-dismiss="alert">×</button>' + message + '</div>';
    $("#"+id).append(html);
}

function alertblock(message, id){
    html = '<div class="alert alert-block fade in"><button type="button" class="close" data-dismiss="alert">×</button>' + message + '</div>';
    $("#"+id).append(html);
}

function alerterror(message, id){
    html = '<div class="alert alert-danger fade in"><button type="button" class="close" data-dismiss="alert">×</button>' + message + '</div>';
    $("#"+id).append(html);
}

function alertinfo(message, id){
    html = '<div class="alert alert-info fade in"><button type="button" class="close" data-dismiss="alert">×</button>' + message + '</div>';
    $("#"+id).append(html);
}

