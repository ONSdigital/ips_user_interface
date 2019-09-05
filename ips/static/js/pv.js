//globals
var build = true;
var right = false;
var copy = false;

$(function(){
    $('#resizing_select').change(function(){
        $("#width_tmp_option").html($(' option:selected').text());
        $(this).width($("#width_tmp_select").width());
    });

    $.contextMenu({
        selector: '.pv_line',
        callback: function(key, options) {
            if(key === "delete"){
                if($(".pv_el_selected").length > 0){
                    $(".pv_el_selected").remove();
                }else {
                    $(".pv_line_selected").remove();
                }
            }else if(key === "copy_line"){
                copy = $(".pv_line_selected");
            }else if(key === "pasteline"){
                let curLine = $(".context-menu-active");
                curLine.after(copy.clone().removeClass("pv_line_selected").removeClass("context-menu-active"))
            }
            else{
                key = key.split("_");

                if(key[0].includes("-")){
                    let skey = key[0].split("-");
                    insertStatement($(".pv_el_selected"), skey[0], key[1]);
                }else if(key[0] === "newline"){
                    insertNewline(key[1]);
                }else {
                    insertElement($(".pv_el_selected"), key[0], key[1]);
                }
            }
        },events: {
            hide: function(opt) {
              $(".pv_el_selected").removeClass("pv_el_selected");
            }
        },
        items: {
            "delete": {"name": "Delete"},
            "sep2": "---------",
            "copy_line": {"name": "Copy Line(s)"},
            "pasteline": {"name": "Paste"},
            "sep": "---------",
            "fold1": {
                "name": "Insert Left",
                "items" : {
                    "fold1": {
                        "name": "Statements",
                        "items": {
                            "if-statement_left": {"name": "if"},
                            "var-statement_left": {"name": "set var"},
                        }
                    },
                    "fold1a": {
                        "name": "Elements",
                        "items": {
                            "if_left": {"name": "if"},
                            "var_left": {"name": "var"},
                            "opp_left": {"name": "=="},
                            "val_left": {"name": "val"},
                            "and_left": {"name": "and"}
                        }
                    },
                    "fold1b": {
                        "name": "Misc",
                        "items": {
                            "tab_left": {"name": "tab"},
                            "bl_left": {"name": "("},
                            "br_left": {"name": ")"},
                            "colon_left": {"name": ":"}
                        }
                    }
                }
            },
            "fold1a": {
                "name": "Insert Right",
                "items" : {
                    "fold1": {
                        "name": "Statements",
                        "items": {
                            "if-statement_right": {"name": "if"},
                            "var-statement_right": {"name": "set var"},
                        }
                    },
                    "fold1a": {
                        "name": "Elements",
                        "items": {
                            "if_right": {"name": "if"},
                            "var_right": {"name": "var"},
                            "opp_right": {"name": "=="},
                            "val_right": {"name": "val"},
                            "and_right": {"name": "and"}
                        }
                    },
                    "fold1b": {
                        "name": "Misc",
                        "items": {
                            "tab_right": {"name": "tab"},
                            "bl_right": {"name": "("},
                            "br_right": {"name": ")"},
                            "colon_right": {"name": ":"}
                        }
                    }
                }
            },
            "sep2": "---------",
            "newline_a": {"name": "New Line Above"},
            "newline_b": {"name": "New Line Below"},
        }
    });
});

