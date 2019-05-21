/*
    Created by Jack Allcock 21/06/2018
    This javascript file handles the edit PV's modal
*/


$(document).ready(function(e){

    var grb_id = 1;
    var expr = [];
    var pv_id;
    var data = [];

    $("#modal_okay_button").click(function(event){
        // Get values entered into the inputs by the user
        pv = $("#builder").pv_val();
        var myJsonString = JSON.stringify(pv);

        reasonInput = $('#reason_input').val();
        contentInput = $('#content_input').val();


        // Get the data from data array
        reason = data[1];
        content = data[2];

        // Update the table data to that in the array
        reason.innerHTML = reasonInput;
        content.innerHTML = contentInput;

        // Take the contents of the table and put it into the hidden field
        fillInputFieldForPosting(rowsLength);
        saveBuildToUI(pv,$("#id_input").attr("pv"))
        console.log(pv)
    // Fade out 500ms
    modal.fadeOut(500);
    });

    $("#savec").click(function(){
        storeAllPVs()
    })
    function storeAllPVs() {
        json = {};
        $("#form_table").children("tbody").children("tr").each(function () {
            pvid = $(this).attr("index");
            json[pvid] = {};
            var builds = {}
            $(this).children(".pv_build").each(function () {
                block = $(this).attr("block");
                expression = $(this).attr("expression");
                consta = $(this).attr("const");
                va = $(this).attr("var");
                opp = $(this).attr("opp");
                val = $(this).attr("val");
                command = $(this).attr("command");
                if (!builds.hasOwnProperty(block)) {
                    builds[block] = {}
                }
                builds[block][expression] = {const: consta, var: va, opp: opp, val: val, command: command};
            });
            pv_code = $(this).children(".pv_def").text();
            pv_name = $(this).children().eq(0).text();
            pv_desc = $(this).children().eq(1).text();
            myJsonString = JSON.stringify(builds);
            json[pvid]['json'] = builds;
            json[pvid]['pv'] = pv_code;
            json[pvid]['pv_name'] = pv_name;
            json[pvid]['pv_desc'] = pv_desc;
        });
        json = JSON.stringify(json);
        $.ajax({
            type: "POST",
            url: '/builder/' + $("#rid").text(),
            data: {json: json},
            async:false,
            success: function () {
                console.log("test");
            }
        });
    }

    function saveBuildToUI(pv,pv_id){
        $("tr[index="+pv_id+"]").children(".pv_build").remove();
        blocks = Object.keys(pv);
        for (block of blocks) {
            block_id = block[block.length - 1]
            expressions = Object.keys(pv[block]);
            for (expression of expressions) {
                expression_id = expression[expression.length - 1]
                elements = Object.keys(pv[block][expression]);
                $("tr[index="+pv_id+"]").append("<td style='display:none;' class='pv_build' block='"+block_id+"' " +
                    "expression='"+expression_id+"' const='"+pv[block][expression]['const']+"'" +
                    "var='"+pv[block][expression]['var']+"' opp='"+pv[block][expression]['opp']+"'" +
                    " val='"+pv[block][expression]['val']+"' command='"+pv[block][expression]['command']+"'></td>")
            }
        }
    }
    // create the builder
    $.fn.pv_builder = function(title, exprFields, stmntFields, loadData){
        var block_id = 1;

        this.each(function(){
            $(this).addClass("builder_main");
            $(this).children().remove();
            var s = "<div id='grb_"+grb_id+"' class='grb'>";
            //s += "<hr>";
            s += "</div>";
            s += "<div class='b_d right'>";
            s += "<img id='add_block' src='/static/img/plus.png' class='b_icon'>";
            s += "</div>";
            $(this).append(s);
        });
        builder = $("#grb_"+grb_id);
        setListeners(exprFields,stmntFields);
        $("#add_block").click(function(){
            div = createBlockStart(builder, block_id);
            addExpression(div, exprFields);
            block_id = createBlockEnd(builder, block_id);

        });
        if(Object.keys(loadData).length > 0){
            block_id = loadBuild(builder,block_id,loadData,exprFields,stmntFields);
        }
    };
    // builder function to get the values output to store in db
    $.fn.pv_val = function(){
        var s = {};
        this.each(function(){
            $(this).children(".grb").children().each(function(){
                s = getExpression($(this), s);
            });
        });
        return s;
    };
    // creates the start of a block ready for an expression to be added
    function createBlockStart(builder,block_id){
        builder.append("<div expr='1' block='"+block_id+"' id='block_"+block_id+"' class='grb_block'></div>");
        block = $("#block_"+block_id);
        block.append("<div expr='1' id='expr_"+block_id+"_1' class='grb_expr'></div>");
        div = $("#expr_"+block_id+"_1");
        return div;
    }
    // ends a block ready for new block to be created
    function createBlockEnd(builder, block_id){
        builder.append("<hr style='border-top: 1px solid #ccc;'>");
        expr[block_id] = 2;
        return block_id+=1;
    }
    // loads data in to builder
    function loadBuild(builder, block_id, loadData, exprFields, stmntFields){
        console.log(loadData)
        blocks = Object.keys(loadData);
        for (blk of blocks) {
            div = createBlockStart(builder, block_id);
            expressions = Object.keys(loadData[blk]);
            for (expression of expressions) {
                e = loadData[blk][expression];
                if(expression == 1){
                    div = addExpression(div, exprFields);
                }
                $(div).children("#var").val(e['var']);
                $(div).children("#val").val(e['val']);
                if(e['command'] != ""){
                    $(div).children("#opp").val(e['opp']);;
                    select = $(div).children("#command");
                    select.val(e['command']);
                    div = commandChanged(select, exprFields, stmntFields)
                }
            }

            block_id = createBlockEnd(builder, block_id);
        }
        return block_id;
    }
    // checks for property in object, returns false if not found.
    function hasOwnProperty(obj, prop) {
        var proto = obj.__proto__ || obj.constructor.prototype;
        return (prop in obj) &&
            (!(prop in proto) || proto[prop] !== obj[prop]);
    }
    // allows object to call hasOwnProperty function
    if ( Object.prototype.hasOwnProperty ) {
        var hasOwnProperty = function(obj, prop) {
            return obj.hasOwnProperty(prop);
        }
    }
    // Create dictionary of all the table cell rows
    var tableRows = [];
            $("#form_table > tbody  > tr").each(function() {
                var row = {
                  "name" : $(this).find(".table--cell")[0],
                  "reason" : $(this).find(".table--cell")[1],
                  "content" : $(this).find(".table--cell")[2],
                };
                tableRows.push(row);
            });

    // Get length of dictionary so it can be iterated over
    rowsLength = tableRows.length

    // Take the contents of the table and put it into the hidden field
    fillInputFieldForPosting(rowsLength);

    // Get the modal so that we can hide/un-hide and attach the ID
    var modal = $(".modal");

    // On the click of the Modal Close button, hide the modal and refresh the page.
    $(".close").click(function(event){
        // Fade out 500ms
        modal.fadeOut(500);
    });

    // When the edit button is clicked, get the ID from the button attribute
    // Show the modal and change the input fields value to the ID
    $(".pv-edit-button").click(function(event){
        var vars = [];
        var builds = {}
        pvid = parseInt($(this).attr("pvid"));
        $(this).parent().siblings(".pv_var").each(function(){
            vars.push($(this).text());
        });
        $(this).parent().siblings(".pv_build").each(function(){
            block = $(this).attr("block"); expression = $(this).attr("expression");
            consta = $(this).attr("const"); va = $(this).attr("var"); opp = $(this).attr("opp");
            val = $(this).attr("val"); command = $(this).attr("command");
            if(!builds.hasOwnProperty(block)){
                builds[block] = {}
            }
            builds[block][expression] = {const:consta, var:va, opp:opp, val:val, command:command};
        });
        // Fade in 500ms
        modal.fadeIn(500);

        variableId = this.id;

        // Length of the rows in the table
        rowsLength = tableRows.length
        // Array we will append rows to
        data = [];

        /** First we need to go through the table data and find the row we need.
            Then we can set the modal inputs with data from that table row and update the actual table data when the
            okay button is clicked
        **/

        // Iterate over dictionary of table rows
        for (i=0; i < rowsLength; i++) {
            // Get dictionary out of array by index
            row = tableRows[i];
            // Get the PV Name text
            name = row['name'].innerHTML;

            // If the dictionary is the one we need add the data to the array
            if (name === variableId) {
                data.push(row['name']);
                data.push(row['reason']);
                data.push(row['content']);
            }
        }

        // Set the inputs values to that in the data array
        $("#id_input").attr("pv", pvid)
        $("#id_input").val(data[0].innerHTML);
        $("#reason_input").val(data[1].innerHTML);
        $("#content_input").val(data[2].innerText);
        // initiate the builder
        $("#builder").pv_builder(data[0].innerHTML+" Builder",{
            const : {
                type : "label",
                extras : {attr : {val : "IF"}}
                    },
            var : {
                type : "select",
                extras : {options: vars}
                },
            opp : {
                type : "select",
                extras : {options : [ "==", ">", "<", "IN"]}
            },
            val : {
                type : "input",
                extras : {attr : {val : ""}}//Don't need this, just an example
            },
            command : {
                type : "select",
                extras : {options : [ "AND", "OR", "SET"]}
            }
        },
            {
            var : {
                type : "select",
                extras : {options: vars}
                },
            opp : {
                type : "label",
                extras : {attr : {val : "="}}
                },
            val : {
                type : "input",
                extras : {attr : {val : ""}}//Don't need this, just an example
                },
            },
            builds
        );

        // Edit table data when the okay button is pressed


        // Make sure the page doesn't refresh/change when this button is clicked
        return false;
    });

function fillInputFieldForPosting(rowsLength) {
        // Fill hidden input with all table data as a comma separated string
        data = [];
        for (i=0; i < rowsLength; i++) {
            // Get row from dictionary
            row = tableRows[i];

            // Get the data from row
            name = row['name'].innerHTML;
            reason = row['reason'].innerHTML;
            content = row['content'].innerHTML;

            // Create a dictionary entry to put in the input
            var row = {
                  name : name,
                  "reason" : reason,
                  "content" : content,
                };

            // Add to the data array
            data.push(row);
        }

        // Iterate over data array and add the data as a comma separated list in the input
        dataLength = data.length;
        dataToSend = "";
        // Put the data array into the input
        for (i=0; i < dataLength; i++) {
            row = data[i]
            dataToSend += row['name'] + '^';
            dataToSend += row['reason']+ '^';
            dataToSend += row['content']+ '^';
        }
        $(".hidden-edit-input-content").val(dataToSend);

    }
});


