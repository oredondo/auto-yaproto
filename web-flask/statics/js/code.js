/* cytoscape js selector demo
moved to https://codepen.io/yeoupooh/pen/BjWvRa
 */


function callStyle(theResponse) {
    return $.ajax({
        url: "/api/style", // the endpoint
        type: "GET", // http method
        dataType: "json",
        // handle a non-successful response
        success: function (data) {
            // Call this function on success
            return data;
        },
        error: function () {
            console.log("ERROR");
        }
    });
}

var deploy = false;
var runripvar = false;
var style = callStyle();
var ips = {};

function callElements(theResponse) {
    return $.ajax({
        url: "/api/elements", // the endpoint
        type: "GET", // http method
        dataType: "json",
        // handle a non-successful response
        success: function (data) {
            // Call this function on success
            return data;
        },
        error: function () {
            console.log("ERROR");
        }
    });
}

var elements = callElements();


$(function () {

    var win = $(window);

    win.resize(function () {
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

    var cy = window.cy = cytoscape({
        container: document.getElementById('cy'),

        minZoom: 0.1,
        maxZoom: 100,
        wheelSensitivity: 0.1,
        layout: {
            name: 'dagre'
        },
        style: style,
        elements: elements // elements
    }); // cytoscape


    var selectedNodeHandler = function (evt) {
        //console.log(evt.data); // 'bar'

        $("#edge-operation").hide();
        $("#node-operation").show();

        var target = evt.cyTarget;
        if (target["_private"]["data"]["color"] == "grey" && deploy) {
            window.open("https://127.0.0.1:" + target["_private"]["data"]["port"]);
        }
        console.log('select ' + target.id(), target);
        $("#selected").text("Selected:" + target.id());
    }

    var unselectedHandler = function (evt) {
        $("#edge-operation").hide();
        $("#node-operation").hide();
    }

    var selectedEdgeHandler = function (evt) {
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
        cy.on('select', 'node', function (evt) {
            console.log('select node:', evt.cyTarget);
            evt.cyTarget.animate({
                style: {
                    'background-color': nodeOptions.selected.bgColor
                }
            }, {
                duration: 100
            });
        });
        cy.on('unselect', 'node', function (evt) {
            console.log('unselect node:', evt.cyTarget);
            evt.cyTarget.stop();
            evt.cyTarget.style({
                'background-color': nodeOptions.normal.bgColor
            });
        });
        cy.on('select', 'edge', function (evt) {
            console.log('select edge:', evt.cyTarget);
            evt.cyTarget.animate({
                style: {
                    'line-color': edgeOptions.selected.lineColor
                }
            }, {
                duration: 100
            });
        });
        cy.on('unselect', 'edge', function (evt) {
            console.log('unselect edge:', evt.cyTarget);
            evt.cyTarget.stop();
            evt.cyTarget.style({
                'line-color': evt.cyTarget.data('color')
            });
        });
    }



    $(document).ready(function () {
        $("#addNode").click(function () {
            var name = $('#name').val();
            var net = $('#net').val();
            var dict = cy.json();
            dict["name"] = name;
            dict["net"] = net;
            console.log(dict);
            $.ajax({
                url: "/api/node", // the endpoint
                type: "PUT", // http method
                data: JSON.stringify(dict),
                contentType: "application/json",
                dataType: 'json',
                // handle a non-successful response
                success: function (data) {
                    // Call this function on success
                    cy.add(data);
                    return data;
                },
                error: function () {
                    console.log("ERROR");
                    console.log(data)
                }
            });
        });
    });

    $(document).ready(function () {
        $("#deleteNode").click(function () {
            var name = $('#name').val();
            var dict = cy.json();
            dict["name"] = name;
            console.log(dict);
            $.ajax({
                url: "/api/node", // the endpoint
                type: "DELETE", // http method
                data: JSON.stringify(dict),
                contentType: "application/json",
                dataType: 'json',
                // handle a non-successful response
                success: function (data) {
                    // Call this function on success
                    jQuery.each(data, function (key, value) {
                        var del = cy.getElementById(value);
                        cy.remove(del);
                        return data;
                    });
                },
                error: function () {
                    console.log("ERROR");
                    console.log(data)
                }
            });
        });
    });

    $(document).ready(function () {
        $("#deleteEdge").click(function () {
            var net_edge = $('#net_edge').val();
            var router = $('#router').val();
            var dict = cy.json();
            dict["net_edge"] = net_edge;
            dict["router"] = router;
            console.log(dict);
            $.ajax({
                url: "/api/edge", // the endpoint
                type: "DELETE", // http method
                data: JSON.stringify(dict),
                contentType: "application/json",
                dataType: 'json',
                // handle a non-successful response
                success: function (data) {
                    // Call this function on success
                    var del = cy.getElementById(data);
                    cy.remove(del);
                    return data;
                },
                error: function () {
                    console.log("ERROR");
                    console.log(data)
                }
            });
        });
    });


    $(document).ready(function () {
        $("#addEdge").click(function () {
            var net_edge = $('#net_edge').val();
            var router = $('#router').val();
            var dict = cy.json();
            dict["net_edge"] = net_edge;
            dict["router"] = router;
            console.log(dict);
            $.ajax({
                url: "/api/edge", // the endpoint
                type: "PUT", // http method
                data: JSON.stringify(dict),
                contentType: "application/json",
                dataType: 'json',
                // handle a non-successful response
                success: function (data) {
                    // Call this function on success
                    cy.add(data);
                    return data;
                },
                error: function () {
                    console.log("ERROR");
                    console.log(data)
                }
            });
        });
    });


    $(document).ready(function () {
        $("#deleteRouter").click(function () {
            var name = $('#nameRouter').val();
            var dict = cy.json();
            dict["name"] = name;
            console.log(dict);
            $.ajax({
                url: "/api/router", // the endpoint
                type: "DELETE", // http method
                data: JSON.stringify(dict),
                contentType: "application/json",
                dataType: 'json',
                // handle a non-successful response
                success: function (data) {
                    // Call this function on success
                    jQuery.each(data, function (key, value) {
                        var del = cy.getElementById(value);
                        cy.remove(del);
                        return data;
                    });
                },
                error: function () {
                    console.log("ERROR");
                    console.log(data)
                }
            });
        });
    });


    $(document).ready(function () {
        $("#addRouter").click(function () {
            var name = $('#nameRouter').val();
            var dict = cy.json();
            dict["name"] = name;
            console.log(dict);
            $.ajax({
                url: "/api/router", // the endpoint
                type: "PUT", // http method
                data: JSON.stringify(dict),
                contentType: "application/json",
                dataType: 'json',
                // handle a non-successful response
                success: function (data) {
                    // Call this function on success
                    cy.add(data);
                    return data;
                },
                error: function () {
                    console.log("ERROR");
                    console.log(data)
                }
            });
        });
    });

    /// DEPLOY
    $(document).ready(function () {
        $("#deploy").click(function () {
            cy.nodes().forEach(function( ele ) {
                    if (ele.data("color") == "grey") {
                        let node = ele;
                        let popper = ele.popper({
                            content: () => {
                                let div = document.createElement('div');
                                div.setAttribute("id", "IP" + ele.id());
                                document.body.appendChild(div);
                                return div;
                            }
                        });
                        let update = () => {
                            popper.scheduleUpdate();
                        };
                        node.on('position', update);
                        cy.on('pan zoom resize', update);
                    }
            });

            var dict = cy.json();
            console.log(dict);
            var last_response_len = false;
            $('#progressTest').html("<p></p>");
            $.ajax({
                url: "/api/getips", // the endpoint
                type: "PUT", // http method
                data: JSON.stringify(dict),
                contentType: "application/json",
                dataType: 'json',
                // handle a non-successful response
                success: function (data) {
                    // Call this function on success
                    ips = data;
                },
                error: function () {
                    console.log("ERROR");
                }
            });
            $.ajax({
                url: "/api/infonet", // the endpoint
                type: "PUT", // http method
                data: JSON.stringify(dict),
                contentType: "application/json",
                dataType: 'json',
                // handle a non-successful response
                success: function (data) {
                    // Call this function on success
                    jQuery.each(data["nodes"], function (key, value) {
                        $('#IP'+ key).append('<p></p>')
                        $('#IP'+ key).append('<p><span style="color:#0040ff;">'+ 'Ip: ' + value[0]["ip"] + '</span></p>')
                        $('#IP'+ key).append('<div id="ESTADO'+ key +'"></div>')
                    });
                    jQuery.each(data["routers"], function (key, value) {
                        $('#IP'+ key).append('<p></p>')
                        jQuery.each(value, function (key2, value2) {
                            $('#IP'+ key).append('<p><span style="color:#0040ff;">'+ 'Ip: ' + value2["ip"] + '</span></p>')
                        });
                        $('#IP'+ key).append('<div id="ESTADO'+ key +'"></div>')
                    });
                },
                error: function () {
                    console.log("ERROR");
                }
            });
            $.ajax({
                url: "/api/deploy", // the endpoint
                type: "PUT", // http method
                data: JSON.stringify(dict),
                contentType: "application/json",
                dataType: 'text',
                xhrFields: {
                    onprogress: function (e) {
                        var this_response, response = e.currentTarget.response;
                        if (last_response_len === false) {
                            this_response = response;
                            last_response_len = response.length;
                        } else {
                            this_response = response.substring(last_response_len);
                            last_response_len = response.length;
                        }
                        deploy = true;
                        $('#progressTest').append(this_response);
                        $('body,html,div').animate({ scrollTop: $('#progressTest').height()}, 800);
                    }
                }
            });


        });
    });

    $(document).ready(function () {
        $("#destroy").click(function () {
            var dict = cy.json();
            console.log(dict);
            var last_response_len = false;
            $('#progressTestDestroy').html("<p></p>");
            $.ajax({
                url: "/api/destroy", // the endpoint
                type: "PUT", // http method
                data: JSON.stringify(dict),
                contentType: "application/json",
                dataType: 'text',
                xhrFields: {
                    onprogress: function (e) {
                        var this_response, response = e.currentTarget.response;
                        if (last_response_len === false) {
                            this_response = response;
                            last_response_len = response.length;
                        } else {
                            this_response = response.substring(last_response_len);
                            last_response_len = response.length;
                        }
                        $('#progressTestDestroy').append(this_response);

                    }
                }
            });
        });
    });
$("html, body").animate({ scrollTop: $(document).height() }, 1000);



// #####RUN RIP##########
    $(document).ready(function () {
        $("#checkNames").click(function () {
            var dict = cy.json();
             $('#ripDiv').empty();
            for (item in dict.elements.nodes) {
                if (dict.elements.nodes[item].data.color == "grey") {
                    ripName = dict.elements.nodes[item].data.id;
                    $('#ripDiv').append("<input type='checkbox' id=" + ripName + " name=" + ripName + " value=" + ripName + ">" +
                        "<label for=" + ripName + "> " + ripName + "</label><br>");
                }
            };
        });
    });
    $(document).ready(function () {
        $("#runRip").click(function () {
            // cy.nodes().forEach(function( ele ) {
            //         if (ele.data("color") == "grey") {
            //             let node = ele;
            //             let popper = ele.popper({
            //                 content: () => {
            //                     let div = document.createElement('div');
            //                     div.setAttribute("id", "ESTADO" + ele.id());
            //                     document.body.appendChild(div);
            //                     return div;
            //                 }
            //             });
            //             let update = () => {
            //                 popper.scheduleUpdate();
            //             };
            //             node.on('position', update);
            //             cy.on('pan zoom resize', update);
            //         }
            // });
            var dict = cy.json();
            var selected = [];
            var topic = $('#topic').val();
            if(topic == ""){
                topic = "all";
            }
            $('div#ripDiv input[type=checkbox]').each(function() {
               if ($(this).is(":checked")) {
                   selected.push($(this).attr('name'));
               }
            });
            for (item in dict.elements.nodes) {
                if (dict.elements.nodes[item].data.color == "grey") {
                    ripName = dict.elements.nodes[item].data.id;
                    port = dict.elements.nodes[item].data.port_mosquitto;
                    if ($.inArray( ripName, selected ) != -1){
                        var w = window.open('/logrip&'+ripName+'&'+port +'&'+topic);
                    }
                    if (runripvar == false){
                        $.ajax({
                            url: "/api/runrip", // the endpoint
                            type: "PUT", // http method
                            data: JSON.stringify({name: ripName,
                                                        port: port}),
                            contentType: "application/json"
                        });
                    }
                }
            }

            runripvar = true


            for (item in dict.elements.nodes) {
                if (dict.elements.nodes[item].data.color == "grey") {
                    ripName = dict.elements.nodes[item].data.id;
                    port = dict.elements.nodes[item].data.port_mosquitto;
                executeAsync(CallEstado(ripName, port));

                }
            }


        });
    });
    function executeAsync(func) {
        setTimeout(func, 0);
    }
    function CallEstado(ripName, port) {
        var last_response_len = false;
        $.ajax({
            url: "/api/mqttrip", // the endpoint
            type: "PUT", // http method
            data: JSON.stringify({
                name: ripName,
                port: port,
                mapa: true,
                topic: "ESTADO"
            }),
            contentType: "application/json",
            dataType: 'text',
            xhrFields: {
                onprogress: function (e) {
                    var this_response, response = e.currentTarget.response;
                    if (last_response_len === false) {
                        this_response = response;
                        last_response_len = response.length;
                    } else {
                        this_response = response.substring(last_response_len);
                        last_response_len = response.length;
                        $('#ESTADO' + ripName).empty();
                    }
                    $('#ESTADO' + ripName).append('<p></p>' + this_response);

                }
            }
        });
    }

    // #####RUN OSPF##########
    $(document).ready(function () {
        $("#checkNamesOspf").click(function () {
            var dict = cy.json();
             $('#ospfDiv').empty();
            for (item in dict.elements.nodes) {
                if (dict.elements.nodes[item].data.color == "grey") {
                    ospfName = dict.elements.nodes[item].data.id;
                    $('#ospfDiv').append("<input type='checkbox' id=" + ospfName + " name=" + ospfName + " value=" + ospfName + ">" +
                        "<label for=" + ospfName + "> " + ospfName + "</label><br>");
                }
            };
        });
    });
    $(document).ready(function () {
        $("#runOspf").click(function () {
            var dict = cy.json();
            var selected = [];
            var last_response_len = false;
            $('div#ospfDiv input[type=checkbox]').each(function() {
               if ($(this).is(":checked")) {
                   selected.push($(this).attr('name'));
               }
            });
            for (item in dict.elements.nodes) {
                if (dict.elements.nodes[item].data.color == "grey") {
                    ospfName = dict.elements.nodes[item].data.id;
                    if ($.inArray( ospfName, selected ) != -1){
                        var w = window.open('/logospf&'+ospfName+"&"+ips[ospfName]+"&"+ips["all_ips"]);
                    }else {
                        $.ajax({
                            url: "/api/runospf", // the endpoint
                            type: "PUT", // http method
                            data: JSON.stringify({name: ospfName,
                                                        local_ips: ips[ospfName],
                                                        all_ips: ips["all_ips"]}),
                            contentType: "application/json"
                        });
                    }
                }
            }
        });
    });
    
    // Save Ajax 
    $(document).ready(function () {
        $("#save").click(function () {
            var name = $('#saveText').val();
            var dict = cy.json();
            dict["name"] = name;
            console.log(dict);
            $.ajax({
                url: "/api/save", // the endpoint
                type: "PUT", // http method
                data: JSON.stringify(dict),
                contentType: "application/json",
                dataType: 'json',
                // handle a non-successful response
                success: function (data) {
                    // Call this function on success
                    $('#saveText').val("");
                    return data;
                },
                error: function () {
                    console.log("ERROR");
                    console.log(data)
                }
            });
        });
    });


     // Load Ajax
    $(document).ready(function () {
        $("#checkJson").click(function () {
             $('#loadDiv').empty();
             var files = {};
             $.ajax({
                url: "/api/load", // the endpoint
                type: "GET", // http method
                contentType: "application/json",
                dataType: 'json',
                // handle a non-successful response
                success: function (data) {
                    // Call this function on success
                    for (item in data["files"]) {
                    $('#loadDiv').append("<input type='radio' id=" + data["files"][item] + " name=loadValue value=" + data["files"][item] + "> " +
                        "<label for=" + data["files"][item] + "> " + data["files"][item] + "</label><br>");
                    }
                    console.log(data);
                },
                error: function () {
                    console.log("ERROR");
                }
            });

        });
    });
    $(document).ready(function () {
        var name = "";
        var dict = {};
        $("#load").click(function () {
            $('div#loadDiv input[type=radio]').each(function() {
               if ($(this).is(":checked")) {
                   name = ($(this).attr('value'));
                   dict["name"] = name;
               }
            });

            $.ajax({
                url: "/api/load", // the endpoint
                type: "PUT", // http method
                data: JSON.stringify(dict),
                contentType: "application/json",
                dataType: 'json',
                // handle a non-successful response
                success: function (data) {
                    // Call this function on success
                    data["container"] = document.getElementById('cy');
                    cy = window.cy = cytoscape(data);
                },
                error: function () {
                    console.log("ERROR");
                }
            });
        });
    });



    //////////  Info network ajaxs
    $(document).ready(function () {
        $("#infoNet").click(function () {
            var dict = cy.json();
            $('#infoDiv').empty();
            $.ajax({
                url: "/api/infonet", // the endpoint
                type: "PUT", // http method
                data: JSON.stringify(dict),
                contentType: "application/json",
                dataType: 'json',
                // handle a non-successful response
                success: function (data) {
                    // Call this function on success
                    jQuery.each(data["nodes"], function (key, value) {
                        $('#infoDiv').append("<p><strong>"+ key + "<strong></p>")
                        $('#infoDiv').append("<p>Net: " + value[0]["net"] + "</p>")
                        $('#infoDiv').append("<p>Ip: " + value[0]["ip"] + "</p>")
                        $('#infoDiv').append("<p>Gateway: " + value[0]["gateway"] + "</p>")
                        $('#infoDiv').append("<p></p>")
                    });
                    jQuery.each(data["routers"], function (key, value) {
                        $('#infoDiv').append("<p><strong>"+ key + "<strong></p>")
                        jQuery.each(value, function (key2, value2) {
                            $('#infoDiv').append("<p>Net: " + value2["net"] + "</p>")
                            $('#infoDiv').append("<p>Ip: " + value2["ip"] + "</p>")
                            if (value2["gateway"]) {
                                $('#infoDiv').append("<p>Gateway: " + value2["gateway"] + "</p>")
                            }
                            $('#infoDiv').append("<p></p>")
                        });
                    });
                },
                error: function () {
                    console.log("ERROR");
                }
            });
        });
    });
    
    $("#fit").click(function () {
        console.log('cy=', cy);
        cy.fit();
    });

    $("#layout").click(function () {
        console.log('cy=', cy);
        cy.layout({
            name: 'dagre'
        });
    });


}); // ready