function setPVListeners(main){
    main.keydown(function(e){
        if([32, 37, 38, 39, 40].indexOf(e.keyCode) > -1) {
            e.preventDefault();
        }
    });
    $(".pv_input").each(function(){
        resizeInput($(this));
    });
    $( ".pv_input" ).keyup(function(){resizeInput($(this))});
    $(".pv_input").keydown(function(e) {
        return e.which !== 32;
    });
    $(".pv_select").each(function(){
        resizeSelect($(this));
    });
    $( ".pv_select" ).change(function(){resizeSelect($(this))});
    $( ".pv_select" ).blur(function(){resizeSelect($(this))});
    $( ".pv_select" ).focus(function(){restoreSelect($(this))});
    $('.pv_div').on('click', '.pv_el_delete', function(){
        $(this).parent().remove()
    });
    $( ".pv_div").on('click', '.pv_el', function(e){
        $(".pv_el_selected").removeClass("pv_el_selected");
        if (!e.shiftKey){
            e.stopPropagation();
            $(".pv_line_selected").removeClass("pv_line_selected");
            $(this).parent().addClass("pv_line_selected")
            $(this).toggleClass("pv_el_selected");
        }
    })
    $( ".pv_div").on('contextmenu', '.pv_el', function(){
        $(".pv_el_selected").removeClass("pv_el_selected");
        $(this).addClass("pv_el_selected");
    })
    $( ".pv_div").on('click', '.pv_line', function(e){
        $(".pv_el_selected").removeClass("pv_el_selected");
        if (!e.shiftKey) $(".pv_line_selected").removeClass("pv_line_selected");
        else{
            let selected, first, last;
            if($(".pv_line_selected").first().index() < $(this).index()){
                first = $(".pv_line_selected").first();
                last = $(this);
            }else{
                last = $(".pv_line_selected").last();
                first = $(this);
            }
            first.prevAll().removeClass("pv_line_selected");
            last.nextAll().removeClass("pv_line_selected");
            selected = first.nextUntil(last);
            selected.addClass("pv_line_selected");
        }
        $(this).toggleClass("pv_line_selected");
    })
    $( ".pv_div").on('contextmenu', '.pv_line', function(){
        if($(this).hasClass("pv_line_selected")) return;
        $(".pv_line_selected").removeClass("pv_line_selected");
        $(this).toggleClass("pv_line_selected");
    })
    $( ".pv_div").on('keyup', '.pv_line', function(e){
        let el = false;
        if(e.which == 40) {
            $(".pv_line_selected").removeClass("pv_line_selected");
            el = $(this).next(".pv_line");
        }else if(e.which == 38){
            $(".pv_line_selected").removeClass("pv_line_selected");
            el = $(this).prev(".pv_line");
        }
        if(el) {
            el.toggleClass("pv_line_selected");
            el.focus();
        }
    })
    $('#txtbld').change(function(){
        build = !build;
        if(!build){
           $(".pv_txt_div").val($("#builder").txt_val());
        }
        $(".pv_div").toggle();
        $(".pv_txt_div").toggle();
    });

    $('#lr').change(function(){
        right = !right;
    })
}

$.fn.pv_builder_v2 = function (content){
    right = false;
    let header = pvHeader();
    let lines = getLines(content);
    lines = convertLines(lines);
    for( var i = 0; i < lines.length; i++){
        if(i === 0){
            lines[i] = "<div class='pv_line pv_line_selected' tabindex='"+i+"'>"+lines[i].join("")+"</div>";
        }else{
            lines[i] = "<div class='pv_line' tabindex='"+i+"'>"+lines[i].join("")+"</div>";
        }
    }
    lines = "<div class='pv_div'>"+lines.join("")+"</div>";
    lines += "<textarea disabled class='pv_txt_div'>"+content+"</textarea>";
    this.empty();
    this.append(header);
    this.append(lines);
    setPVListeners(this);
    headerListeners();
};

$.fn.txt_val = function (){
    let container = $(this).children(".pv_div").first();
    let s = "";
    $(container).children(".pv_line").each(function(){
        $(this).children(".pv_el").each(function(){
            let el = $(this).children().first();
            if(el.is("span")){
                s += el.text();
            }else{
                let n = $(this).next(".pv_el").children().first();
                if( n.length > 0){
                    if((! (el.hasClass("pv_and") || el.hasClass("pv_op"))) && n.is("span")){
                        s += el.val();
                    }else{
                        s += el.val() + " ";
                    }
                }else{
                    s += el.val() + " ";
                }
            }
        });
        s += "\n";
    });
    return s;
};

