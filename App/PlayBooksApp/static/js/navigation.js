/** 
function ident_url_placeholder(){
    return "REF";
}
*/
function ident_main_container(){
    return "#PlayBooks";
};
/** 
function ident_pb_nav_byID(id){
    return $("#pb-nav-"+id);
}
*/
/** 
function ident_hook_pbnav_pbpage(pageID){
    return $(".pbnav-pb-page[data-page="+pageID+"]");
}
*/
/** 
function ident_pb_nav_overview(){
    return $("#nav-overview-pbs");
}
*/
/** 
function ident_pb_main_overview(){
    return $("#pb-overview");
}
*/
function ident_pb_main(){
    return $("#pb-main");
}
function ident_modal_edit_page(){
    return $("#edit-page-modal");
}
function ident_prefetch_container(){
    return $("#prefetch-container");
}
function ident_prefetch_base(){
    return $("#pb-prefetch");
}
function ident_page_picksource_clk(){
    return $('.pb-page-picksource-clk');
}
function ident_all_input_types(){
    return 'input, select, textarea, div'
}
function ident_page_content_edit_selector(){
    return '[data-event=pageContentEdit]';
}
function ident_pbnav_page_byID(pageId){
    return $('.pb-page-clk[data-page='+pageId+']');
}
function pb_page_clk_sector(pageID){
    if( pageID ){ return '.pb-page-clk[data-page='+pageID+']' }
    else { return '.pb-page-clk' }
}
function ident_prefetch_update_btn(){
    return '[data-event=PrefetchUpdatePageBtn]'
}
function ident_close_prefetch_update_btn(){
    return '[data-event=ClosePrefetchUpdatePageBtn]'
}
function ident_pb_clk_selector(pbID){
    if( pbID ){ return '.pb-clk[data-pb='+pbID+']' }
    else { return '.pb-clk' };
}
function ident_prefetch_animation_container(){
    return '[data-hook=prefetch-animation]';
}
/** 
function ident_pbm_sec_container(){
    return $( ident_pb_main() ).find("[data-hook='pbm-sec-container']")
}
*/
/** 
function ident_pbm_loading(){
    return $("#pbm-loading");
}
*/
/** 
function iden_pbnav_section(sectionID){
    return $(".pb-section[data-section="+sectionID+"]")
}
*/
/** 
function ident_pbm_page_container(){
    return "[data-hook='pbm-page-container']";
}
*/
/** 
function ident_hook_sec_name(){
    return "[data-hook='pbm-sec-name']";
}
*/
/** 
function ident_hook_page_title(){
    return "[data-hook='pbm-page-title']";
}
*/
/** 
function ident_hook_page_lu(){
    return "[data-hook='pbm-page-last-update']";
}
*/
/*
function ident_form_add_page(){
    return "form#form-add-page";
}
*/
/*
function ident_hook_pbnav_pbpage(){
    return "[data-hook=pbnav-pb-page]"
}
*/
/*
function ident_form_addpage_title(){
    return "[name='page-title']"
}
*/
/** 
function url_get_pb(pbID){
    return 'api/pb/'+pbID;
}
*/
/** 
function url_get_page(pbID, pageID){
    return 'api/pb/'+pbID+'/page/'+pageID;
}
*/
/** 
function url_add_page(pbID, sectionID){
    return "pb/"+pbID+"/section/"+sectionID+"/new";
}
*/
/** 
function url_get_pb(pbID){
    return 'pb/'+pbID
}
*/

function refresh_sortable(updateCallback){
    $('.sortable').sortable({
        containment: "parent",
        update: function( event, ui ) {
            updateCallback(event, ui);
        }
    })
};

function refresh_update_toggles(){
    $('.update-toggle').bootstrapToggle({});
}

function trigger_prefetch_animation(container, showHide){
    if( showHide == 'show' ){
        $(container).find( ident_prefetch_animation_container() ).show()
    }else {
        $(container).find( ident_prefetch_animation_container() ).hide()
    }
}

function set_location_href_anchor(anchor){
    window.location.href = window.location.origin + anchor;
}

function set_playbook_nav_anchor(pbID){
    set_location_href_anchor("#" + pbID);
}

function set_playpage_nav_anchor(pageID){
    var pbAnchor = window.location.hash.split('#')[1];
    var newAnchors = "#" + pbAnchor + "#" + pageID;
    set_location_href_anchor(newAnchors);
}

function xhr_data(url, options, callbackSucc, callbackFail, callbackAlways){
    $.ajax(url, options).done(function(data, textStatus, jqxhr){
        if( callbackSucc != null ){
            callbackSucc(data, textStatus, jqxhr);
        }
    }).fail(function(jqXHR, textStatus, errorThrown){
        if( callbackFail != null  ){
            callbackFail(jqXHR, textStatus, errorThrown);
        }
    }).always(function(dataOrJQXhr, textStatus, jqxhr){
        if( callbackAlways != null ){
            callbackAlways(dataOrJQXhr, textStatus, jqxhr);
        }
    });
    /** 
    $.ajax({
        url: url,
        success: function(data, textStatus, jqXHR) {
            callbackSucc(data);
            },
        error: function(jqXHR, textStatus, errorThrown){
            callbackFail(jqXHR, textStatus, errorThrown);
        }
    });
    */
}

