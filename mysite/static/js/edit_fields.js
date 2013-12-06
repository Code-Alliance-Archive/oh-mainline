(function($) {
    'use strict';

    $(document).ready(function() {
        $("a.collapse-fieldset").click(function(e) {
            e.preventDefault();

            var text = $(this).text();
            text = (text === 'Expand') ? 'Collapse' : 'Expand';
            $(this).text(text);

            var collapsed = (text === 'Expand');
            $(this).parents('fieldset').children().not('legend').toggleClass('collapsed');
        });

        $("a.select-all-fieldset").click(function(e) {
            e.preventDefault();

            $(this).parents('fieldset').find('input[type=checkbox]').prop('checked', true);
        });

        $("a.select-none-fieldset").click(function(e) {
            e.preventDefault();

            $(this).parents('fieldset').find('input[type=checkbox]').prop('checked', false);
        });
    });
})(jQuery);