//------------------------ Header Stuff ---------------------------------
function pvHeader(){
    let s = "<div class='pv_header'>";
    s += "<span class='pv_header_el'>Insert to</span>"
    s += lrSwitch("lr", false);
    s += headerSpan("Statements");
    s += headerButton("if_statement", "if");
    s += headerButton("var_statement", "set var");
    s += headerSpan("Elements");
    s += headerButton("if", "if");
    s += headerButton("var", "var");
    s += headerButton("and", "and/or");
    s += headerButton("opp", "+-/*=");
    s += headerButton("val", "value");
    s += headerSpan("Misc");
    s += headerButton("tab", "tab");
    s += headerButton("bl", "(");
    s += headerButton("br", ")");
    s += headerButton("col", ":");
    s += headerSpan("New Line");
    s += headerButton("a_newline", "above");
    s += headerButton("b_newline", "below");
    s += lrSwitch("txtbld", true);
    s += "</div>";
    return s;
}

function headerButton(id, value){
    let s = "<button class='pv_header_button' id='"+id+"'>"+value+"</button>";
    return s;
}

function headerSpan(value){
    let s = "<span class='pv_header_span'>"+value+"</span>";
    return s;
}

function lrSwitch(id, view){
    if(view) {
        var s = '<div style="float: right" class="onoffswitch pv_header_el">';
    }else{
        var s = '<div class="onoffswitch pv_header_el">';
    }
    s += '<input type="checkbox" name="onoffswitch" class="onoffswitch-checkbox" id="'+id+'" checked>';
    s += '<label class="onoffswitch-label" for="'+id+'">';
    if(view){
        s += '<span class="onoffswitchview-inner"></span>';
    }else{
        s += '<span class="onoffswitch-inner"></span>';
    }
    s += '<span class="onoffswitch-switch"></span>';
    s += '</label>';
    s += '</div>';
    return s;
}

function headerListeners(){
    $(".pv_header_button").click(function(){
        let el = $(".pv_el_selected");
        let type = $(this).attr("id").split("_");
        if(type.length === 1) {
            insertElement(el, $(this).attr("id"), right ? "right" : "left");
        }else{
            if(type[1] == "statement"){
                insertStatement(el, type[0], right ? "right" : "left");
            }else if(type[1] == "newline"){
                insertNewline(type[0]);
            }
        }
    })
}

//------------------------ Manipulation ---------------------------------

function convertLines(lines){
    for( var i = 0; i < lines.length; i++){
        let strs = lines[i];
        for( var x = 0; x < strs.length; x++){
            let special = false;
            do {
                special = specialCase(lines[i][x], x);
                if(special !== false){
                    if(Array.isArray(special[0])){
                        lines[i].splice(special[1], 1);
                        let ind = 0;
                        for( let z = special[1]; z < special[1]+special[0].length; z++) {
                            lines[i].splice(z, 0, special[0][ind]);
                            ind ++;
                        }
                    }else {
                        lines[i][x] = special[2];
                        lines[i].splice(special[1], 0, special[0]);
                    }
                }
            } while (special !== false);
            lines[i][x] = convertToElement(lines[i][x]);
        }
    }
    return lines;
}

function convertToElement(s){
    let el = "<div class='pv_el pv_cm'>";
    if(isIf(s)){
        el += ifElement(s);
    }else if(isAnd(s)){
        el += andElement(s);
    }else if(isValue(s)){
        el += valueElement(s);
    }else if(isOpperator(s)){
        el += opElement(s);
    }else if(isSpecialChar(s)){
        el += charElement(s);
    }else if(isTab(s)){
        el += tabElement(s);
    }else{
        el += varElement(s);
    }
    el += "<img class='pv_el_delete' src='/static/img/close.svg'>";
    el += "</div>";
    return el;
}

function getLines(content){
    let lines = content.replaceAll("    ","TAB ");
    lines = lines.split("\n");
    for( var i = 0; i < lines.length; i++){
       if ( lines[i] != "") {
           break;
       }else{
           lines.splice(i, 1);
           i--;
       }
    }
    for( var i = 0; i < lines.length; i++){
        lines[i] = lines[i].replaceAll(", ", ",");
        lines[i] = lines[i].split(" ");
    }
    return lines;
}



//-------------------------- Element Creation ------------------------------
function charElement(s){
    let el = "<span class='pv_span'>"+s+"</span>";
    return el;
}

