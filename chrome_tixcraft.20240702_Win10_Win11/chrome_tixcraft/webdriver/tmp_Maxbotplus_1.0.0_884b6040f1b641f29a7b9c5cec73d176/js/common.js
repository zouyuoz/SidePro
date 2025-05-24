function get_target_item_with_order(mode, matched_block) {
    //console.log(settings);
    let target_area = null;

    if (matched_block.length) {
        let last_index = matched_block.length - 1
        let center_index = 0;
        let random_index = 0;
        if (matched_block.length > 1) {
            center_index = parseInt(last_index / 2);
            random_index = getRandom(0, last_index)
        }
        if (mode.toLowerCase() == "from top to bottom")
            target_area = matched_block[0];
        if (mode.toLowerCase() == "from bottom to top")
            target_area = matched_block[last_index];
        if (mode.toLowerCase() == "center")
            target_area = matched_block[center_index];
        if (mode.toLowerCase() == "random")
            target_area = matched_block[random_index];
    }
    return target_area;
}

function get_target_area_with_order(settings, matched_block) {
    return get_target_item_with_order(settings.area_auto_select.mode, matched_block);
}

function get_target_date_with_order(settings, matched_block) {
    return get_target_item_with_order(settings.date_auto_select.mode, matched_block);
}

function getRandom(min,max){
    return Math.floor(Math.random()*(max-min+1))+min;
}

function get_remote_url(settings) {
    let remote_url_string = "";
    if (settings) {
        let remote_url_array = [];
        if (settings.advanced.remote_url.length > 0) {
            remote_url_array = JSON.parse('[' + settings.advanced.remote_url + ']');
        }
        if (remote_url_array.length) {
            remote_url_string = remote_url_array[0];
        }
    }
    return remote_url_string;
}

async function webdriver_sendkey(settings, selector, answer) {
    const cmd = [{type: 'sendkey', selector: selector, text: answer}];
    webdriver_command(settings, cmd);
}

async function webdriver_location_sendkey(settings, selector, answer, location) {
    const cmd = [{type: 'sendkey', selector: selector, text: answer, location: location}];
    webdriver_location_command(settings, location, cmd);
}

async function webdriver_click(settings, selector) {
    const cmd = [{type: 'click', selector: selector}];
    webdriver_command(settings, cmd);
}

async function webdriver_location_click(settings, selector, location) {
    const cmd = [{type: 'click', selector: selector, location: location}];
    webdriver_location_command(settings, location, cmd);
}

async function webdriver_command(settings, command) {
    let api_url = get_remote_url(settings);
    //console.log("api_url:" + api_url);
    if(api_url.indexOf("127.0.0.")>-1) {
        let body = {
            token: settings.token,
            command: command};
        body = JSON.stringify(body);

        let bundle = {
            action: 'post',
            data: {
                'url': api_url + 'sendkey',
                'post_data': body,
            }
        };
        let bundle_string = JSON.stringify(bundle);
        //console.log(bundle);
        const return_answer = await chrome.runtime.sendMessage(bundle);
        //console.log(return_answer);
    }
}

async function webdriver_location_command(settings, location, command) {
    let api_url = get_remote_url(settings);
    //console.log("api_url:" + api_url);
    if(api_url.indexOf("127.0.0.")>-1) {
        let body = {
            token: settings.token,
            command: command};
        body = JSON.stringify(body);

        let bundle = {
            action: 'post',
            data: {
                'url': api_url + 'sendkey',
                'post_data': body,
            }
        };
        let bundle_string = JSON.stringify(bundle);
        //console.log(bundle);
        const return_answer = await chrome.runtime.sendMessage(bundle);
        //console.log(return_answer);
    }
}

async function webdriver_eval(settings, text) {
    let api_url = get_remote_url(settings);
    //console.log("api_url:" + api_url);
    if(api_url.indexOf("127.0.0.")>-1) {
        let body = {
            token: settings.token,
            command: [
            {type: 'eval', script: text}
        ]};
        body = JSON.stringify(body);

        let bundle = {
            action: 'post',
            data: {
                'url': api_url + 'eval',
                'post_data': body,
            }
        };
        let bundle_string = JSON.stringify(bundle);
        //console.log(bundle);
        const return_answer = await chrome.runtime.sendMessage(bundle);
        //console.log(return_answer);
    }
}

async function webdriver_location_eval(settings, text, location) {
    let api_url = get_remote_url(settings);
    //console.log("api_url:" + api_url);
    if(api_url.indexOf("127.0.0.")>-1) {
        let body = {
            token: settings.token,
            command: [
            {type: 'eval', script: text, location: location}
        ]};
        body = JSON.stringify(body);

        let bundle = {
            action: 'post',
            data: {
                'url': api_url + 'eval',
                'post_data': body,
            }
        };
        let bundle_string = JSON.stringify(bundle);
        //console.log(bundle);
        const return_answer = await chrome.runtime.sendMessage(bundle);
        //console.log(return_answer);
    }
}

function playsound(){
    chrome.runtime.sendMessage({action: 'playsound'});
}
