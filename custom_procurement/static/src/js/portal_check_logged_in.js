odoo.define('custom_procurement.portal_check_logged_in', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');

    publicWidget.registry.websiteTenderDetail = publicWidget.Widget.extend({
        selector: '#apply-button',
        disabledInEditableMode: false,

        start: function () {
            var self = this;
            this._rpc({
                route: '/website_tender_detail/is_logged_in',
            }).then(function (result) {
                if (result.logged_in) {
                    self.$el.show();
                } else {
                    self.$el.hide();
                }
            });
            return this._super.apply(this, arguments);
        },
    });
});