// retrieve expression given element
function getExpression(el, s){
    if($(el).attr('id') == "ignore"){
        return s;
    }
    if($(el).prop('nodeName') == "DIV"){
        s[$(el).attr('id')] = {};
        $(el).children().each(function(){
            s[$(el).attr('id')] = getExpression($(this), s[$(el).attr('id')]);
        });
    }else if($(el).prop('nodeName') == "HR" || $(el).prop('nodeName') == "IMG"){
        return s;
    }else{
        if($(el).prop('nodeName') == "LABEL"){
            s[$(el).attr('id')] = $(el).text();
        }else if($(el).prop('nodeName') == "H4"){
            s["Title"] = $(el).text();
        }else{
            s[$(el).attr('id')] = $(el).val();
        }
    }
    return s;
}

function addExpression(div,fields,expression=false){
    first = (expression) ? true : false;
    for (var column in fields) {
        if(expression && first){
            first = false;
            continue;
        }
        div.append(createElement(column, fields[column]['type'], fields[column]['extras']));
    }
    div.append(createDeleteButton());
    return div;
}

function setListeners(exprFields, stmntFields){
    $("body").off("change", "select[type='command']");
    $("body").on("click", ".delete", function(){
        deleteLines($(this));
    });
    $("body").on("change", "select[type='command']", function(){
        commandChanged(this, exprFields, stmntFields);
    });

}