/** 
function append_pb_data(data){
    var secDOM = ident_pbm_sec_container();
    for(secID in data.sections){
        var secObj = data.sections[secID];
        var secEl = secDOM.clone();
        secEl.attr('data-section', secID);
        // set section content
        $(secEl).find( ident_hook_sec_name() ).text(secObj.name);
        var pageCon = $(secEl).find( ident_pbm_page_container() );
        for(pageID in secObj.pages){
            var pageObj = secObj.pages[pageID];
            var pageEl = pageCon.clone();
            $(pageEl).attr('data-page', pageID);
            $(pageEl).find( ident_hook_page_title() ).text(pageObj.title);
            $(pageEl).find( ident_hook_page_lu() ).text(pageObj.last_modified);
            $(secEl).append(pageEl);
        }
        $(ident_pb_main()).append(secEl);
        $(pageCon).remove();
        $(secDOM).remove();
    }
}
*/

function place_page(el, html_content){
    $(el).children().off();
    $(el).html(html_content);
}

function handle_fail_pb_data(jqXHR, textStatus, errorThrown){
    console.log("TODO Handle data loading fail");
    console.log("Error: "+ textStatus);
    console.log("Error: "+ errorThrown);
    console.log("Error: "+ jqXHR)
}

function handle_fail_page_data(jqXHR, textStatus, errorThrown){
    handle_fail_pb_data(jqXHR, textStatus, errorThrown);
}

/** 
function async_pb_display(pbID, fincallback){
    // TODO display loading screen
    url = url_get_pb(pbID);
    xhr_data(url, function(data){
        append_pb_data(data);
    }, function(jqXHR, textStatus, errorThrown){
        handle_fail_pb_data(jqXHR, textStatus, errorThrown);
    });
    // finish callback
    fincallback();
}
*/

function update_page_positions(event, ui){
    var eventContainer = $(event.target);
    var updateUrl = $(eventContainer).data('url-update-position');
    var positions = {
        'positions': []
    };
    $.each( (eventContainer).children(), function(index){
        var dataset = { 'page': $(this).data('page'), 'position': index } ;
        positions["positions"].push( dataset );
    });
    options = {
        type: "POST",
        data: JSON.stringify(positions),
        processData: false,
        contentType: 'application/json',
        cache: false,
        timeout: 600000,
    };
    xhr_data(updateUrl, options, function(data, textStatus, jqxhr){
        // success Callback
        // nothing to do
    }, function(jqXHR, textStatus, errorThrown){
        // Fail Callback
        handle_fail_pb_data(jqXHR, textStatus, errorThrown);
    });
}

function load_playbook(url){
    options = {
        type: "GET",
        processData: false,
        contentType: false,
        cache: false,
        timeout: 600000,
    };
    xhr_data(url, options, function(data, textStatus, jqxhr){
        // success Callback
        // clear target container
        var targetContainer = $(ident_main_container())
        //$(targetContainer).children().off()
        // add content
        var newMainDOM = $('<html></html>').append(data);
        var newMain = $(newMainDOM).find( ident_main_container() );
        // Replace DOM
        place_page(targetContainer, newMain);
        // enable sortable elements
        refresh_sortable(function(event, ui){
            update_page_positions(event, ui);
        });
    }, function(jqXHR, textStatus, errorThrown){
        // Fail Callback
        handle_fail_pb_data(jqXHR, textStatus, errorThrown);
    });

}


function playbook_clk(el){
    // Load Playbook Page
    // Replace DOM
    var url = $(el).data('url');
    var pbID = $(el).data('pb');
    load_playbook(url);
    // add to navigation
    if( pbID ){
        set_playbook_nav_anchor(pbID);
    }
    /** 
    var pbID= $(el).data('pb');
    var pbnav= ident_pb_nav_byID(pbID);
    // toggle views
    $(ident_pb_nav_overview()).slideToggle('slow');
    $(ident_pb_main_overview()).slideToggle('slow');
    $(pbnav).slideToggle('slow');
    $(ident_pb_main()).slideToggle('slow');
    // load pb pages
    async_pb_display(pbID, function(){
        $( ident_pbm_loading() ).hide();
    });
    */
}

function playbook_page_place(data, pageID){
    var pbpageDOM = $('<div></div>').append(data);
    // add handler for all failing images
    $.each( $(pbpageDOM).find('img'), function(index, imgEl){
        $(imgEl).on('error', function(event) {
            $(this).attr('data-action', 'replace-image');
            $(this).addClass('action data-replace');
            $(this).attr('data-page', pageID)
            //console.log("Could not load, ", this);
        })
    })
    var target = ident_pb_main()
    place_page(target, pbpageDOM);
    // check for updates
    $(pbpageDOM).find('[data-hook=update-status]').each(function(idx){
        get_update_status(this);
    })
}

function playbook_page_clk(el){
    var url = $(el).data('url');
    var pageID  = $(el).data('page');
    options = {
        type: "GET",
        processData: false,
        contentType: false,
        cache: false,
        timeout: 600000,
    };
    xhr_data(url, options, function(data, textStatus, jqxhr){
        // success Callback
        // clear target
        playbook_page_place(data, pageID);
        // add anchor
        set_playpage_nav_anchor(pageID);
    }, function(jqXHR, textStatus, errorThrown){
        // Fail Callback
        handle_fail_page_data(jqXHR, textStatus, errorThrown);
    });
}


