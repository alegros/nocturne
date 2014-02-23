function demon()
{
    var selected_demon = $("#demon_list option:selected").val();
    var response = $.post("/demonList", {demon:selected_demon}, function(){
        $("#response").html(response.responseText);
    });
}

function fusion()
{
    var selected_d1 = $("#d1 option:selected").val();
    var selected_d2 = $("#d2 option:selected").val();
    var response = $.post("/fusion", {d1:selected_d1, d2:selected_d2}, function(){
        $("#response").html(response.responseText);
    });
}

function reverse_demon() 
{
    var child = $("#childdemon option:selected").val();
    var parentdemon = $("#parentdemon option:selected").val();
    var response = $.post("/reverseFusion", {child:child, parentdemon:parentdemon}, function(){
        $("#response").html(response.responseText);
    });
}

function reverse_race() 
{
    var childrace = $("#childrace option:selected").val();
    var parentrace = $("#parentrace option:selected").val();
    var response = $.post("/reverseFusion", {childrace:childrace, parentrace:parentrace}, function(){
        $("#response").html(response.responseText);
    });
}

function search()
{
    // Récupérer les champs fu formulaire...
    //var allSelects = $(":select");
    //$("#response").html(allSelects.length+" selects found");
    //$("#response").html("coucou");
    //var values = $("select option:selected").val();
    var level = $("#level").val();
    var response = $.post("/search", {level:level},  function() {
        $("#response").html(response.responseText);
    });
}
