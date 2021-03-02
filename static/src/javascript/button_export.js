odoo.define('export_view_parthenay', function (require) {
    "use strict";
    var core = require('web.core');
//    var ListView = require('web.ListView')
    var ListController = require('web.ListController');
    var rpc = require('web.rpc');

    ListController.include({
        renderButtons: function($node) {
        this._super.apply(this, arguments);
            if (this.$buttons) {
                let button_export = this.$buttons.find('.oe_button_export');
                button_export && button_export.click(this.proxy('button_export')) ;
            }
        },
        button_export: function () {
            // my code
            rpc.query({
                model:'export.student',
                method:'get_active_records',
            }).then(function (result) {
                // On envoie les données en POST avedc Ajax
                //prepare your data values to be sent in the request
                //create an XMLHttpRequest
//                var xmlhttp;
//                if (window.XMLHttpRequest){
//                    xmlhttp = new XMLHttpRequest();
//                } else {
//                    xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
//                }
//
//                //submit the request to your desired page (user will not be redirected, as this is AJAX request
//                xmlhttp.open('POST', '/export_fichier/', true);
//                xmlhttp.setRequestHeader('Content-type','application/x-www-form-urlencoded');
//                xmlhttp.send('data_back='+result);
//                xmlhttp.onload = function () {
//                    // do something to response
//                    window.open('/export_fichier/', '_blank');
//                };
                console.log("Done");
                alert(result);
                window.open('/export_fichier/'+result.toString(), '_blank');
            });
//            window.open('/export_fichier/', '_blank');
        },
    });
})