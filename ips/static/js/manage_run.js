/*
    Created by George Rushton 20/05/2019
    Handles the manage run page javascript
*/

$(document).ready(function(e){
    getStatus();
    window.setInterval(getStatus, 2000);
});

function getStatus(){
    const run_id = $('#run_id').text();
    $.ajax({
        type: "GET",
        url: '/manage_run/status/' + run_id,
        async:true,
        success: function (data) {
            data = JSON.parse(data);
            setUIStatus(data);
        }
    });
}

function setUIStatus(status){
    const steps = Object.keys(status['steps']);
    const main = $('#current_run_status');
    main.attr('class', 'status '+getStepStatusClass(status['status']));
    main.text(getStepText(status['status']));
    $('#progress').text(status['percentage_done']+"%");
    for (step of steps){
        const el = $('.status_column[step_num="'+step+'"]').children("em");
        el.attr('class', 'status status--small '+getStepStatusClass(status['steps'][step]));
        el.text(getStepText(status['steps'][step]));
    }
}

function getStepStatusClass(status){
    switch(status) {
        case '0':
            return 'status--info';
        case '1':
            return 'status--info';
        case '2':
            return 'status--info';
        case '3':
            return 'status--success';
        case '4':
            return 'status--error';
        case '5':
            return 'status--error';
        case '6':
            return 'status--error';
          default:
        // code block
    }
}

function getStepText(status){
    switch(status) {
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