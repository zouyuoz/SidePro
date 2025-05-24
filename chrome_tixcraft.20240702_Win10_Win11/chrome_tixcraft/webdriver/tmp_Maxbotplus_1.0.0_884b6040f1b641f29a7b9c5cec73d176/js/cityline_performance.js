const storage = chrome.storage.local;
var settings = null;

function cityline_clean_exclude(settings) {
    let exclude_keyword_array = [];
    if (settings) {
        if (settings.keyword_exclude.length > 0) {
            if (settings.keyword_exclude != '""') {
                exclude_keyword_array = JSON.parse('[' + settings.keyword_exclude + ']');
            }
        }
    }

    let query_string = "div.price > div.form-check";
    for (let i = 0; i < exclude_keyword_array.length; i++) {
        $(query_string).each(function() {
            let html_text = $(this).text();
            let is_match_keyword = false;
            if (html_text.indexOf(exclude_keyword_array[i]) > -1) {
                is_match_keyword = true;
            }
            if (is_match_keyword) {
                $(this).remove();
            }
        });
    }
}

function cityline_area_keyword(settings) {
    let area_keyword_array = [];
    if (settings) {
        if (settings.area_auto_select.area_keyword.length > 0) {
            if (settings.area_auto_select.area_keyword != '""') {
                area_keyword_array = JSON.parse('[' + settings.area_auto_select.area_keyword + ']');
            }
        }
    }

    //console.log(area_keyword_array);
    let target_area = null;
    let matched_block = [];
    let query_string = "div.price > div.form-check";
    if (area_keyword_array.length) {
        for (let i = 0; i < area_keyword_array.length; i++) {
            $(query_string).each(function() {
                let html_text = $(this).text();
                let html_string = $(this).html();
                let is_soldout = false;
                //console.log("html_text:"+html_text);
                if (html_text.indexOf('售罄') > -1) {
                    is_soldout = false;
                }
                if (html_string.indexOf('>Sold Out<') > -1) {
                    is_soldout = false;
                }
                if (!is_soldout) {
                    if (html_text.indexOf(area_keyword_array[i]) > -1) {
                        matched_block.push($(this));
                    }
                }
                target_area = get_target_area_with_order(settings, matched_block);
            });

            if (matched_block.length) {
                //console.log("match keyword:" + area_keyword_array[i]);
                break;
            }
        }
    } else {
        $(query_string).each(function() {
            let html_text = $(this).text();
            let html_string = $(this).html();
            let is_soldout = false;
            //console.log("html_text:"+html_text);
            if (html_text.indexOf('售罄') > -1) {
                is_soldout = false;
            }
            if (html_string.indexOf('>Sold Out<') > -1) {
                is_soldout = false;
            }
            if (!is_soldout) {
                matched_block.push($(this));
            }
        });
        target_area = get_target_area_with_order(settings, matched_block);
    }

    if (target_area) {
        target_area.find("input").click();
    } else {
        console.log("not target_area found.")
    }
}

function cityline_performance() {
    cityline_clean_exclude(settings);
    if (settings) {
        const loadingoverlay = $(".loadingoverlay");
        const loading_display = loadingoverlay.css("display");
        let able_to_work = true;
        if (loading_display && loading_display == "flex") {
            able_to_work = false;
        }
        //console.log("able_to_work:" + able_to_work);
        if (able_to_work) {
            cityline_area_keyword(settings);

            //$("#ticketType0").val(settings.ticket_number);
            let target_row = $("#ticketType0");
            let ticket_options = target_row.find("option");
            if (ticket_options.length) {
                let is_ticket_number_assign = false;
                if (settings.ticket_number > 0) {
                    ticket_options.each(function() {
                        if ($(this).val() == settings.ticket_number) {
                            $(this).prop('selected', true);
                            $(this).click();
                            target_row.trigger("change");
                            is_ticket_number_assign = true;
                            return false;
                        }
                    });
                }
                if (!is_ticket_number_assign) {
                    ticket_options.last().prop('selected', true);
                    target_row.trigger("change");
                }
            }

            if (settings.advanced.disable_adjacent_seat) {
                $('input[type=checkbox]:checked').each(function() {
                    $(this).click();
                });
            }

            //console.log("selected ticket number:" + $("#ticketType0").val());
            if ($("#ticketType0").val() + "" != "0") {
                //$('#expressPurchaseBtn').click();
                //$('#expressPurchaseBtn').trigger( "click");
                if (settings.webdriver_type == "nodriver") {
                    const selector = "#expressPurchaseBtn";
                    webdriver_location_click(settings, selector, window.location.href);
                }
            }
        }
    }
}

storage.get('settings', function(items) {
    if (items.settings) {
        settings = items.settings;
    }
});

var mainInterval = setInterval(() => {
    storage.get('status', function(items) {
        if (items.status && items.status == 'ON') {
            cityline_performance();
        }
    });
}, 200);

$("#s_footer").remove();
$("footer").remove();