function form_collect_data(form){
    var data = new FormData();
    var allInputTypes = ident_all_input_types();
    var all_inputs = $(form).find( allInputTypes );
    var file_input = $(form).find('[type=file]')[0];

    $.each(all_inputs, function(index, input){
        if( input== file_input){ data.append(input.name, file_input.files[0]); }
        else if ( $(input).attr('type')  == 'checkbox' ){ data.append( input.name, input.checked ) }
        else if (input.name) { data.append( input.name, input.value ) };
    });
    return data
}

function page_modal_submit_action(url, options, button, reloadUrl){
    xhr_data(url, options, function(data, textStatus, jqxhr){
        // success Callback
        // close modal
        $(button).closest('.modal').modal('hide');
        // replace DOM
        load_playbook( reloadUrl );
    }, function(jqXHR, textStatus, errorThrown){
        // Fail Callback
        //playpage_modal_add(jqXHR.responseText);//, pbID, urlNewPage, urlReloadPB);
        playpage_modal_update(jqXHR.responseText);
        // console.log(jqXHR, textStatus, errorThrown)
        // console.log(jqXHR.responseText);
        // foo = jqXHR;
        // target = $( ident_modal_edit_page() );
        // newModalEl = $('<div></div>').append(jqXHR.responseText);
        // newModalEl = $(newModalEl).find('.modal');
        // place_page(target, newModalEl);
        // $(target).children('.modal').modal('show')
    }, function(dataOrJQXhr, textStatus, jqxhr){
        // Always Callback
        //$(button).closest('.modal').modal('hide');
    });
}

function playbook_page_modal_submit(event, button){//, pbID, urlNewPage, urlReloadPB){
    //var action = $(button).data('action');
    var targetUrl = $(button).data('url');
    var reloadUrl = $(button).data('url-reloadpb');
    var action = $(button).data('action');
    // var url = '';
    // if( action == 'new' ) url = urlNewPage;
    // else url = $(button).data('url');
    
    var form = $(button).data('form');
    //var pageID = $(button).data('page');
    
    // Send POST request
    var data = form_collect_data(form)

    options = {
        type: "POST",
        enctype: 'multipart/form-data',
        data: data,
        processData: false,
        contentType: false,
        cache: false,
        timeout: 600000,
    };
    
    if( action == 'delete' ){
        // Confirm
        $.confirm({
            title: 'Are You Sure?',
            content: "If the pages exists in another Playbook or Section it stays there, if not it is deleted",
            theme: 'supervan',
            buttons: {
                cancel: function () {
                    // just go on
                },
                confirm: function () {
                    page_modal_submit_action(targetUrl, options, button, reloadUrl);
                }
            }
        });
    }
    else {
        page_modal_submit_action(targetUrl, options, button, reloadUrl);
    }
    
    /**
    done(function(data, textStatus, jqxhr){
        callbackSucc(data, textStatus, jqxhr);
    }).fail(function(jqXHR, textStatus, errorThrown){
        callbackFail(jqXHR, textStatus, errorThrown);
    }).always(function(dataOrJQXhr, textStatus, jqxhr){
        
    });
    */

    
    /** 
    var jqxhr = $.post(url, $(form).serialize(), function(data, textStatus, jqxhr){
        // TODO add success banner
    }).fail(function(jqXHR, textStatus, errorThrown){
        handle_fail_page_data(jqXHR, textStatus, errorThrown);
    }).always(function(){
        // close modal
        $(button).closest('.modal').modal('hide');
        // replace DOM
        load_playbook( urlReloadPB );
    });
    */
    return false
}

function playpage_modal_select_source(){
    // preselct Source
    var sourceClkElements = ident_page_picksource_clk();
    $( sourceClkElements ).each(function(idx, el){
        if( $(el).data('selected') ){
            $(el).click();
        }
    });
}
function playpage_modal_update(respdata){
    var targetModal = $( ident_modal_edit_page() );
    var updateModal = $('<div></div>').append(respdata);
    var targetModalContent = $(targetModal).find('.modal-content')
    var updateContent = $(updateModal).find('.modal-content')
    place_page(targetModalContent, updateContent);
    playpage_modal_select_source();
}

function playpage_modal_add(respdata){//, pbID, urlNewPage, urlReloadPB){
    var target = $( ident_modal_edit_page() );
    // remove any preexisting events
    //$(target).off()
    // add new content
    var newModalEl = $('<div></div>').append(respdata);
    var newModalEl = $(newModalEl).find('.modal');
    
    place_page(target, newModalEl);
    playpage_modal_select_source();
    // // prevent submit
    // $(newModalEl).on('click', '[type=submit]', function(event){
    //     event.preventDefault();
    //     playbook_page_modal_submit(event, this, pbID, urlNewPage, urlReloadPB);
    //     return false;
    // });
    
    // refresh select picker
    $('.selectpicker').selectpicker('refresh');
    // enable update toggle
    refresh_update_toggles();
    // Remove all modal backdrops but one
    //$('.modal-backdrop').remove()
    // show modal
    $(target).children('.modal').modal('show');
};

