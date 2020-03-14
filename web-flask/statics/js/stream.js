var lastResponseLength = false;





function GetSteam() {
    $(document).ready(function() {
        var refreshIntervalId = window.setInterval(function() {
            return Stream(); //Pass Data Here...!!!
        }, 25); //Call every 0.5 min


    });
}

function Stream() {
    $.ajax({
            type: 'get',
            url: '/api/stream',
            dataType: 'text',
            success:  function(e)
                {
                    if(e==''){
                        return clearInterval(refreshIntervalId);
                    }
                    else {
                        $('#progressTest').append("<p><kbd>" + e + "</kbd></p>");
                    }

                },
            error : function() {
               console.log("EROOR");
            }
        });
}

function sleep(milliseconds) {
  var start = new Date().getTime();
  for (var i = 0; i < 1e7; i++) {
    if ((new Date().getTime() - start) > milliseconds){
      break;
    }
  }
}
