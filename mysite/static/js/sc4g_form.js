jQuery(document).ready(function($) {
    'use strict';

    (function() {
        function parseInputFields() {
            var questions = [];
            var form = $('form.webform-client-form');

            var getValues = function(selector) {
                var valueArray = [];

                $(selector).each(function(index, element) {
                    if ($(element).is('option')) {
                        valueArray.push($(element).text());
                    } else {
                        valueArray.push($(element).next('label').eq(0).text());
                    }
                });

                return valueArray;
            };

            var getSelectValue = function(selector) {
                var valueArray = [];

                if ($(selector).find('option').length > 0 && $(selector).val() !== null) {
                    var values = $(selector).val();
                    for (var i = 0; i < values.length; i++) {
                        $(selector).find('option[value=\'' + values[i] + '\']').each(function (index, element) {
                            valueArray.push($(this).text());
                        });
                    }
                }

                return valueArray;
            };

            var getSelectType = function(selector) {
                if ($(selector).is('[size]') && parseInt($(selector).attr('size')) > 1) {
                    return 'multi';
                }
                return 'single';
            };

            String.prototype.trim = function() {
                return this.replace(/^\s\s*/, '').replace(/\s\s*$/, '');
            };

            form.find('div.webform-component').each(function (index, element) {
                var inputType = null;
                var label = $(this).find('label').eq(0).text().trim();
                var requiredLabel = $(this).find('label').eq(0).next('span.form-required');
                var values = [];
                var responses = [];
                var required = (requiredLabel.length) ? true : false;
                if (label.indexOf('*') > -1) {
                    required = true;
                    label = label.substring(0, label.indexOf('*')).trim();
                }

                if ($(this).find('input[type=text]').length > 0) {
                    // text or url
                    var text = $(this).find('input[type=text]');
                    if (text !== undefined && text.attr('id').search('url') > 0) {
                        inputType = 'url';
                    } else {
                        inputType = 'text';
                    }
                    responses = [ $(this).find('input[type=text]').val() ];
                } else if ($(this).find('input[type=email]').length > 0) {
                    inputType = 'text';
                    responses = [ $(this).find('input[type=email]').val() ];
                } else if ($(this).find('input[type=file]').length > 0) {
                    inputType = 'file';
                } else if ($(this).find('input[type=radio]').length > 0) {
                    inputType = 'single';
                    values = getValues($(this).find('input[type=radio]'));
                    responses = getValues($(this).find('input[type=radio]:checked'));
                } else if ($(this).find('select').length > 0) {
                    var select = $(this).find('select');
                    inputType = getSelectType(select);
                    values = getValues($(this).find('option'));
                    responses = getSelectValue(select);
                } else if ($(this).find('input[type=checkbox]').length > 0) {
                    inputType = 'multi';
                    values = getValues($(this).find('input[type=checkbox]'));
                    responses = getValues($(this).find('input[type=checkbox]:checked'));
                } else if ($(this).find('textarea').length > 0) {
                    inputType = 'textarea';
                    responses = [ $(this).find('textarea').val() ];
                }

                if (inputType === null) {
                    return true;
                }

                var question = {
                    inputType: inputType,
                    label: label,
                    values: values,
                    required: required,
                    responses: responses
                };
                questions.push(question);
            });

            $.post('http://127.0.0.1:8000/account/signup', { data: JSON.stringify(questions) })
                .success(function(response) {
                    return true;
                }).error(function(response) {
                    alert('There was an error while processing the form.');
                    return false;
                });
        }

        $('form').submit(function(e) {
            e.preventDefault();
            if (parseInputFields()) {
                $(this).submit();
            }
        });

    }(jQuery));
});