function commandChanged(e, exprFields, stmntFields){
    block_id = $(e).closest(".grb_block").attr("block");
    expression_id = parseInt($(e).closest("div").attr("expr")) + 1;
    block = $("#block_"+block_id);
    if(! (($(e).parent().nextAll("div").length <= 1) || ($(this).val() != "SET"))){
            $(e).val($.data(e, 'current'));
            return false;
    }
    r = true;
    if($("#expr_"+block_id+"_"+expression_id).length){
        div = $("#expr_"+block_id+"_"+expression_id);
        if($(e).val() == "SET"){
            $(e).parent().nextAll("div").remove();
        }else{
            if($(e).parent().next("div").children("label").first().text() == "SET"){
                $(e).parent().nextAll("div").remove();
            }else{
                r = false;
                $(e).parent().next("div").children("label").first().text($(e).val());
            }
        }
    }
    if(r){
        block.append("<div expr='"+expression_id+"' id='expr_"+block_id+"_"+expression_id+"' class='grb_expr'></div>");
        div = $("#expr_"+block_id+"_"+expression_id);
        div.append(createElement("ignore","label",{attr : {val:$(e).val()}}));
        end = ($(e).val() == "SET") ? addExpression(div, stmntFields, false) : addExpression(div, exprFields, true);
        $.data(e, 'current', $(e).val());
    }
    return div;
}

function deleteLines(button){
    if(button.parent().parent().attr("expr") == "1"){
            button.parent().parent().parent().next("hr").remove();
            button.parent().parent().parent().remove();
    }else{
        button.parent().parent().nextAll("div").remove();
        button.parent().parent().remove();
    }
}

function createDeleteButton(){
    return "<div id='ignore' class='b_div right'><img class='right b_icon delete' src='/static/img//minus.png'></div>";
}

function createElement(id, type, extras){
    switch (type) {
        case "label":
            return createLabel(id,extras["attr"]);
        case "select":
            return createSelect(id,extras["options"]);
        case "input":
            return createInput(id,extras["attr"]);
        default:
            console.log("Element not in label, select, input!");
    }
}

function createLabel(id,options){
    return "<label class='grb_l input' id='"+id+"'>"+options['val']+"</label>";
}
function createSelect(id,options){
    if(!options.includes(id)){
        options.unshift(id);
    }
    var s = "<select type='"+id+"' class='grb_i grb_"+id+" input input--select' id='"+id+"'>";
    options.forEach(function(entry) {
        s+= "<option value='"+entry+"'>"+entry+"</option>";
    });
    s += "</select>";
    return s;
}
function createInput(id,options){
    return "<input class='grb_i input' id='"+id+"'>";
}