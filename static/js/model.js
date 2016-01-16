function Backend(server, port) {
    this.serverHost = server;
    this.serverPort = port;
    this.currentStop = '';
    this.currentStopDepartures = [];
}

Backend.prototype.validStopID = function(stopID, callbackFunction) {
    var requestUrl = "http://" + this.serverHost + ":" + this.serverPort + "/validstopid";
    
    $.ajax({
        type: "POST",
        url: requestUrl,
        dataType: 'json',
        async: true,
        data: {
            stop_id: stopID
        },
        success: function(response) {
            callbackFunction(stopID, response);
        }
    });
}

Backend.prototype.stopDepartures = function(stopID, previewInterval, callbackFunction) {
    var requestUrl = "http://" + this.serverHost + ":" + this.serverPort + "/departures";
    $.ajax({
        type: "POST",
        url: requestUrl,
        dataType: 'json',
        async: true,
        data: {
            stop_id: stopID,
            preview_time: previewInterval
        },
        success: function(response) {
            callbackFunction(response);
        }
    });
}

function BusStop(stopID, addressString, server) {
    this.server = server;
    this.stopID = stopID;
    this.addressString = addressString;
    this.stopDepartures = ["???"];
    self.journeysOnBusRoute = [];
    this.availableBusRoutes = [];

}

BusStop.prototype.updateDepartures = function(previewInterval, callbackFunction) {
    this.server.stopDepartures(this.stopID, previewInterval, function(response) {
        callbackFunction(response);
    });
}

BusStop.prototype.setDepartures = function(departures) {
    this.stopDepartures = departures;
}

BusStop.prototype.updateAvailableBusRoutes = function() {
    var allRoutes = this.stopDepartures;

    availableBusRoutes = [];
    $.each(allRoutes, function(index, value) {
        var busNumber = value["busRouteNumber"];
        if ($.inArray(busNumber, availableBusRoutes) == -1) {
            availableBusRoutes.push(busNumber);
        }
    });
    this.availableBusRoutes = availableBusRoutes;
    return availableBusRoutes;
}

BusStop.prototype.validBusRouteSelected = function(busRouteNumber) {
    if (this.availableBusRoutes.indexOf(busRouteNumber) > -1) {
        return true;
    } else {
        return false;
    }
}

BusStop.prototype.updateJourneysOnBusRoute = function(busRoute) {
    var busRouteJourneys = [];
    $.each(this.stopDepartures, function(index, busJourney) {
        if (busJourney["busRouteNumber"] == busRoute) {
            busRouteJourneys.push(busJourney);
        }
    });

    this.journeysOnBusRoute = busRouteJourneys;
};

BusStop.prototype.fastestBusOnRoute = function(busRouteNumber) {
    this.updateJourneysOnBusRoute(busRouteNumber);
    var fastestBus = [];
    var currentTime = moment();

    $.each(this.journeysOnBusRoute, function(index, currentBus) {
        if (fastestBus.length == 0) {
            fastestBus = currentBus;
        } else {
            var currentFastest = moment(fastestBus["departureTime"], moment.ISO_8601);
            var thisBus = moment(currentBus["departureTime"], moment.ISO_8601);

            if (currentFastest.diff(thisBus) > 0) {
                fastestBus = currentBus;
            }
        }
    });
    return fastestBus;
}

BusStop.prototype.address = function() {
    return this.addressString;
}

function Bus(busJourneyObject) {
    this.busJourneyObject = busJourneyObject;
}

Bus.prototype.departureTimestamp = function() {
    return this.busJourneyObject["departureTime"];
}

Bus.prototype.routeNumber = function() {
    return this.busJourneyObject["busRouteNumber"];
}

Bus.prototype.destination = function() {
    return this.busJourneyObject["destinationName"];
}

Bus.prototype.monitored = function() {
    if (this.busJourneyObject["monitored"] == "true") {
        return true;
    } else {
        return false;
    }
}

Bus.prototype._durationUntilArrival = function() {
    var departureTime = moment(this.departureTimestamp(), moment.ISO_8601);
    var currentTime = moment();
    return moment.duration(departureTime.diff(currentTime));
}


Bus.prototype.minutesUntilArrival = function() {

    var duration = this._durationUntilArrival();
    var minutes = duration.minutes(); // Fix so it works over 1 hour
    //var seconds = duration.seconds();
    return minutes;
}

Bus.prototype.secondsUntilArrival = function() {
    var duration = this._durationUntilArrival();
    var seconds = duration.seconds();
    return seconds;
}

Bus.prototype.exactSecondsUntilArrival = function() {
    var duration = this._durationUntilArrival();
    var seconds = duration.asSeconds() - (duration.minutes() * 60);
    return seconds;
}

// Future Location Development

/*
function setLocationCoords(position) {
    locationCoords = [position.coords.latitude,position.coords.longitude];
    console.log(locationCoords);
}
*/