$(function(){
    $('.run').click(function(){
        $(this).attr("disabled", true);
        let run_id = $(this).attr('run_id');
        $.ajax({
            type: "POST",
            url: '/manage_run/start/' + run_id,
            data: $("#tabs").serialize(),
            async: true,
            success: function (data) {
                setInterval(function(){ location.reload() }, 1000);
            },
            error: function (error) {
                console.log('got error: ' + error);
            }
        });
    });
});