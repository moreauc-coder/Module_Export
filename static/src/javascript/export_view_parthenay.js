function result_requests_export(){
    var checkbox_field_list = [];
    var checkbox_fields = document.getElementsByClassName('checkbox_fields');
    for (var i = 0; i < checkbox_fields.length; i++)
    {
        if (checkbox_fields[i].checked == true){
            var checkbox_field = checkbox_fields[i].value;
            checkbox_field_list.push(checkbox_field);
        }
    }
    alert(checkbox_field_list);
    document.getElementById("request_export").src = '/tableau_export_fichier/'+checkbox_field_list.toString();

    return false;
//    var $checked_form_ecole_partner_school = checked_form_ecole_partner_school.toString();
//
//    $("#request_export").attr('src', "/tableau_export_fichier/"+fields_checked.toString());
}
