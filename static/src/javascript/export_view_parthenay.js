function result_requests_export(){
    var checkbox_field_list = [];
    var checkbox_fields = document.getElementsByClassName('checkbox_fields');
    var data_back = document.getElementById('data_back');
    for (var i = 0; i < checkbox_fields.length; i++)
    {
        if (checkbox_fields[i].checked == true){
            var checkbox_field = checkbox_fields[i].value;
            checkbox_field_list.push(checkbox_field);
        }
    }
//    alert(data_back.value.toString());
    document.getElementById("request_export").src = '/tableau_export_fichier/'+checkbox_field_list.toString()+'/'+data_back.value.toString();

    return false;
}

function check(){
    tableau_checkbox = document.getElementsByClassName('checkbox_fields');
    if (document.getElementById('all').checked){
        for (var i=0; i < tableau_checkbox.length; i++){
            tableau_checkbox[i].checked = true;
        }
    }
    else {
        for (var i=0; i < tableau_checkbox.length; i++){
            tableau_checkbox[i].checked = false;
        }
    }
}

// Cacher le menu pour l'iframe
if (document.getElementsByTagName('header')){
    document.getElementsByTagName('header')[0].style.display = "none";
}
if (document.getElementById('oe_main_menu_navbar')){
    document.getElementById('oe_main_menu_navbar').style.display = "none";
}