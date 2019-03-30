var lastResponseLength = false;

function GetSteam() {
    while (1) {
        $.ajax({
            type: 'get',
            url: '/api/stream',
            dataType: 'text',
            processData: false,
            xhrFields: {
                // Getting on progress streaming response
                onprogress: function(e)
                {
                    var progressResponse;
                    var response = e.currentTarget.response;

                    progressResponse = response;
                    lastResponseLength = response.length;
                    $('#progressTest').text(progressResponse);
                }
            }
        });
    }
}