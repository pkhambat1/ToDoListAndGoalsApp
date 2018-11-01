$(document).ready(function() {


    // Mark complete
    $('#mark_completed').click(function() {
        // Send list data to /checked
        if ($('form').serialize().length != 0) {
            $.ajax({
                type: "POST",
                url: "checked",
                data: $('form').serialize(),
                success: function(data) {
                    // Empty reminders list
                    $('#myTableId').empty();

                    // Table filler html
                    var rawhtml = "";

                    if (data.length != 0) {
                        // Fill reminders list
                        $.each(data, function(i, item) {
                            rawhtml += '<tr class="clickable"><td class="checkbox">';
                            rawhtml += '<form action="/checked" method="post">';
                            rawhtml += '<input type="checkbox" value="' + data[i]['id'];
                            rawhtml += '" id="' + data[i]['id']
                            rawhtml += '" name="check_reminder"></form></td>';
                            rawhtml += '<td>' + data[i]['name'] + '</td>';
                            rawhtml += '<td>' + data[i]['datetime'] + '</td>';
                            rawhtml += '<tr>';
                        });
                    } else {
                        // Empty table message
                        rawhtml +=
                            '<tr><td colspan="3">You have no items on your ToDo list. <a id="link_add_todo" href="#reminder">Add</a> some?</td></tr>';
                    }

                    $('#myTableId').append(rawhtml);
                }
            });
        }
    });


    // Delete
    $('#delete').click(function() {
        if ($('form').serialize().length != 0) {
            $.ajax({
                type: "POST",
                url: "delete",
                data: $('form').serialize(),
                success: function(data) {
                    // Empty reminders list
                    $('#myTableId').empty();

                    // Table filler html
                    var rawhtml = "";

                    if (data.length != 0) {
                        // Fill reminders list
                        $.each(data, function(i, item) {
                            rawhtml += '<tr class="clickable"><td class="checkbox">';
                            rawhtml += '<form action="/checked" method="post">';
                            rawhtml += '<input type="checkbox" value="' + data[i]['id'];
                            rawhtml += '" id="' + data[i]['id'];
                            rawhtml += '" name="check_reminder"></form></td>';
                            rawhtml += '<td>' + data[i]['name'] + '</td>';
                            rawhtml += '<td>' + data[i]['datetime'] + '</td>';
                            rawhtml += '<tr>';
                        });
                    } else {
                        // Empty table message
                        rawhtml +=
                            '<tr><td colspan="3">You have no items on your ToDo list. <a id="link_add_todo" href="#reminder">Add</a> some?</td></tr>';
                    }

                    $('#myTableId').append(rawhtml);
                }
            });
        }
    });

    // Link to focus into new ToDo box
    $(document).on('click', '#link_add_todo', function(e) {
        e.preventDefault();
        $("#reminder").focus();
    });


});