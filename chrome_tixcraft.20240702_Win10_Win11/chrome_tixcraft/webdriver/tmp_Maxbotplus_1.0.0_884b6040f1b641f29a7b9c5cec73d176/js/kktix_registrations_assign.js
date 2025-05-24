// PS: this script is not activated NOW, due to detected.

function kktix_verification_conditions(settings) {
    let is_text_sent = false;
    let user_guess_string_array = [];
    if (settings) {
        if (settings.advanced.user_guess_string.length > 0) {
            if (settings.advanced.user_guess_string != '""') {
                user_guess_string_array = JSON.parse('[' + settings.advanced.user_guess_string + ']');
            }
        }
    }

    let target_row = null;
    let all_row = $("div.control-group > div.controls > label > input[type='text']");
    if (all_row.length > 0 && user_guess_string_array.length > 0) {
        //console.log("input count:" + all_row.length);
        let travel_index = 0;
        all_row.each(function() {
            let current_index = all_row.index(this);
            //console.log("current_index:" + current_index);
            if (current_index + 1 <= user_guess_string_array.length) {
                //console.log("input data:" + user_guess_string_array[current_index]);
                $(this).val(user_guess_string_array[current_index]);
                is_text_sent = true;
            }
        });
    }

    return is_text_sent;
}

function kktix_ticket_unit_clean_exclude(exclude_keyword_array) {
    for (let i = 0; i < exclude_keyword_array.length; i++) {
        $("div.ticket-unit").each(function() {
            let html_text = $(this).text();
            //console.log("html:"+html_text);
            if (html_text.indexOf(exclude_keyword_array[i]) > -1) {
                $(this).remove();
            }
        });
    }
}

function kktix_area_keyword(settings) {
    let area_keyword_array = [];
    if (settings) {
        if (settings.area_auto_select.area_keyword.length > 0) {
            if (settings.area_auto_select.area_keyword != '""') {
                area_keyword_array = JSON.parse('[' + settings.area_auto_select.area_keyword + ']');
            }
        }
    }
    kktix_area_keyword_ticket_number(settings, area_keyword_array, settings.ticket_number);
}

function kktix_area_keyword_ticket_number(settings, area_keyword_array, ticket_number) {
    // console.log(area_keyword_array);
    let target_area = null;
    let matched_block = [];
    let query_string = "div.ticket-unit";
    if (area_keyword_array.length) {
        for (let i = 0; i < area_keyword_array.length; i++) {
            $(query_string).each(function() {
                let html_text = $(this).text();
                if (html_text.indexOf(area_keyword_array[i]) > -1) {
                    matched_block.push($(this));
                }
                target_area = get_target_area_with_order(settings, matched_block);
            });

            if (matched_block.length) {
                console.log("match keyword:" + area_keyword_array[i]);
                break;
            }
        }
    } else {
        $(query_string).each(function() {
            matched_block.push($(this));
        });
        target_area = get_target_area_with_order(settings, matched_block);
    }

    if (target_area) {
        let first_node = target_area.find(":first-child");
        let link_id = first_node.attr("id");
        //console.log("link_id: " + link_id);
        if (link_id) {
            let seat_inventory_key = link_id.split("_")[1];
            //console.log("seat_inventory_key:"+seat_inventory_key);

            if (ticket_number > 0) {
                //console.log(base_info);
                let is_verification_conditions_popup = false;

                let add_button = target_area.find('button[ng-click="quantityBtnClick(1)"]');
                for (let i = 0; i < ticket_number; i++) {
                    add_button.click();
                }

                let auto_click_next_btn = settings.kktix.auto_press_next_step_button;

                if (auto_click_next_btn) {
                    if (is_verification_conditions_popup) {
                        auto_click_next_btn = false;
                        let is_text_sent = kktix_verification_conditions(settings);
                        if (is_text_sent) {
                            auto_click_next_btn = true;
                        }
                    }
                }

                if (auto_click_next_btn) {
                    let $next_btn = $('div.register-new-next-button-area > button');
                    if ($next_btn) {
                        let selector = 'div.register-new-next-button-area > button';
                        if ($next_btn.length > 1) {
                            selector = 'div.register-new-next-button-area > button:last-child'
                            //$next_btn.last().click();
                        } else {
                            //$next_btn.click();
                        }
                        webdriver_click(settings, selector);
                    }
                }
            }
        }
    } else {
        console.log("not target_area found.")
    }
}

function checkall() {
    $('input[type=checkbox]:not(:checked)').each(function() {
        $(this).click();
    });
}

console.log('start assign');

var settings;
chrome.storage.local.get('settings', function(items) {
    if (items.settings) {
        settings = items.settings;
    }
});

var assignInterval = setInterval(() => {
    chrome.storage.local.get('status', function(items) {
        if (items.status && items.status == 'ON') {
            if (settings) {
                checkall();
                //kktix_area_keyword(settings);
                var area_keyword_array = []; 
                var ticket_number = 2;
                kktix_area_keyword_ticket_number(settings, area_keyword_array, ticket_number);
            }
        } else {
            //console.log('ddddext status is not OFF');
        }
    });
}, 100);