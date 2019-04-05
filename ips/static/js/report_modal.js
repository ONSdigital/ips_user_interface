/*
    Created by Jack Allcock 21/06/2018
    This javascript file handles the edit PV's modal
*/

$(document).ready(function(e){

    // Get the modal so that we can hide/un-hide and attach the ID
    var modal = $(".modal");

    // When the edit button is clicked, get the ID from the button attribute
    // Show the modal and change the input fields value to the ID
    $(".pv-edit-button").click(function(event){

        // Fade in 500ms
        modal.fadeIn(500);

        variableId = this.id;

        // Length of the rows in the table
        rowsLength = tableRows.length
        // Array we will append rows to
        data = [];

        // Make sure the page doesn't refresh/change when this button is clicked
        return false;
    });
});