function playbook_page_action_clk(el, pbID, urlEditForm, urlNewPage, urlReloadPB){
    //var target = $( ident_modal_edit_page() );
    /**
     var action = $(el).data('action');
    var url = $(target).data('url');
    var urlPlaceholder = ident_url_placeholder();
     
    var newUrlVal = '';
    if( action == 'new' ){
        newUrlVal = 'new';
    }else {
        newUrlVal = $(el).data('page')
    }
    var regexMatch = new RegExp(urlPlaceholder+'$');
    var newUrl = url.replace(regexMatch, newUrlVal);
    */
    options = {
        type: "GET",
        enctype: 'multipart/form-data',
        processData: false,
        contentType: false,
        cache: false,
        timeout: 600000,
    };
    xhr_data(urlEditForm, options, function(data, textStatus, jqxhr){
        // success Callback
        playpage_modal_add(data);//, pbID, urlNewPage, urlReloadPB);
        // newModalEl = $('<div></div>').append(data);
        // newModalEl = $(newModalEl).find('.modal');
        // place_page(target, newModalEl);

        // prevent submit
        // $(newModalEl).on('click', '[type=submit]', function(event){
        //     event.preventDefault();
        //     playbook_page_modal_submit(event, this, pbID, urlNewPage, urlReloadPB);
        //     return false;
        // });
        // // show modal
        // $(target).children('.modal').modal('show');
    }, function(jqXHR, textStatus, errorThrown){
        // Fail Callback
        handle_fail_page_data(jqXHR, textStatus, errorThrown);
    });
};

function playpage_edit_src_change(pressedButton){
    var sourceType = $(pressedButton).data('source-type');
    var sourceFieldSelector = $(pressedButton).data('source-field');
    var buttonSelector = $(pressedButton).data('button-selector');
    var sourceField = $(sourceFieldSelector);
    var targetFieldsStr = $(pressedButton).data('target-fields');
    var targetFieldIDs = targetFieldsStr.split(',').filter(function(v){return v!==''});
    var targetForm = $(pressedButton).data('form');

    // set source type
    $(sourceField).val(sourceType);
    // hide not needed elements
    var allInputTypes = ident_all_input_types()
    var allInputs = $(targetForm).find( allInputTypes ).parents('.input-group');
    var requiredInputs = targetFieldIDs.filter(function(v){return v!==''});
    var fadeSpeed = 700;
    $(targetForm).children('.modal-body').fadeTo(fadeSpeed, 0, function(){
        $(allInputs).hide();
        $.each(targetFieldIDs, function(idx, fieldID){
            var selector = "#"+fieldID;
            $(selector).parents('.input-group').show();
        });
        $(targetForm).children('.modal-body').fadeTo(fadeSpeed, 1.0)
    });
    // remove active class from other buttons
    $(buttonSelector).removeClass('active');
    // add active class to
    $(pressedButton).addClass('active');
}

/** 
function prepare_addpgae_modal(modal, pressedButton){
    var pbID = $(pressedButton).data('pb')
    var sectionID = $(pressedButton).data('section')
    var form = $(modal).find( ident_form_add_page() )
    var actionURL = url_add_page(pbID, sectionID);
    form.attr('action', actionURL);
    $(form).submit(function(event){
        // TODO add loading animation
        event.preventDefault();
        // TODO Determine success or failure
        $.post(actionURL, $(this).serialize(), function(res){
            var new_page_id = res;
            // add page to section
            var curr_section = iden_pbnav_section(sectionID); 
            var last_secpage = $(curr_section).find( ident_hook_pbnav_pbpage() ).last();
            var new_page = $(last_secpage).clone();
            var new_page_title = $(form).find( ident_form_addpage_title() ).val()
            console.log(curr_section, last_secpage, new_page, new_page_title);
            $(new_page).attr('data-page', new_page_id);
            // TODO span is removed here, keep it
            $(new_page).first('span').text(new_page_title);
            $(curr_section).append(new_page)
            // close modal
            $(modal).modal('hide');
            // reset form
            $(form).trigger('reset');
            // trigger click on the new page
            $(new_page).trigger('click');
            boo = $(new_page);
            // Don't forget to hide the loading indicator!
        });
    
        return false; // prevent default action
    });
}
*/

function animate_prefetch_container(hideShow){
    var pretchContainer = ident_prefetch_container();
    $(pretchContainer).animate({width: hideShow}, 700, 'linear');
}

function show_prefetch_data(data){
    var replaceTarget = ident_prefetch_base();
    var newModalEl = $('<html></html>').append(data);
    var newContent = $(newModalEl).html();
    place_page(replaceTarget, newContent);
    animate_prefetch_container('show');
}

