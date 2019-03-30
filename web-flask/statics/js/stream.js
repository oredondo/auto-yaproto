var lastResponseLength = false;





function GetSteam() {
    $(document).ready(function() {
       refreshIntervalId = window.setInterval(function() {
            console.log("call");
            Stream(); //Pass Data Here...!!!
        }, 750); //Call every 1 min
    });
}

function Stream() {
    $.ajax({
            type: 'get',
            url: '/api/stream',
            dataType: 'text',
            success:  function(e)
                {
                    if(e==""){
                    clearInterval(refreshIntervalId);
                    }

                    $('#progressTest').append("<h4 >"+ e + "</h4>" );
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
