// Execute when the DOM is fully loaded
$(document).ready(function() {

    // Prevent duplicate submissions
    $('form').submit(function() {
        $(this).find(':submit').attr('disabled', 'disabled');
    });

    // Make entire rows clickable
    $(document).on('click', '.clickable', function() {
        console.log("click");
        // If unchecked row is clicked
        if ($(this).find('td input[type=checkbox]').prop("checked") == false) {
            // Row click
            console.log(this, "this");
            if (event.target.type !== 'checkbox') {
                $(this).find('td input[type=checkbox]').prop('checked', true);
                $(this).css('background', '#b8daff');
                // Checkbox click
            } else {
                $(this).css('background', 'white');
            }
            // If checked row is clicked
        } else if ($(this).find('td input[type=checkbox]').prop("checked") == true) {
            // Row click
            if (event.target.type !== 'checkbox') {
                $(this).find('td input[type=checkbox]').prop('checked', false);
                $(this).css('background', 'white');
                // Checkbox click
            } else {
                $(this).css('background', '#b8daff');
            }
        }
    });





});