function prefetch_url(apiEndpoint, changedInput){
    var url = apiEndpoint;
    var form = $(changedInput).closest("form");
    
    // show prefetch animation
    trigger_prefetch_animation(form, 'show');
    // Send POST request
    var data = form_collect_data(form);

    options = {
        type: "POST",
        enctype: 'multipart/form-data',
        data: data,
        processData: false,
        contentType: false,
        cache: false,
        timeout: 600000,
    };
    xhr_data(url, options, function(data, textStatus, jqxhr){
        // success Callback
        // show prefetch data
        show_prefetch_data(data);        
    }, function(jqXHR, textStatus, errorThrown){
        // Fail Callback
        //playpage_modal_add(jqXHR.responseText);//, pbID, urlNewPage, urlReloadPB);
        playpage_modal_update(jqXHR.responseText);
        // console.log("Could not load page. Status: ",  textStatus)
        // handle_fail_page_data(jqXHR, textStatus, errorThrown);
    }, function(dataOrJQXhr, textStatus, jqxhr){
        // Always Callback
        // show prefetch animation
        trigger_prefetch_animation(form, 'hide');
    });
    
    
    
    
    // options = {
    //     type: "GET",
    //     processData: false,
    //     contentType: false,
    //     cache: false,
    //     timeout: 600000,
    // };
    // xhr_data(url, options, function(data, textStatus, jqxhr){
        
    // }, function(jqXHR, textStatus, errorThrown){
    //     // Fail Callback
    //     console.log("Could not load page. Status: ",  textStatus)
    //     handle_fail_page_data(jqXHR, textStatus, errorThrown);
    // });
    
}

function add_to_element_update_queue(updateElement){
    if( elementUpdateQueue.indexOf(updateElement) == -1 ){
        elementUpdateQueue.push(updateElement);
    }
};

function update_elements(){
    var i = elementUpdateQueue.length
    while (i--) {
        element = elementUpdateQueue.pop()
        page_edit_update(element);
    }
};

function collectAllNodesFor(element, containerArray) {
    for (var child= element.firstChild; child!==null; child= child.nextSibling) {
        containerArray.push(child);
        collectAllNodesFor(child, containerArray);
    }
}

function page_edit_update(updateElement){
    // update related form field
    var targetFormFieldSelector = $(updateElement).data('target');
    var targetFormField = $('#'+targetFormFieldSelector);
    //var elementContent = $(updateElement).text();
    var prefetchURL = $(targetFormField).data('url-prefetch');
    // get contents
    var formContent = ""
    var containerArray = [];
    collectAllNodesFor(updateElement, containerArray);
    // control vars
    var suppressBR = false;
    var newLineEntered = false;
    $.each( containerArray, function(idx){
        if( this ){
            // HTML elements aka. tags
            if( this.nodeType == 1){
                if( this.tagName == "IMG" ){
                    formContent += this.outerHTML;
                }
                else if ( this.tagName == "BR" && !suppressBR ){
                    formContent += "\<br\>";
                }
                else if ( this.tagName == "P" && !newLineEntered ){
                    // p tag, but no previous newLine, meaning we need to add one
                    formContent += "\n";
                }
            }
            // Text elements
            else if( this.nodeType == 3 && this.wholeText){
                var text = this.wholeText;
                var lineFeeds = text.match(/\n/g)||[];
                if( lineFeeds > 0 ){
                    $.each(lineFeeds, function(idx){
                        formContent += "\n";
                    });
                    // newline entered
                    newLineEntered = true;
                }
                else {
                    // add plain text
                    formContent += text;
                    // content entered, not a newline
                    newLineEntered = false;
                    /// ``` indicates start of code segment, if supress already set we completed code segtion
                    if( text == "```" && suppressBR ){ suppressBR = false; formContent += "\n"; }
                    /// ``` indicates start of code segment, otherwise <br> would be HTML encoded
                    if( text.startsWith('```') ){ suppressBR = true; }
                }
            }
            else if( this.wholeText ) {
                //formContent += this.wholeText
            }
            
        }
        // elementCopy = $(this).clone();
        // // get rid of span elements
        // $.each($(elementCopy).children(), function(idx){ 
        //     if( $(this).is('span') ){
        //         formContent += $(this).html(); 
        //         $(this).remove(); 
        //     }
        // })
        // formContent += $(elementCopy).html() + "\n\r";
    });
    // update form field
    $(targetFormField).val(formContent);
    // Prefetch 
    prefetch_url(prefetchURL, targetFormField);
}

function getCaretPosition(element) {
    var ie = (typeof document.selection != "undefined" && document.selection.type != "Control") && true;
    var w3 = (typeof window.getSelection != "undefined") && true;
    var caretOffset = 0;
    if (w3) {
        var range = window.getSelection().getRangeAt(0);
        var preCaretRange = range.cloneRange();
        preCaretRange.selectNodeContents(element);
        preCaretRange.setEnd(range.endContainer, range.endOffset);
        caretOffset = preCaretRange.toString().length;
    } else if (ie) {
        var textRange = document.selection.createRange();
        var preCaretTextRange = document.body.createTextRange();
        preCaretTextRange.moveToElementText(element);
        preCaretTextRange.setEndPoint("EndToEnd", textRange);
        caretOffset = preCaretTextRange.text.length;
    }
    return caretOffset;
}

function page_edit_insert_img(base64IMG){
    var targetSelector = ident_page_content_edit_selector();
    var target = $(targetSelector);
    var cursorPos = getCaretPosition( $(target).get(0) );
    // buffer text
    var image = '<p><img src="'+base64IMG+'"></p>';
    var sel, range, node;
    if (window.getSelection) {
        sel = window.getSelection();
        if (sel.getRangeAt && sel.rangeCount) {
        range = window.getSelection().getRangeAt(0);
        node = range.createContextualFragment(image);
        range.insertNode(node);
        }
    } else if (document.selection && document.selection.createRange) {
        document.selection.createRange().pasteHTML(image);
    }
}

