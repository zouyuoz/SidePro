var settings = null;

$("div.masthead-wrap").remove();

function date_clean() {
    remove_list = ['Currently Unavailable',
        'Sale ended on 20',
        'Sold out',
        '暫停販售',
        ':00 截止',
        '已售完',
        '00に発売終了',
        '販売一時中止',
        '完売した'
    ];
    for (let i = 0; i < remove_list.length; i++) {
        $("#gameList td:contains('" + remove_list[i] + "')").each(function() {
            $(this).parent().remove();
        });
    }
}

function date_keyword(settings) {
    let date_keyword_array = [];
    if (settings) {
        if (settings.date_auto_select.date_keyword.length > 0) {
            if (settings.date_auto_select.date_keyword != '""') {
                date_keyword_array = JSON.parse('[' + settings.date_auto_select.date_keyword + ']');
            }
        }
    }
    //console.log(date_keyword_array);
    gameList_keyword(date_keyword_array, settings.date_auto_select.mode);
}

function gameList_keyword(date_keyword_array, date_order_mode) {
    let target_date = null;
    if (date_keyword_array.length) {
        for (let i = 0; i < date_keyword_array.length; i++) {
            let query_string = "#gameList td:contains('" + date_keyword_array[i] + "')";
            if (date_keyword_array[i] == "") {
                query_string = "#gameList td"
            }
            let matched_block = [];
            $(query_string).each(function() {
                matched_block.push($(this));
            });
            target_date = get_target_item_with_order(date_order_mode, matched_block);
            if (target_date) {
                console.log("match keyword:" + date_keyword_array[i]);
                break;
            }
        }
    } else {
        let query_string = "#gameList td";
        let matched_block = [];
        $(query_string).each(function() {
            matched_block.push($(this));
        });
        target_date = get_target_item_with_order(date_order_mode, matched_block);
    }

    if (target_date) {
        let button_tag = "button";
        const currentUrl = window.location.href;
        const domain = currentUrl.split('/')[2];
        if (domain == "ticketmaster.sg") {
            button_tag = "a";
        }

        let link = target_date.parent().find(button_tag).attr("data-href");
        if (link) {
            //console.log("link: " + link);
            if (link.length > 0 && link.indexOf('/') > -1) {
                clearInterval(gameInterval);
                window.location.href = link;
            }
        }
    } else {
        //console.log("not target_date found.")
    }
}

async function do_reload_if_not_overheat(user_auto_reload_page_interval, auto_reload_overheat_count, auto_reload_overheat_cd) {
    const overheat_second = 2.5;
    const overheat_second_target = overheat_second * 1000;
    let auto_reload_page_interval = user_auto_reload_page_interval;
    chrome.storage.local.get('last_reload_timestamp', function(items) {
        if (items.last_reload_timestamp) {
            let new_timestamp = [];
            const now = new Date().getTime();
            
            //for (let i = items.last_reload_timestamp.length - 1; i >= 0; i--) {
            for (let i = 0; i < items.last_reload_timestamp.length; i++) {
                let each_time = items.last_reload_timestamp[i];
                let current_diff = now - each_time;
                if (current_diff <= overheat_second_target) {
                    //last_reload_timestamp.splice(i, 1);
                    new_timestamp.push(each_time);
                }
            }
            new_timestamp.push(now);
            chrome.storage.local.set({
                last_reload_timestamp: new_timestamp
            });

            if (new_timestamp.length >= auto_reload_overheat_count) {
                console.log("overheat, slow down!");
                auto_reload_page_interval = auto_reload_overheat_cd;
            }

            const target_delay = auto_reload_page_interval * 1000;
            //console.log("target_delay:" + target_delay);
            if (target_delay < 100) {
                //console.log('Start to reload now.');
                location.reload();
            } else {
                //console.log('We are going to reload after few seconeds.');
                setTimeout(function() {
                    location.reload();
                }, target_delay);
            }
        } else {
            console.log("initial timestamp.");
            chrome.storage.local.set({
                last_reload_timestamp: []
            });
        }
    });
}

function date_auto_reload() {
    let reload = false;

    let button_tag = "button";
    const currentUrl = window.location.href;
    const domain = currentUrl.split('/')[2];
    if (domain == "ticketmaster.sg") {
        button_tag = "a";
    }

    const query_string = "#gameList " + button_tag;
    if ($(query_string).length) {
        date_clean();
        if ($(query_string).length) {
            if (settings) {
                date_keyword(settings);
            }
        } else {
            reload = true;
        }
    } else {
        reload = true;
    }

    if (reload) {
        if (settings) {
            if (gameInterval) clearInterval(gameInterval);
            
            let user_auto_reload_page_interval = settings.advanced.auto_reload_page_interval;
            let user_auto_reload_overheat_count = settings.advanced.auto_reload_overheat_count;
            let user_auto_reload_overheat_cd = settings.advanced.auto_reload_overheat_cd;
            do_reload_if_not_overheat(user_auto_reload_page_interval, user_auto_reload_overheat_count, user_auto_reload_overheat_cd);
        }
    }
}

chrome.storage.local.get('settings', function(items) {
    if (items.settings) {
        settings = items.settings;
    }
});

var gameInterval = setInterval(() => {
    if (chrome.storage.local) {
        chrome.storage.local.get('status', function(items) {
            if (items.status && items.status == 'ON') {
                date_auto_reload();
            } else {
                //console.log('maxbot status is not OFF');
            }
        });
    }
}, 100);
