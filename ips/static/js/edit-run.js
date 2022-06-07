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

    function storeAllAndVerifyPVs() {
        // Get UI elements
        let pv_validation_panel_success_1 = $('#pv-validation-panel-success-1');
        let pv_validation_panel_success_2 = $('#pv-validation-panel-success-2');
        let pv_validation_panel_error = $('#pv-validation-panel-error');
        let pv_validation_panel_loading = $('#pv-validation-panel-loading');
        let error_panel_placeholder = $('#error-panel-placeholder');
        pv_validation_panel_loading.show();
        pv_validation_panel_success_1.hide();
        pv_validation_panel_success_2.hide();
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
                if (response.status === "successful") {
                    // Shows success panel
                    $('#btn-continue').show();
                    error_panel_placeholder.empty();
                    pv_validation_panel_success_1.show();
                    pv_validation_panel_success_2.show();
                    pv_validation_panel_error.hide();
                    pv_validation_panel_loading.hide();
                    // Clear any Errors from Table List
                    $("tr").removeClass("panel--error");
                } else if (response.status === "error") {
                    // Clear any Errors from Table List
                    $("tr").removeClass("panel--error");
                    // Hides Continue button and
                    $('#btn-continue').hide();
                    pv_validation_panel_success_1.hide();
                    pv_validation_panel_success_2.hide();
                    pv_validation_panel_error.show();
                    pv_validation_panel_loading.hide();
                    // Clear Panel Error and Displays new error
                    error_panel_placeholder.empty();
                    error_panel_placeholder.append('' +
                        '<div class="panel panel--error">\n' +
                        '  <div class="panel__header">\n' +
                        '    <h1 class="panel__title u-fs-r--b">Error</h1>\n' +
                        '  </div>\n' +
                        '  <div class="panel__body">\n' +
                        '    <em>Error Validating PV:  <a href="#' + response.PV + '">' + response.PV + '</a></em>\n' +
                        '    <p>' + response.errorMessage + '</p>\n' +
                        '  </div>\n' +
                        '</div>');
                    window.scrollTo(0,0);
                    $("tr:contains(" + response.PV + ")").addClass("panel--error")
                }
            },
            error: function (err) {
                console.log("Builder & Validation Call Error");
                console.log(err)
            }
        });
    }
});