function page_content_submit(button){
    var targetForm = $(button).data('target');
    var targetUrl = $(button).data('url');
    var pageID = $(button).data('page');
    var formData = form_collect_data(targetForm);
    // send update request
    options = {
        type: "POST",
        enctype: 'multipart/form-data',
        data: formData,
        processData: false,
        contentType: false,
        cache: false,
        timeout: 600000,
    };
    xhr_data(targetUrl, options, function(data, textStatus, jqxhr){
        // success Callback
        // hide prefetch container
        animate_prefetch_container('hide');
        // update page
        playbook_page_place(data, pageID);
        // update title
        pbnav_update_page_title(pageID);
    }, function(jqXHR, textStatus, errorThrown){
        // Fail Callback
        handle_fail_page_data(jqXHR, textStatus, errorThrown);
    }, function(dataOrJQXhr, textStatus, jqxhr){
        // Always Callback
        
    });
    
}

function pbnav_update_page_title(pageID){
    var updateElement = ident_pbnav_page_byID(pageID);
    var url = $(updateElement).data('url-update-title');
    // send update request
    options = {
        type: "GET",
        processData: false,
        contentType: false,
        cache: false,
        timeout: 600000,
    };
    xhr_data(url, options, function(data, textStatus, jqxhr){
        // success Callback
        var newTitle = data.title;
        $(updateElement).find('[data-attribute=title]').text(newTitle);
    }, function(jqXHR, textStatus, errorThrown){
        // Fail Callback
        handle_fail_page_data(jqXHR, textStatus, errorThrown);
    }, function(dataOrJQXhr, textStatus, jqxhr){
        // Always Callback
        
    });
}

function add_section_submit(form){
    var url = $(form).attr('action');
    var reloadUrl = $(form).data('reload-url');
    var method = $(form).attr('method');
    var data = form_collect_data(form);
    // send update request
    options = {
        type: method,
        enctype: 'multipart/form-data',
        data: data,
        processData: false,
        contentType: false,
        cache: false,
        timeout: 600000,
    };
    xhr_data(url, options, function(data, textStatus, jqxhr){
        // success Callback
        load_playbook(reloadUrl);
    }, function(jqXHR, textStatus, errorThrown){
        // Fail Callback
        handle_fail_page_data(jqXHR, textStatus, errorThrown);
    }, function(dataOrJQXhr, textStatus, jqxhr){
        // Always Callback
        
    });
}

function delete_section(button){
    var url = $(button).data('url');
    var reloadUrl = $(button).data('reload-url');
    // Options
    options = {
        type: 'GET',
        processData: false,
        contentType: false,
        cache: false,
        timeout: 600000,
    };
    // Confirm
    $.confirm({
        title: 'Are You Sure?',
        content: 'Contained pages are deleted if not referenced elsewhere',
        theme: 'supervan',
        buttons: {
            cancel: function () {
                // just go on
            },
            confirm: function () {
                // send update request
                xhr_data(url, options, function(data, textStatus, jqxhr){
                    // success Callback
                    load_playbook(reloadUrl);
                }, function(jqXHR, textStatus, errorThrown){
                    // Fail Callback
                    handle_fail_page_data(jqXHR, textStatus, errorThrown);
                }, function(dataOrJQXhr, textStatus, jqxhr){
                    // Always Callback
                    
                });
            }
        }
    });
}

function prefetch_update_page_from_source(updateButton){
    var url = $(updateButton).data('url');
    options = {
        type: 'GET',
        processData: false,
        contentType: false,
        cache: false,
        timeout: 600000,
    };
    xhr_data(url, options, function(data, textStatus, jqxhr){
        // success Callback
        // show prefetch data
        show_prefetch_data(data);
        // hide prefetch button
        $(updateButton).hide();
        // show close button
        $(ident_close_prefetch_update_btn()).show();
    }, function(jqXHR, textStatus, errorThrown){
        // Fail Callback
        handle_fail_page_data(jqXHR, textStatus, errorThrown);
    }, function(dataOrJQXhr, textStatus, jqxhr){
        // Always Callback
        //$(statusElement).text(dataOrJQXhr);
    });
}

function update_page_from_source(updateButton){
    var url = $(updateButton).data('url');
    var pageID = $(updateButton).data('page');
    // send update request
    options = {
        type: 'GET',
        processData: false,
        contentType: false,
        cache: false,
        timeout: 600000,
    };
    xhr_data(url, options, function(data, textStatus, jqxhr){
        // success Callback
        // simulate page click
        var pageElementSelctor = pb_page_clk_sector(pageID);
        var pageClickEl = $(pageElementSelctor);
        playbook_page_clk(pageClickEl);
        // hide animation container
        animate_prefetch_container('hide');
    }, function(jqXHR, textStatus, errorThrown){
        // Fail Callback
        handle_fail_page_data(jqXHR, textStatus, errorThrown);
    }, function(dataOrJQXhr, textStatus, jqxhr){
        // Always Callback
        //$(statusElement).text(dataOrJQXhr);
    });
}

