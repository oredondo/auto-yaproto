/* cytoscape js selector demo
moved to https://codepen.io/yeoupooh/pen/BjWvRa
 */



function callStyle(theResponse) {
    return $.ajax({
            url : "/api/style", // the endpoint
            type : "GET", // http method
            dataType: "json",
            // handle a non-successful response
            success: function( data ) {
                // Call this function on success
                return data;
            },
            error : function() {
               console.log("EROOR");
            }
      });
}

var style = callStyle();

$(function() {

  var win = $(window);

  win.resize(function() {
    resize();
  });

  function resize() {
    console.log(win.height(), win.innerHeight());
    $("#cy-container").height(win.innerHeight() - 130);
    cy.resize();
  }

  setTimeout(resize, 0);

  var nodeOptions = {
    normal: {
      bgColor: 'grey'
    },
    selected: {
      bgColor: 'yellow'
    }
  };

  var edgeOptions = {
    selected: {
      lineColor: 'yellow'
    }
  };


var toJson = function(res){ return res.json(); }



  var cy = window.cy = cytoscape({
    container: document.getElementById('cy'),

    minZoom: 0.1,
    maxZoom: 100,
    wheelSensitivity: 0.1,

    // panningEnabled: false,
    //boxSelectionEnabled: true,
    //autounselectify: false,
    //selectionType: 'additive',
    //autoungrabify: true,
    layout: {
      name: 'dagre'
    },

        style: style,

    elements: {
      //selectable: false,
      //grabbable: false,
      nodes: [{
        data: {
          id: '0',
          text: 'router ',
          type: 'rectangle'
        }
      }, {
        data: {
          id: '1',
          text: 'nodo1',
          type:  "ellipse"
        }
      }, {
        data: {
          id: '2',
          text: 'nodo2',
          type:  "ellipse"
        }
      }, {
        data: {
          id: '3',
          text: 'nodo3',
          type:  "ellipse"
        }
      }], // nodes
      edges: [{
          data: {
            color: '#000',
            source: '0',
            target: '1'
          }
        }, {
          data: {
            color: '#000',
            source: '1',
            target: '2'
          }
        }, {
          data: {
            color: '#000',
            source: '2',
            target: '3'
          }
        }, {
          data: {
            color: '#000',
            source: '0',
            target: '2'
          }
        }, {
          data: {
            color: '#000',
            source: '0',
            target: '3'
          }
        }, {
          data: {
            color: '#000',
            source: '0',
            target: '3'
          }
        }] // edges
    } // elements
  }); // cytoscape

  var selectedNodeHandler = function(evt) {
    //console.log(evt.data); // 'bar'

    $("#edge-operation").hide();
    $("#node-operation").show();

    var target = evt.cyTarget;
    console.log('select ' + target.id(), target);
    $("#selected").text("Selected:" + target.id());
  }

  var unselectedHandler = function(evt) {
    $("#edge-operation").hide();
    $("#node-operation").hide();
  }

  var selectedEdgeHandler = function(evt) {
    $("#edge-operation").show();
    $("#node-operation").hide();

    var target = evt.cyTarget;
    console.log('tapped ' + target.id(), target);
    $("#selected").text("Selected:" + target.id());
  }

  cy.on('select', 'node', selectedNodeHandler);
  cy.on('unselect', 'node', unselectedHandler);
  cy.on('select', 'edge', selectedEdgeHandler);
  cy.on('unselect', 'edge', unselectedHandler);

  // NOTE: Use selector(':selected') instead of event handler
  function addSelectHandler() {
    cy.on('select', 'node', function(evt) {
      console.log('select node:', evt.cyTarget);
      evt.cyTarget.animate({
        style: {
          'background-color': nodeOptions.selected.bgColor
        }
      }, {
        duration: 100
      });
    });
    cy.on('unselect', 'node', function(evt) {
      console.log('unselect node:', evt.cyTarget);
      evt.cyTarget.stop();
      evt.cyTarget.style({
        'background-color': nodeOptions.normal.bgColor
      });
    });
    cy.on('select', 'edge', function(evt) {
      console.log('select edge:', evt.cyTarget);
      evt.cyTarget.animate({
        style: {
          'line-color': edgeOptions.selected.lineColor
        }
      }, {
        duration: 100
      });
    });
    cy.on('unselect', 'edge', function(evt) {
      console.log('unselect edge:', evt.cyTarget);
      evt.cyTarget.stop();
      evt.cyTarget.style({
        'line-color': evt.cyTarget.data('color')
      });
    });
  }

  $("#fit").click(function() {
    console.log('cy=', cy);
    cy.fit();
  });

  $("#layout").click(function() {
    console.log('cy=', cy);
    cy.layout({
      name: 'dagre'
    });
  });

}); // ready