{% extends "base-pub.html" %}
{% block saturs %}
	{% for log in logs %}
	<div class="log">
		<div class="lognr"><a href="/s/{{ log.number }}">{{ log.number }}</a></div>
		<span class="logcontent"> {{ log.content }}
		<p>{{ log.date }}</p>
	</div>
	{% endfor %}
{% endblock %}