function get_update_status(statusElement){
    var url = $(statusElement).data('url');
    // send update request
    options = {
        type: 'GET',
        processData: false,
        contentType: false,
        cache: false,
        timeout: 600000,
    };
    xhr_data(url, options, function(data, textStatus, jqxhr){
        // success Callback
        // show status
        if( textStatus == 'notmodified'  ){
            $(statusElement).find('.status-notmodified').show();
        }else {
            $(statusElement).find('.status-update').show();
        }
    }, function(jqXHR, textStatus, errorThrown){
        // Fail Callback
        $(statusElement).find('.status-error').show();
    }, function(dataOrJQXhr, textStatus, jqxhr){
        // Always Callback
    });

}

function get_server_file_options(button){
    var apiURL = $(button).data('url-fileoptions');
    var form = $(button).closest("form");
    var updateTargetID = $(button).data('update-target');
    var updateTarget = $('#'+updateTargetID);

    // Send POST request
    var data = form_collect_data(form);
    options = {
        type: "POST",
        enctype: 'multipart/form-data',
        data: data,
        processData: false,
        contentType: false,
        cache: false,
        timeout: 600000,
    };
    xhr_data(apiURL, options, function(data, textStatus, jqxhr){
        // success Callback
        place_page(updateTarget, data);
        $(updateTarget).selectpicker('refresh');
        $(updateTarget).show();
    }, function(jqXHR, textStatus, errorThrown){
        // Fail Callback
        
    }, function(dataOrJQXhr, textStatus, jqxhr){
        // Always Callback
        
    });
}

function search_playbooks(searchInput){
    var url = $(searchInput).data('url');
    var updateTargetSelctor = $(searchInput).data('update-target');
    var updateTarget = $(updateTargetSelctor);
    var formSelector = $(searchInput).data('form'); 
    var form = $(formSelector);
    var data = form_collect_data(form);
    
    options = {
        type: "POST",
        enctype: 'multipart/form-data',
        data: data,
        processData: false,
        contentType: false,
        cache: false,
        timeout: 600000,
    };
    xhr_data(url, options, function(data, textStatus, jqxhr){
        // success Callback
        // place search results
        place_page(updateTarget, data);
        
    }, function(jqXHR, textStatus, errorThrown){
        // Fail Callback
        
    }, function(dataOrJQXhr, textStatus, jqxhr){
        // Always Callback
        
    });
}

function clk_pb_n_page(pbID, pageID){
    var pbSelector = ident_pb_clk_selector(pbID);
    var pageSelector = pb_page_clk_sector(pageID);
    if( $.isNumeric(pbID) ){
        // click pb
        $(pbSelector).click();
    }
    // wait 1 sec and click page
    setTimeout(function(){
        if( $.isNumeric(pageID) ) {
            $(pageSelector).click();
        }
    }, 500);
}

var elementUpdateQueue = []

