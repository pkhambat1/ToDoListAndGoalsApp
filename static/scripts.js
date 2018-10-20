// Execute when the DOM is fully loaded
$(document).ready(function() {

    // Make entire rows clickable - ToDoList
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
                console.log("this below");
                console.log(this, "this");
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

    // Make entire rows clickable - Goals
    $(document).on('click', '.clickable_goals', function() {
        console.log("click");
        // If unchecked row is clicked
        if ($(this).find('td input[type=checkbox]').prop("checked") == false) {
            // Row click
            console.log(this, "this");
            if (event.target.type !== 'checkbox') {
                $(this).find('td input[type=checkbox]').prop('checked', true);
                $(this).css('background', '#c3e6cb');
                // Checkbox click
            } else {
                console.log("this below");
                console.log(this, "this");
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
                $(this).css('background', '#c3e6cb');
            }
        }
    });

    // Prevent duplicate submissions
    $('form').submit(function() {
        $(this).find(':submit').attr('disabled', 'disabled');
    });

    // On click of any of the generated checkboxes - ToDoList
    $('#mark_completed').click(function() {
        // Send list data to /checked
        if ($('form').serialize().length != 0) {
            $.ajax({
                type: "POST",
                url: "checked",
                data: $('form').serialize(),
                success: function(data) {
                    console.log(data, "data");
                    // Empty reminders list
                    $('#myTableId').empty();

                    // Table filler html
                    var rawhtml = "";

                    console.log(data.length);

                    if (data.length != 0) {
                        // Fill reminders list
                        $.each(data, function(i, item) {
                            rawhtml +=
                                '<tr class="clickable"><td class="checkbox" style="width: 10%;"><form action="/checked" method="post"><input type="checkbox" value="'
                                + data[i]['id'] + '" id="' + data[i]['id'] +
                                '" name="check_reminder"></form></td>';
                            rawhtml += '<td style="width: 30%;">' + data[i]['name'] + '</td>';
                            rawhtml += '<td style="width: 30%;">' + data[i]['details'] +
                                '</td>';
                            rawhtml += '<td style="width: 30%;">' + data[i]['datetime'] +
                                '</td>';
                        });
                    } else {
                        // Empty table message
                        rawhtml +=
                            '<tr><td colspan="4" align="center">You have no items on your checklist</td></tr>';
                    }

                    $('#myTableId').append(rawhtml);
                }
            });
        }
    });



    // On click of any of the generated checkboxes - Goals
    $('#mark_completed_goals').click(function() {
        // Send list data to /checked
        if ($('form').serialize().length != 0) {
            $.ajax({
                type: "POST",
                url: "checked_goal",
                data: $('form').serialize(),
                success: function(data) {
                    console.log(data, "data");
                    // Empty reminders list
                    $('#myTableId').empty();

                    // Table filler html
                    var rawhtml = "";

                    console.log(data.length);

                    if (data.length != 0) {
                        // Fill reminders list
                        $.each(data, function(i, item) {
                            rawhtml +=
                                '<tr class="clickable_goals"><td class="checkbox" style="width: 10%;"><form action="/checked" method="post"><input type="checkbox" value="'
                                + data[i]['id'] + '" id="' + data[i]['id'] +
                                '" name="check_goal"></form></td>';
                            rawhtml += '<td style="width: 30%;">' + data[i]['name'] + '</td>';
                            rawhtml += '<td style="width: 30%;">' + data[i]['details'] +
                                '</td>';
                            rawhtml += '<td style="width: 30%;">' + data[i]['datetime'] +
                                '</td>';
                        });
                    } else {
                        // Empty table message
                        rawhtml +=
                            '<tr><td colspan="4" align="center">You have no items on your goals</td></tr>';
                    }

                    $('#myTableId').append(rawhtml);
                }
            });
        }
    });


});