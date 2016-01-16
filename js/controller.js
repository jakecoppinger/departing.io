window.busStop = 0;
window.arrivingBus = 0;

console.log("Port is:");
console.log(window.hostPort);
console.log("Host is:");
console.log(window.hostURL);

window.server = new Backend(window.hostURL, window.hostPort);

window.visualisingBus = false;
window.updatingView = true;

// Disable scrolling iOS Safari
$(document).bind(
    'touchmove',
    function(e) {
        e.preventDefault();
    }
);

$(document).ready(function() {

    // Hide canvas div until after page load to prevent flash
    setTimeout(function() {
        $("#hidpidiv").show();
    }, 3000);

    // Popup ibject for about page
    $('#about_popup').popup({
        opacity: 0.94,
        transition: 'all 0.3s',
        color: '#111111',
    });

    $("#address").autocomplete({
        source: function(request, response) {
            $("#testdata").text(JSON.stringify(request.term));
            $.ajax({
                type: "POST",
                url: "http://" + window.hostURL + ":" + window.hostPort + "/closeststop",
                dataType: 'json',
                async: true,
                data: {
                    search_term: request.term
                },
                success: function(data) {
                    response(data);
                }
            });

        },
        minLength: 1,
        delay: 300,
        select: function(event, ui) {
            if (ui.item) {

                if(ui.item.id != "0000") { // Don't try to load stuff when no stops shown
                    console.log("Selected: " + ui.item.label);
                    console.log("Bus Stop ID is " + ui.item.id);
                    $("#stopid").val(ui.item.id);

                    // This is where the magic happens
                    updateStopData(ui.item.label);

                    $("#loadingroutestext").text("Loading bus routes...");
                    $('.loading_routes').fadeIn();

                    heap.track('Selected bus stop', {'Bus stop description': ui.item.label, 'Bus stop ID': ui.item.id});
                }
            } else {
                console.log("Nothing selected, input was " + this.value);
            }

        },
        open: function() {
            $(this).removeClass("ui-corner-all").addClass("ui-corner-top");
        },
        close: function() {
            $(this).removeClass("ui-corner-top").addClass("ui-corner-all");
        }
    });

    // Allow scrolling when select a bus stop adress
    $("#address").focus(function() {
        $(document).unbind('touchmove');
        console.log("We have focus");
    });

    $("#address").focusout(function() {
        $(document).bind(
            'touchmove',
            function(e) {
                e.preventDefault();
            }
        );
    });
});

function updateStopData(addressString) {
    var stopID = $("#stopid").val();

    window.server.validStopID(stopID, function(response) {
        if (response) {
            window.busStop = new BusStop(stopID, addressString, server);
            window.busStop.updateDepartures("90", function(response) {
                window.busStop.setDepartures(response);
                updatedDeparturesResponse(response); // Updates listed departures
                // console.log(JSON.stringify(response)); // Show loaded bus routes
            });
        } else {
            console.log("Invalid bus route!");
        }
    });
}

function updatedDeparturesResponse(response) {
    var availableBusRoutes = window.busStop.updateAvailableBusRoutes();

    console.log(availableBusRoutes);

    if (availableBusRoutes.length > 0) {
        viewAvailableBusRoutes(availableBusRoutes);
        $('.loading_routes').fadeOut(function() {
            $(".afterloading_routes").fadeIn();
        });
        heap.track('Viewing departures', {'Bus route ID': $("#stopid").val()});
    } else {
        heap.track('No departures found', {'Bus route ID': $("#stopid").val()});

        $("#loadingroutestext").text("No departures found");

    }
}

function progressToVisualisation() {
    if ($("#busrouteselect").val()) {
        visualisingBus = true;
        updateFastestBus();
        showVisualisationPage();
        heap.track('Viewed bus route', {'Bus Route': $("#busrouteselect").val()});

    } else {
        console.log("No bus route has been selected!");
    }
}

function updateFastestBus() {
    var busRoute = $("#busrouteselect").val();
    var busObjectJSON = window.busStop.fastestBusOnRoute(busRoute);
    window.arrivingBus = new Bus(busObjectJSON);
}


// Future Location Development
/*
function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(setLocationCoords);
    } else {
        console.log("Geolocation is not supported by this browser.");
    }
}

function setLocationCoords(position) {
    locationCoords = [position.coords.latitude,position.coords.longitude];
    console.log(locationCoords);
}
*/