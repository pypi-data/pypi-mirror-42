{% load instant_tags %}

var mq_callbacks_{% get_users_channel %} = {
    "message": function(dataset) {
    	if (instantDebug === true) { console.log('DATASET: '+JSON.stringify(dataset));};
    	res = unpack_data(dataset);
    	var message = res['message']
    	var event_class = res['event_class']
    	var message_label = res['message_label']
    	var data = res['data']
    	var channel = res['channel'];
    	var uid = res['UID'];
    	var site = res["site"];
    	// handlers
    	if (debug === true) {
    			console.log('Msg: '+message+"\nChan: "+channel+"\nEvent_class: "+event_class+'\nData: '+JSON.stringify(data));
    	}
    	var timenow = getClockTime(false);
    	if ( data.hasOwnProperty('admin_url') ) {
    		message = '<a href="'+data['admin_url']+'" target="_blank">'+message+'</a>';
    	}
    	handlers_for_event(event_class, channel, message, data, site, uid);
    },
    {% include "instant/js/join_events.js" %}
}

var users_subscription = centrifuge.subscribe("{% get_users_channel %}", mq_callbacks_{% get_users_channel %});