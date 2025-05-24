const storage = chrome.storage.local;
var settings = null;

$("footer").remove();

function ticketmaster_assign_ticket_number(ticket_number) {
    let ticket_options = $("#ticketPriceList select:first option");
    if (ticket_options.length > 1) {
        let is_ticket_number_assign = false;
        const first_option = ticket_options.first();
        if (ticket_number > 0 && first_option.prop('selected') && first_option.prop('value') == '0') {
            ticket_options.each(function() {
                if ($(this).val() == ticket_number) {
                    $(this).prop('selected', true);
                    is_ticket_number_assign = true;
                    return false;
                }
            });
            if (!is_ticket_number_assign) {
                ticket_options.last().prop('selected', true);
                is_ticket_number_assign = true;
            }
            if (is_ticket_number_assign) {
                // PS: click too fast will be detected.
                setTimeout(() => {
                    $("#autoMode").click();
                }, 300);
            }
        }
    }
}

var myInterval = null;

function ticketmaster_select_box_ready(settings) {
    let ret = false;
    let form_select = $("table#ticketPriceList tbody tr td select.form-select");
    if (form_select.length > 0) {
        ret = true;
        if (myInterval)
            clearInterval(myInterval);
        ticketmaster_assign_ticket_number(settings.ticket_number);
    }
    //console.log("select_box_ready:"+ret);
    return ret;
}

function ticketmaster_area_main() {
    myInterval = setInterval(() => {
        ticketmaster_select_box_ready(settings);
    }, 100);
}

storage.get('settings', function(items) {
    if (items.settings) {
        settings = items.settings;
    } else {
        console.log('no settings found');
    }
});

storage.get('status', function(items) {
    if (items.status && items.status == 'ON') {
        ticketmaster_area_main();
    } else {
        console.log('no status found');
    }
});