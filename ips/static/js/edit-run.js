/*
    Created by Jack Allcock 21/06/2018
    This javascript file handles the edit PV's modal
*/


$(document).ready(function (e) {

    const grb_id = 1;
    let expr = [];
    let data = [];
    storeAllAndVerifyPVs();

    $("#modal_okay_button").click(function (event) {
        // Get values entered into the inputs by the user
        let pv = $("#builder").txt_val();
        $(".pv_error").removeClass("pv_error");
        $.ajax({
            type: "POST",
            url: '/builder/validate',
            data: {pv: pv},
            async: false,
            statusCode: {
                406: function(data, message) {
                  let line = data.responseText-1;
                  let el = $("#builder").children(".pv_div").children(".pv_line").eq(line);
                  el.addClass("pv_error");
                  el.focus();
                },
                200: function(data) {
                    console.log(data);
                    fillInputFieldForPosting(rowsLength);
                    saveBuildToUI(pv, $("#id_input").attr("pv"));
                    // Fade out 500ms
                    modal.fadeOut(500);
                }
            }
        });
        storeAllAndVerifyPVs();
    });

    $("#savec").click(function () {
        storeAllAndVerifyPVs()
    });

    $("#btn-continue").click(function () {
        storeAllAndVerifyPVs()
    });

    function storeAllAndVerifyPVs() {
        // Get UI elements
        let pv_validation_panel_success = $('#pv-validation-panel-success');
        let pv_validation_panel_error = $('#pv-validation-panel-error');
        let pv_validation_panel_loading = $('#pv-validation-panel-loading');
        let error_panel_placeholder = $('#error-panel-placeholder');
        pv_validation_panel_loading.show();
        pv_validation_panel_success.hide();
        pv_validation_panel_error.hide();

        let json = {};

        $("#form_table").children("tbody").children("tr").each(function () {
            const pvid = $(this).attr("index");
            json[pvid] = {};
            pv_code = $(this).children(".pv_def").text();
            pv_name = $(this).children().eq(0).text();
            pv_desc = $(this).children().eq(1).text();
            json[pvid]['pv'] = pv_code.trim();
            json[pvid]['pv_name'] = pv_name;
            json[pvid]['pv_desc'] = pv_desc;
        });
        json = JSON.stringify(json);
        $.ajax({
            type: "POST",
            url: '/builder/' + $("#rid").text(),
            data: {json: json},
            success: function(response){
                console.log(response)
                if (response.status === "successful") {
                    // Shows success panel
                    $('#btn-continue').show();
                    error_panel_placeholder.empty();
                    pv_validation_panel_success.show();
                    pv_validation_panel_error.hide();
                    pv_validation_panel_loading.hide();
                } else {
                    // Hides Continue button and Displays error Panel
                    $('#btn-continue').hide();
                    pv_validation_panel_success.hide();
                    pv_validation_panel_error.show();
                    pv_validation_panel_loading.hide();
                    error_panel_placeholder.empty();
                    error_panel_placeholder.append('' +
                        '<div id="error-panel">\n' +
                        '    <div class="panel panel--error">\n' +
                        '        <div class="panel__header">\n' +
                        '            <div class="u-fs-r--b">Error</div>\n' +
                        '        </div>\n' +
                        '        <div class="panel__body">\n' +
                        '            <p class="u-fs-r">Error Validating PVs: ' + response.error + '</p>\n' +
                        '        </div>\n' +
                        '    </div>' +
                        '</div>');
                    window.scrollTo(0,0);
                }
            },
            error: function (err) {
                console.log("Builder & Validation Call Error");
                console.log(err)
            }
        });
    }

    function saveBuildToUI(pv, pv_id) {
        $("#pv_"+pv_id).children(".pv_def").first().html(pv);
        console.log($("#pv_"+pv_id));
        console.log($("#pv_"+pv_id).children(".pv_def").first());
    }


    // allows object to call hasOwnProperty function
    if (Object.prototype.hasOwnProperty) {
        var hasOwnProperty = function (obj, prop) {
            return obj.hasOwnProperty(prop);
        }
    }
    // Create dictionary of all the table cell rows
    var tableRows = [];
    $("#form_table > tbody  > tr").each(function () {
        var row = {
            "name": $(this).find(".table--cell")[0],
            "reason": $(this).find(".table--cell")[1],
            "content": $(this).find(".table--cell")[2],
        };
        tableRows.push(row);
    });

    // Get length of dictionary so it can be iterated over
    rowsLength = tableRows.length;

    // Take the contents of the table and put it into the hidden field
    fillInputFieldForPosting(rowsLength);

    // Get the modal so that we can hide/un-hide and attach the ID
    var modal = $(".modal");

    // On the click of the Modal Close button, hide the modal and refresh the page.
    $(".close").click(function (event) {
        // Fade out 500ms
        modal.fadeOut(500);
    });

    $("#cancel").click(function (event) {
        // Fade out 500ms
        modal.fadeOut(500);
    });

    // When the edit button is clicked, get the ID from the button attribute
    // Show the modal and change the input fields value to the ID
    $(".pv-edit-button").click(function (event) {

        pvid = parseInt($(this).attr("pvid"));
        // Fade in 500ms
        modal.fadeIn(500);

        variableId = this.id;

        // Length of the rows in the table
        rowsLength = tableRows.length;
        // Array we will append rows to
        data = [];

        /** First we need to go through the table data and find the row we need.
         Then we can set the modal inputs with data from that table row and update the actual table data when the
         okay button is clicked
         **/

        // Iterate over dictionary of table rows
        for (i = 0; i < rowsLength; i++) {
            // Get dictionary out of array by index
            row = tableRows[i];
            // Get the PV Name text
            name = row['name'].innerHTML;

            // If the dictionary is the one we need add the data to the array
            if (name === variableId) {
                data.push(row['name']);
                data.push(row['reason']);
                data.push(row['content']);
            }
        }

        // Set the inputs values to that in the data array
        $("#id_input").attr("pv", pvid);
        $("#id_input").val(data[0].innerHTML);
        $("#reason_input").val(data[1].innerHTML);

        // initiate the builder
        $("#builder").pv_builder_v2(data[2].innerText);

        // Edit table data when the okay button is pressed


        // Make sure the page doesn't refresh/change when this button is clicked
        return false;
    });

    function fillInputFieldForPosting(rowsLength) {
        // Fill hidden input with all table data as a comma separated string
        data = [];
        for (i = 0; i < rowsLength; i++) {
            // Get row from dictionary
            row = tableRows[i];

            // Get the data from row
            name = row['name'].innerHTML;
            reason = row['reason'].innerHTML;
            content = row['content'].innerHTML;

            // Create a dictionary entry to put in the input
            var row = {
                name: name,
                "reason": reason,
                "content": content,
            };

            // Add to the data array
            data.push(row);
        }

        // Iterate over data array and add the data as a comma separated list in the input
        dataLength = data.length;
        dataToSend = "";
        // Put the data array into the input
        for (i = 0; i < dataLength; i++) {
            row = data[i];
            dataToSend += row['name'] + '^';
            dataToSend += row['reason'] + '^';
            dataToSend += row['content'] + '^';
        }
        $(".hidden-edit-input-content").val(dataToSend);

    }
});
