function result_requests_export(checked_form_ecole_partner_school){

    var $checked_form_ecole_partner_school = checked_form_ecole_partner_school.toString();

    $("#request_export").attr('src', "/Telechargement_Fichier/"+$checked_form_ecole_partner_school);
}
