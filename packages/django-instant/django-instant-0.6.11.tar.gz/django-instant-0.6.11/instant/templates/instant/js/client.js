{% load instant_tags %}

var instantDebug = {% debug_mode %};

{% include "instant/js/utils.js" %}

{% get_timestamp as timestamp %}
var centrifuge = new Centrifuge({
	url: "{% get_centrifugo_url %}",
    user: "{% if user.is_anonymous %}anonymous{% else %}{{ request.user.username }}{% endif %}",
    timestamp: "{{ timestamp }}",
    token: "{% if user.is_anonymous %}{% mq_generate_token 'anonymous' timestamp %}{% else %}{% mq_generate_token user.username timestamp %}{% endif %}"
});

{% include "instant/extra_clients.js" %}

{% if user.is_superuser %}
	{% is_superuser_channel as enable_superuser_channel %}
	{% if enable_superuser_channel %}
		{% include "instant/channels/superuser/client.js" %}
	{% endif %}
	{% get_channels_for_role request.path "superuser" as supchans %}
	{% for chan in supchans %}
		{% get_handlers_url chan as handlers %}
		{% with handlers.0 as url %}
		{% with handlers.1 as chan_name %}
			{% include "instant/channels/client.js" %}
		{% endwith %}
		{% endwith %}
	{% endfor %}
{% endif %}

{% if user.is_staff %}
	{% is_staff_channel as enable_staff_channel %}
	{% if enable_staff_channel %}
		{% include "instant/channels/staff/client.js" %}
	{% endif %}
	{% get_channels_for_role request.path "staff" as staffchans %}
	{% for chan in staffchans %}
		{% get_handlers_url chan as handlers %}
		{% with handlers.0 as url %}
		{% with handlers.1 as chan_name %}
			{% include "instant/channels/client.js" %}
		{% endwith %}
		{% endwith %}
	{% endfor %}
{% endif %}

{% if user.is_authenticated %}
	{% is_users_channel as enable_user_channel %}
	{% if enable_user_channel %}
		{% include "instant/channels/users/client.js" %}
	{% endif %}
	{% get_channels_for_role request.path "users" as userchans %}
	{% for chan in userchans %}
		{% get_handlers_url chan as handlers %}
		{% with handlers.0 as url %}
		{% with handlers.1 as chan_name %}
			{% include "instant/channels/client.js" %}
		{% endwith %}
		{% endwith %}
	{% endfor %}
{% endif %}

{% get_channels_for_role request.path "public" as pubchans %}
{% for chan in pubchans %}
	{% get_handlers_url chan as handlers %}
	{% with handlers.0 as url %}
	{% with handlers.1 as chan_name %}
		{% include "instant/channels/client.js" %}
	{% endwith %}
	{% endwith %}
{% endfor %}

centrifuge.connect();