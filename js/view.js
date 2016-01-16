function viewAvailableBusRoutes(availableBusRoutes) {
    var options = $("#busrouteselect");
    options.empty();
    $.each(availableBusRoutes, function() {
        options.append($("<option />").val(this).text(this));
    });
};

function secondsUntilNextBus() {
    return window.arrivingBus.exactSecondsUntilArrival();
}

function isBusDisplayed() {
    if (window.arrivingBus) {
        return true;
    } else {
        return false;
    }
}
var testing = true;

function showVisualisationPage() {
    $("#main_overlay").fadeOut(function() {
        $("#main_overlay").hide();
        $("canvas").fadeIn();
    });
    
}

function showMainPage() {
    if (visualisingBus) {
        $("canvas").fadeOut(function() {
            $("#main_overlay").fadeIn();
            $("main_overlay").show();
        });
        visualisingBus = false;
    }
}