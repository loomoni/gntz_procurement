odoo.define('custom_procurement.website_tender_detail', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    var ajax = require('web.ajax');

    publicWidget.registry.tenderDetail = publicWidget.Widget.extend({
        selector: '#apply-button',

        start: function () {
            this.$el.on('click', _.bind(this._onClickApply, this));
        },

        _onClickApply: function (ev) {
            ev.preventDefault();
            this._renderApplicationForm();
        },

        _renderApplicationForm: function () {
            var self = this;
            var $form = $('<div>', { class: 'application-form' });

            // Create the form fields (name, email, phone, attachment, submit button)
            // Customize the form fields as needed

            // Append form fields to $form

            $form.append($('<button>', {
                class: 'btn btn-primary',
                text: 'Submit',
                click: function () {
                    // Handle form submission here
                    var formData = {
                        name: $('#name-input').val(),
                        email: $('#email-input').val(),
                        phone: $('#phone-input').val(),
                        attachment: $('#attachment-input')[0].files[0],
                        tender_id: self._getTenderId() // Get the tender ID
                    };

                    // Send the form data to the server
                    ajax.jsonRpc('/submit_application', 'call', formData).then(function (result) {
                        // Handle the response (e.g., show a confirmation message)
                        if (result.success) {
                            alert('Application submitted successfully.');
                            // Optionally, close the form or perform other actions
                        } else {
                            alert('Application submission failed. Please try again.');
                        }
                    });
                }
            }));

            // Display the form as a popup (you can use a library like Bootstrap modal or customize as needed)
            $form.dialog({
                modal: true,
                title: 'Apply for Tender',
                width: '400px',
                close: function () {
                    $form.remove();
                }
            });
        },

        _getTenderId: function () {
            // Implement a method to retrieve the tender ID from the page (e.g., from a hidden input)
            // Return the tender ID
        }
    });

    return publicWidget.registry.tenderDetail;
});