$(document).ready(function(){
    // Event bindings
    $(document).on('click', ident_pb_clk_selector(null), function(){
        playbook_clk(this);
    });
    $(document).on('click', pb_page_clk_sector(null), function(event){
        playbook_page_clk(this);
        animate_prefetch_container('hide');
    });
    $(document).on('click', '.pb-page-edit-clk', function(){
        var pbID = $(this).data('pb');
        var urlReloadPB = $(this).data('url-reloadpb');
        var urlEditForm = $(this).data('url-editform');
        playbook_page_action_clk(this, pbID, urlEditForm, null, urlReloadPB);
    });
    $(document).on('click', '.pb-page-add-clk', function(){
        var pbID = $(this).data('pb');
        var urlNewPage = $(this).data('url-addpage');
        var urlEditForm = $(this).data('url-editform');
        var urlReloadPB = $(this).data('url-reloadpb');
        playbook_page_action_clk(this, pbID, urlEditForm, urlNewPage, urlReloadPB);
    });
    $(document).on('click', '.pb-page-picksource-clk', function(){
        playpage_edit_src_change(this);
    });
    
    //
    // Section events
    //
    // add section
    $(document).on('submit', '#form_new_section', function(event){
        event.preventDefault();
        // disable button
        $(this).prop('disabled', true);
        add_section_submit(this);
        return false;
    });
    // delete section
    $(document).on('click', '.pb-section [data-action=delete]', function(event){
        delete_section(this);
    });
    // 
    // -----------

    //
    // Playbook events
    //
    // delete playbook
    $(document).on('submit', '.form_delete_playbook', function(event){
        if( !$(this).data('confirmed') ){
            event.preventDefault();
            el = $(this);
            $.confirm({
                title: 'Are You Sure?',
                content: "If pages of this playbook exists in another Playbook they stays there, otherwise they are deleted",
                theme: 'supervan',
                buttons: {
                    cancel: function () {
                        // just go on
                    },
                    confirm: function () {
                        $(el).data('confirmed', true);
                        $(el).submit();
                    }
                }
            });
            return false;
        }
    });
    // 
    // -----------

    $(document).on('change', '[data-event=urlPrefetch]', function(e){
        var apiEndpoint = $(this).data('url-prefetch');
        //var targetURL = $(this).val();
        prefetch_url(apiEndpoint, this);
    });

    $(document).on('change', '[data-event=diskFolder]', function(e){
        get_server_file_options(this);
    });

    //
    // Page Content Eventns
    //
    $(document).on('click', '[data-event=pageContentShow]', function(e){
        // toggle views
        $('[data-hook=pageContentEdit]').toggle();
        refresh_update_toggles();
    });

    $(document).on('click', '[data-event=pageContentHide]', function(e){
        // toggle views
        $('[data-hook=pageContentEdit]').toggle();
        animate_prefetch_container('hide');
    });

    $(document).on('click', '[data-action=pageContentUpdate]', function(){
        page_content_submit(this);
        animate_prefetch_container('hide');
    });
    // Update Page From Source
    $(document).on('click', '[data-event=UpdatePageBtn]', function(){
        update_page_from_source(this);
    });
    // Prefetch Update Page From Source
    $(document).on('click', ident_prefetch_update_btn(), function(){
        prefetch_update_page_from_source(this);
    });
    // Hide Prefetch Window
    $(document).on('click', ident_close_prefetch_update_btn(), function(){
        // hide prefetch container
        animate_prefetch_container('hide');
        // hide close button
        $(this).hide();
        // show update prefetch button
        $(ident_prefetch_update_btn()).show();
    });
    // 
    // -----------
    

    $(document).on('keyup', ident_page_content_edit_selector(), function(e){
        var container = $(this).data('container');
        if( container ){
            trigger_prefetch_animation($(container), 'show');
        }
        add_to_element_update_queue(this);
    });
    
    //
    // Modal events
    //
    var pageModal = ident_modal_edit_page()
    $(pageModal).on('click', '.submit-action', function(event){
        event.preventDefault();
        //var urlNewPage = $(this).data('url-addpage');
        //var urlReloadPB = $(this).data('url-reloadpb');
        
        //console.log("Submitting New Modal", "NewPageURL ", urlNewPage, "UrlReloadPage ", urlReloadPB);
        // disable button
        $(this).prop('disabled', true);
        playbook_page_modal_submit(event, this);//, null, urlNewPage, urlReloadPB);
        return false;
    });
    $(document).on('hide.bs.modal', function (event) {
        animate_prefetch_container('hide');
    })
    // 
    // -----------


    //
    // Close Container
    //
    $(document).on('click', '.close-prefetch-container', function(e){
        animate_prefetch_container('hide');
    });
    // 
    // -----------

    //
    // search function
    //
    $(document).on('submit', '#form_search', function(e){
        e.preventDefault();
        return false;
    });
    $(document).on('keyup', '#form_search_input', function(e){
        search_playbooks(this);
    });
    $(document).on('click', '.form_search_result', function(e){
        // anchor tags places by a-tag
        setInterval(function(){
            location.reload();
        }, 300)
        // reload page
    });
    // 
    // -----------

    //
    // anchor navigation
    //
    if( window.location.hash.split('#').pop() ){
        var IDs = window.location.hash.split('#');
        var pbID = IDs[1];
        var pageID = IDs[2];
        clk_pb_n_page(pbID, pageID);
    }
    // 
    // -----------

    // start element update queue
    update_element_interval = setInterval(function(){
        update_elements();
    }, 3000);
});

/**
 * This handler retrieves the images from the clipboard as a base64 string and returns it in a callback.
 * 
 * @param pasteEvent 
 * @param callback 
 */
function retrieveImageFromClipboardAsBase64(pasteEvent, callback, imageFormat){
	if(pasteEvent.clipboardData == false){
        if(typeof(callback) == "function"){
            callback(undefined);
        }
    };

    var items = pasteEvent.clipboardData.items;

    if(items == undefined){
        if(typeof(callback) == "function"){
            callback(undefined);
        }
    };

    for (var i = 0; i < items.length; i++) {
        // Skip content if not image
        if (items[i].type.indexOf("image") == -1) continue;
        // Retrieve image on clipboard as blob
        var blob = items[i].getAsFile();

        // Create an abstract canvas and get context
        var mycanvas = document.createElement("canvas");
        var ctx = mycanvas.getContext('2d');
        
        // Create an image
        var img = new Image();

        // Once the image loads, render the img on the canvas
        img.onload = function(){
            // Update dimensions of the canvas with the dimensions of the image
            mycanvas.width = this.width;
            mycanvas.height = this.height;

            // Draw the image
            ctx.drawImage(img, 0, 0);

            // Execute callback with the base64 URI of the image
            if(typeof(callback) == "function"){
                callback(mycanvas.toDataURL(
                    (imageFormat || "image/png")
                ));
            }
        };

        // Crossbrowser support for URL
        var URLObj = window.URL || window.webkitURL;

        // Creates a DOMString containing a URL representing the object given in the parameter
        // namely the original Blob
        img.src = URLObj.createObjectURL(blob);
    }
}

// PLAIN JS
window.addEventListener("paste", function(e){
    // textSource = document.getElementById("id_text_source");
    // Handle the event
    retrieveImageFromClipboardAsBase64(e, function(imageDataBase64){
        // If there's an image, open it in the browser as a new window :)
        if(imageDataBase64){
            // data:image/png;base64,iVBORw0KGgoAAAAN......
            // imgTag = document.createElement("img");
            // imgTag.src = imageDataBase64;
            // foo = imageDataBase64;
            page_edit_insert_img(imageDataBase64);
            //pbMain.prepend(imgTag);
            //insertAtCursor(textSource, imgTag);
            //window.open(imageDataBase64);
        }
    });
}, false);