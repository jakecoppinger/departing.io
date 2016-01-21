/*
Departing.io, a web app to answer the question of "When will the next bus come?"
Copyright (C) 2016 Jake Coppinger

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

function viewAvailableBusRoutes(availableBusRoutes) {
    var options = $("#busrouteselect");
    options.empty();
    $.each(availableBusRoutes, function() {
        options.append($("<option />").val(this).text(this));
    });
}

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