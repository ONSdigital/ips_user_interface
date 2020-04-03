/*
    Created by George Rushton 20/05/2019
    Handles the manage run page javascript
*/

$(document).ready(function (e) {
    $('.modal').height(screen.height);
    getStatus();
    window.setInterval(getStatus, 2000);
});

function getStatus() {
    const run_id = $('#run_id').text();
    $.ajax({
        type: "GET",
        url: '/manage_run/status/' + run_id,
        async: true,
        success: function (data) {
            data = JSON.parse(data);
            setUIStatus(data);
        }
    });
}

function setUIStatus(status) {
    const run_id = $('#run_id').text();
    let steps = [];
    if(status['steps'] !== undefined) {
        steps = Object.keys(status['steps']);
    }
    const main = $('#current_run_status');
    setMainStatus(status, main, run_id);
    $('#progress').text((status['percentage_done'] === undefined ? "0" : status['percentage_done'])+"%");
    cancelButton(status['status'], steps, status['steps']);
    exportButton(status['status']);
    for (step of steps) {
        const td = $('.status_column[step_num="' + step + '"]');
        const tr = td.parent();
        const el = td.children("em");
        el.attr('class', 'status status--small ' + getStepStatusClass(status['steps'][step]['Status']));
        el.text(getStepText(status['steps'][step]['Status']));

        const info_column = $('.info_column[step_num="' + step + '"]');

        if (status['steps'][step].hasOwnProperty('Responses')) {
            const reports = $('#myModal' + step).find(".reports");
            reports.empty();
            setReports(tr, info_column, step, reports, status['steps'][step]['Responses']);
        } else {
            noReports(tr, info_column);
        }
    }
}

function setReports(tr, td, step_num, reports, response_data) {
    const responses = Object.keys(response_data);
    if (!td.children('a').length) {
        td.append("<a class='info_img'>Information</a>");
    }
    for (response of responses) {
        appendToReport(reports, response_data[response]);
    }
    tr.attr("data-toggle", "modal");
    tr.attr("data-target", "#myModal" + step_num);
    tr.css('cursor', 'pointer');
}

function noReports(tr, td) {
    td.find('a').remove();
    tr.removeAttr("data-toggle");
    tr.removeAttr("data-target");
    tr.css('cursor', 'default');
}

function appendToReport(report, response) {
    report.append('<tr style="line-height: 0px"><td class="report_td">' + getReportStatus(response['RESPONSE_CODE']) + ':</td><td class="report_td">' + response['MESSAGE'] + '</td></tr>');
}

function getStepStatusClass(status) {
    switch (status) {
        case '0':
            return 'status--info';
        case '1':
            return 'status--info';
        case '2':
            return 'status--info';
        case '3':
            return 'status--success';
        case '4':
            return 'status--dead';
        case '5':
            return 'status--error';
        case '6':
            return 'status--error';
        default:
        // code block
    }
}

function getStepText(status) {
    switch (status) {
        case '0':
            return 'Ready';
        case '1':
            return 'Ready';
        case '2':
            return 'Running';
        case '3':
            return 'Completed';
        case '4':
            return 'Cancelled';
        case '5':
            return 'Invalid';
        case '6':
            return 'Failed';
        default:
        // code block
    }
}

function getReportStatus(status) {
    status = status.toString();
    switch (status) {
        case '0':
            return 'Ready';
        case '1':
            return 'SUCCESS';
        case '2':
            return 'WARNING';
        case '3':
            return 'ERROR';
    }
}

function setMainStatus(status, main, run_id){
    statusNum = status['status'];
    main.attr('class', (getStepStatusClass(status['status']) === undefined ? "status status--info" : 'status ' + getStepStatusClass(status['status'])));
    main.text(getStepText(status['status']));
}

function cancelButton(status, steps, stepsArr) {
    var ready = true;
    for (step of steps) {
        if(stepsArr[step]['Status'] == 2){
            ready = false;
        }
    }
    if (status == "2") {
        ready = false;
    }
    if(ready){
        $("#run_button").attr("class", 'btn btn--loader');
        $("#run_button").attr("disabled", false);
        $("#cancel_button").hide();
        $("#edit_button").show();
    } 
    if (status == "2") {
        $("#cancel_button").show();
        $("#run_button").attr("disabled", true);
        $("#edit_button").hide();
        $("#run_button").attr("class", 'btn btn--loader is-loading');
    }
}

function exportButton(status){
    if(status in [0,1,2]){
        $("#export_button").hide();
    }else{
        $("#export_button").show();
    }
}