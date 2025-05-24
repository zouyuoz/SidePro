function kktix_event_redirect() {
    const currentUrl = window.location.href;
    let event_code = currentUrl.split('/')[4];
    if (event_code.indexOf('?') > -1) {
        event_code = event_code.split('?')[0];
    }
    //console.log(currentUrl);
    //console.log(event_code);
    if (event_code) {
        let button_count = $("div.tickets > a.btn-point").length;
        //console.log("length:"+button_count);
        if (button_count == 1) {
            let new_url = "https://kktix.com/events/" + event_code + "/registrations/new";
            location.href = new_url;
        } else {
            // do nothing.
        }
    }
}

chrome.storage.local.get('status', function(items) {
    if (items.status && items.status == 'ON') {
        setTimeout(() => {
            kktix_event_redirect();
        }, 2000);
    } else {
        console.log('no status found');
    }
});