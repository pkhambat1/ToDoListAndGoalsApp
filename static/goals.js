$(document).ready(function() {

    // On click of any of the generated checkboxes - Goals
    $('#mark_completed_goals').click(function() {
        // Send list data to /checked
        if ($('form').serialize().length != 0) {
            $.ajax({
                type: "POST",
                url: "checked_goal",
                data: $('form').serialize(),
                success: function(data) {
                    // Empty reminders list
                    $('#myTableId').empty();

                    // Table filler html
                    var rawhtml = "";

                    if (data.length != 0) {
                        // Fill reminders list
                        $.each(data, function(i, item) {
                            rawhtml +=
                                '<tr class="clickable"><td class="checkbox"><form action="/checked" method="post"><input type="checkbox" value="'
                                + data[i]['id'] + '" id="' + data[i]['id'] +
                                '" name="check_goal"></form></td>';
                            rawhtml += '<td>' + data[i]['name'] + '</td>';
                            rawhtml += '<td>' + data[i]['details'] +
                                '</td>';
                            rawhtml += '<td>' + data[i]['datetime'] +
                                '</td>';
                            rawhtml += '</tr>';
                        });
                    } else {
                        // Empty table message
                        rawhtml +=
                            '<tr><td colspan="4">You have no items on your Goals list. <a href="/new_goal">Add</a> some?</td></tr>';
                    }

                    $('#myTableId').append(rawhtml);
                }
            });
        }
    });

    // Delete Goals

    // Delete
    $('#delete_goal').click(function() {
        if ($('form').serialize().length != 0) {
            $.ajax({
                type: "POST",
                url: "delete_goal",
                data: $('form').serialize(),
                success: function(data) {
                    // Empty reminders list
                    $('#myTableId').empty();

                    // Table filler html
                    var rawhtml = "";

                    if (data.length != 0) {
                        // Fill reminders list
                        $.each(data, function(i, item) {
                            rawhtml +=
                                '<tr class="clickable"><td class="checkbox"><form action="/checked" method="post"><input type="checkbox" value="'
                                + data[i]['id'] + '" id="' + data[i]['id'] +
                                '" name="check_goal"></form></td>';
                            rawhtml += '<td>' + data[i]['name'] + '</td>';
                            rawhtml += '<td>' + data[i]['details'] +
                                '</td>';
                            rawhtml += '<td>' + data[i]['datetime'] +
                                '</td>';
                            rawhtml += '</tr>';
                        });
                    } else {
                        // Empty table message
                        rawhtml +=
                            '<tr><td colspan="4">You have no items on your Goals list. <a href="/new_goal">Add</a> some?</td></tr>';
                    }

                    $('#myTableId').append(rawhtml);
                }
            });
        }
    });
});


