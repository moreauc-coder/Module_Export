odoo.define('export_view_parthenay', function (require) {
    "use strict";
    var core = require('web.core');
    var ListController = require('web.ListController');
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
            window.open('/export_fichier/', '_blank');
        }
    });
})
