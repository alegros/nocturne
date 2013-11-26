function demon()
{
    var selected_demon = $("#demon_list option:selected").val();
    var response = $.post("/demonList", {demon:selected_demon}, function(){
        $("#content").html(response.responseText);
    });
}

function fusion()
{
    var selected_d1 = $("#d1 option:selected").val();
    var selected_d2 = $("#d2 option:selected").val();
    var response = $.post("/fusion", {d1:selected_d1, d2:selected_d2}, function(){
        $("#content").html(response.responseText);
    });
}

function reverse() 
{
    var child = $("#child option:selected").val();
    var parent1 = $("#parent1 option:selected").val();
    var response = $.post("/reverseFusion", {child:child, parent1:parent1}, function(){
        $("#content").html(response.responseText);
    });
}