function tabElement(s){
    let el = "<span class='pv_tab'>    </span>";
    return el;
}

function varElement(s){
    s = s.replaceAll("'", "&#39;");
    let el = "<input class='pv_input' value='"+s+"'>"
    return el;
}

function ifElement(s){
    let arr = ['if', 'elif', 'else'];
    let el = "<select class='pv_select' resized=false>";
    arr.forEach(function(op){
        if(op == s){
            el += "<option selected value='"+op+"'>"+op+"</option>";
        }else{
            el += "<option value='"+op+"'>"+op+"</option>";
        }
    });
    el += "</select>";
    return el;
}

function andElement(s){
    let arr = ['and', 'or'];
    let el = "<select class='pv_select pv_and' resized=false>";
    arr.forEach(function(op){
        if(op == s){
            el += "<option selected value='"+op+"'>"+op+"</option>";
        }else{
            el += "<option value='"+op+"'>"+op+"</option>";
        }
    });
    el += "</select>";
    return el;
}

function opElement(s){
    let arr = ['=', '!=', '==', '>', '>=', '<', '<=', '+', '+=', '-', '-=', '*', '%', 'in'];
    let el = "<select class='pv_select pv_op' resized=false>";
    arr.forEach(function(op){
        if(op == s){
            el += "<option selected value='"+op+"'>"+op+"</option>";
        }else{
            el += "<option value='"+op+"'>"+op+"</option>";
        }
    });
    el += "</select>";
    return el;
}

function valueElement(s){
    if(isStringValue(s)){
        s = s.slice(1,-1);
        s = "&#39;"+s+"&#39;";
    }
    let el = "<input class='pv_input' value='"+s+"'>"
    return el;
}



//-------------------------- Type Checking ---------------------------------
function isIf(s){
    switch (s) {
        case "if":
            return true;
        case "elif":
            return true;
        case "else":
            return true;
    }
    return false;
}

function isAnd(s){
    switch (s) {
        case "and":
            return true;
        case "or":
            return true;
    }
    return false;
}

function isTab(s){
    if(s === "TAB"){
        return true;
    }
    return false;
}

function isOpperator(s){
    let reg = /^[\+\-\=*&%\\><!]+|in{1}$/;
    return reg.test(s);
}

function isValue(s){
    if(isStringValue(s)){
       return true;
    }else if(isNumber(s)){
        return true;
    }
    return false;
}

function isNumber(s){
    let reg = /^[0-9]$/
    return reg.test(s)
}

function isStringValue(s){
    if(s[0] == "'" && s[s.length - 1] == "'"){
       return true;
    }
    return false;
}

function isSpecialChar(s){
    switch (s) {
        case ")":
            return true;
        case "(":
            return true;
        case ":":
            return true;
        case "":
            return true;
        default:
            return false;
    }
}

//--------------------------    Misc     ---------------------------------

function colonEnd(s){
    if(s[s.length - 1] == ":"){
        return true;
    }
    return false;
}

function closingBracketEnd(s){
    if(s[s.length - 1] == ")"){
        return true;
    }
    return false;
}

function openingBracketEnd(s){
    if(s[s.length - 1] == "("){
        return true;
    }
    return false;
}

function openingBracketStart(s){
    if(s[0] == "("){
        return true;
    }
    return false;
}

function specialCase(s, index){
    if(s.length <= 1){
        return false;
    }
    if(colonEnd(s)){
        return [":", index+1, s.substring(0, s.length-1)];
    }else if(closingBracketEnd(s)){
        return [")", index+1, s.substring(0, s.length-1)];
    }else if(openingBracketEnd(s)){
        return ["(", index+1, s.substring(0, s.length-1)];
    }else if(openingBracketStart(s)){
        return ["(", index, s.substring(1, s.length)];
    }else if(s.includes("(")){
        let a = getSplitArr(s, "(");
        return [a, index];
    }else if(s.includes(")")){
        let a = getSplitArr(s, ")");
        return [a, index];
    }
    return false;
}

