$(document).ready(function() {

    // On click of clickable_lists (row)
    $('.clickable_lists').click(function() {

        // Bring back to normal color all lists
        $('.clickable_lists').children('td, th').css('background-color', '#e9ecef');

        // Link Table headers (lists) to checkboxes
        if ($(this).find('th input[type=radio]').prop("checked") == false) {
            $(this).find('th input[type=radio]').prop('checked', true);
            $(this).children('td, th').css('background-color', '#caccce');
        } else if ($(this).find('th input[type=radio]').prop("checked") == true) {
            $(this).find('th input[type=radio]').prop('checked', false);
            $(this).children('td, th').css('background-color', '#e9ecef');
        }

        var list_id = $(this).attr('id');

        $('.myItems').empty();

        // Send list data to /checked_list
        if ($('form').serialize().length != 0) {
            // Send list data to /checked
            $.ajax({
                type: "post",
                url: "lists",
                data: $('form').serialize(),
                success: function(data) {

                    // Table filler html
                    var rawhtml = '<table class="table">';
                    if (data.length != 0) {
                        // Fill reminders list
                        $.each(data, function(i, item) {
                            rawhtml += '<tr class="clickable">';
                            rawhtml += '<td class="checkbox">';
                            rawhtml += '<form id = "checked_item"';
                            rawhtml += ' method="post">';
                            rawhtml += '<input type="hidden" name="list_id" value="';
                            rawhtml += list_id + '">';
                            rawhtml += '<input type="checkbox" value="' + data[i]['id'];
                            rawhtml += '" id="' + data[i]['id'];
                            rawhtml += '" name="check_item"></form></td>';
                            rawhtml += '<td>' + data[i]['name'] + '</td>';
                            rawhtml += '<td>' + data[i]['details'] + '</td>';
                            rawhtml += '<td>' + data[i]['datetime'] + '</td>';
                            rawhtml += '</tr>';
                        });
                    } else {
                        // Empty table message
                        rawhtml +=
                            '<tr><td colspan="4" align="center">You have no items in this list</td></tr>';
                    }
                    rawhtml += '</table>';

                    $('#' + list_id + '.myItems').append(rawhtml);
                }
            });
        }
    });

    // On click of any of the generated checkboxes - ToDoList
    $('#mark_completed_items').click(function() {
    // Send list data to /checked
        $.ajax({
            type: "POST",
            url: "checked_item",
            data: $('form').serialize(),
            success: function(data) {
                // Empty reminders list
                $('.myItems').empty();
                var list_id = $(':radio:checked').closest('tr').attr('id');
                // Table filler html
                var rawhtml = '<table class="table">';
                if (data.length != 0) {
                    // Fill reminders list
                    $.each(data, function(i, item) {
                        rawhtml += '<tr class="clickable" align="left">';
                        rawhtml += '<td class="checkbox">';
                        rawhtml += '<form id = "checked_item"';
                        rawhtml += ' method="post">';
                        rawhtml += '<input type="hidden" name="list_id" value="';
                        rawhtml += list_id + '">';
                        rawhtml += '<input type="checkbox" value="' + data[i]['id'];
                        rawhtml += '" id="' + data[i]['id'];
                        rawhtml += '" name="check_item"></form></td>';
                        rawhtml += '<td>' + data[i]['name'] + '</td>';
                        rawhtml += '<td>' + data[i]['details'] + '</td>';
                        rawhtml += '<td>' + data[i]['datetime'] + '</td>';
                        rawhtml += '</tr>';
                    });
                } else {
                    // Empty table message
                    rawhtml +=
                        '<tr><td colspan="4" align="center">You have no items in this list</td></tr>';
                }
                rawhtml += '</table>';

                $('#' + list_id + '.myItems').append(rawhtml);
            }
        });
    });


    // Delete items
    $('#delete_item').click(function() {
        $.ajax({
            type: "POST",
            url: "delete_item",
            data: $('form').serialize(),
            success: function(data) {
                // Empty reminders list
                $('.myItems').empty();
                var list_id = $(':radio:checked').closest('tr').attr('id');
                // Table filler html
                var rawhtml = '<table class="table">';
                if (data.length != 0) {
                    // Fill reminders list
                    $.each(data, function(i, item) {
                        rawhtml += '<tr class="clickable" align="left">';
                        rawhtml += '<td class="checkbox">'
                        rawhtml += '<form id = "checked_item"';
                        rawhtml += ' method="post">';
                        rawhtml += '<input type="hidden" name="list_id" value="';
                        rawhtml += list_id + '">';
                        rawhtml += '<input type="checkbox" value="' + data[i]['id'];
                        rawhtml += '" id="' + data[i]['id'];
                        rawhtml += '" name="check_item"></form></td>';
                        rawhtml += '<td>' + data[i]['name'] + '</td>';
                        rawhtml += '<td>' + data[i]['details'] + '</td>';
                        rawhtml += '<td>' + data[i]['datetime'] + '</td>';
                        rawhtml += '</tr>';
                    });
                } else {
                    // Empty table message
                    rawhtml +=
                        '<tr><td colspan="4" align="center">You have no items in this list</td></tr>';
                }
                rawhtml += '</table>';

                $('#' + list_id + '.myItems').append(rawhtml);
            }
        });
    });
});