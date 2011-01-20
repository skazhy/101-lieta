{% extends "base-admin.html" %}
{% block content %}
	{% for t in tt %}
        <form class="editt" action="/admin/writet" method="post">
			<p>{{ t.name_short }}</p>
			<textarea name="content" rows="2" cols="100">{{ t.content }}</textarea>
			<input type="hidden" name="name_short" value="{{ t.key }}" />
			<input type="submit" value="Edit text"/>
		</form>
	{% endfor %}
    {% for log in logs %}
		<form class="editl" action="/admin/writel" method="post">
            <div class="grid_6 entry">
                <textarea name="content" rows="5" cols="50">{{ log.content}}</textarea>
			</div>
		    <div class="grid_3">
			    <p>{{ log.combo }}</p>
                <input type="text" name="number" value="{{ log.numbers }}" /><br />
			    <input type="submit" value="Labot"/>
			</div>
            <input type="hidden" name="id" value="{{ log.key }}" />
		</form>
	    <div class="clear"></div>
    {% endfor%}
{% endblock content %}