function getSplitArr(s,del){
    let arr = s.split(del);
    for( var i = 1; i < arr.length; i+=2) {
        arr.splice(i, 0, del)
    }
    return arr;
}

//------------------- Select events ---------------------
function resizeSelect(sel) {
    sel = sel[0];
    let resized = $(sel).attr("resized");
    if(resized == "true") return;
    for (var i=0; i<sel.options.length; i++) {
        sel.options[i].title=sel.options[i].innerHTML;
        if (i!=sel.options.selectedIndex) sel.options[i].innerHTML='';
    }
    $(sel).attr("resized", true);
    sel.blur();
}

function restoreSelect(sel) {
    sel = sel[0];
    if($(sel).attr("resized") == "false") return;
    for (var i=0; i<sel.options.length; i++) {
        sel.options[i].innerHTML=sel.options[i].title;
    }
    $(sel).attr("resized", false);
}

function resizeInput(input) {
    $(input).width( $(input).val().length  + 'ch');
}
//----------------------------------------------------------

String.prototype.replaceAll = function(search, replacement) {
    var target = this;
    return target.replace(new RegExp(search, 'g'), replacement);
};

function insertElement(el, key, dir){
    if(el.length > 0) {
        if (dir === "right") {
            el.after(getNewEl(key));
            el.removeClass("pv_el_selected");
            el.next(".pv_el").addClass("pv_el_selected");
        } else if (dir === "left") {
            el.before(getNewEl(key));
        }
    }else{
        if (dir === "right") {
            $(".pv_line_selected").append(getNewEl(key));
        } else if (dir === "left") {
            $(".pv_line_selected").prepend(getNewEl(key));
        }
    }
    int ()
}

function insertStatement(el, key, dir){
    if(el.length > 0) {
        if (dir === "right") {
            el.after(getInsertStatement(key));
        } else if (dir === "left") {
            el.before(getInsertStatement(key));
        }
    }else{
        if (dir === "right") {
            $(".pv_line_selected").append(getInsertStatement(key));
        } else if (dir === "left") {
            $(".pv_line_selected").prepend(getInsertStatement(key));
        }
    }
}

function insertNewline(dir){
    let curLine = $(".pv_line_selected");
    if(curLine.length > 0) {
        if (dir === "a") {
            $(curLine).before(getNewlineEl(curLine.prev(".pv_line")));
        } else {
            $(curLine).after(getNewlineEl(curLine));
        }
    }else{
        $(".pv_div").prepend(getNewlineEl(curLine.prev(".pv_line")));
    }
}

function getNewlineEl(curLine){
    let el = "<div class='pv_line' tabindex='0'>";
    if(curLine.length > 0) {
        if (curLine.children().last().children(".pv_span").text() === ":"){
            el += getNewEl("tab");
        }
        curLine.children().each(function(){
            if($(this).children().first().hasClass("pv_tab")){
                el += getNewEl("tab");
            }else{
                return false;
            }
        })
    }
    el += getInsertStatement("var");
    el += "</div>";
    return el;
}

function getInsertStatement(type){
    let statement = "";
    if(type === "if"){
        statement += getNewEl("if");
        statement += getNewEl("var");
        statement += getNewEl("opp");
        statement += getNewEl("val");
        statement += getNewEl("colon");
    }else if(type === "var"){
        statement += getNewEl("var");
        statement += getNewEl("opp");
        statement += getNewEl("val");
    }
    return statement;
}

function getNewEl(key){
    let el = "<div class='pv_el pv_cm'>";
    switch(key){
        case "if":
            el += ifElement("if");
            break;
        case "var":
            el += varElement("var");
            break;
        case "opp":
            el += opElement("==");
            break;
        case "val":
            el += valueElement("value");
            break;
        case "tab":
            el += tabElement();
            break;
        case "br":
            el += charElement(")");
            break;
        case "bl":
            el += charElement("(");
            break;
        case "colon":
            el += charElement(":");
            break;
        case "and":
            el += andElement("and");
            break;
        default:
            return "";
    }
    el += "<img class='pv_el_delete' src='/static/img/close.svg'>";
    el += "</div>";
    return el;

}