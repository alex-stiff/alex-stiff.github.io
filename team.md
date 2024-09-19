---
layout: page
title: Team
permalink: /team/
---

{% assign players = "" | split: "" %}

{% for player in site.data.players %}
    {% assign p = player.forename | split: " " %}
    {% assign players = players | concat: p %}
{% endfor %}

{% for player in players %}
    {% assign weighted = 0 %}
    {% assign darts = 0 %}
    {% assign hundreds = 0 %}
    {% for week in site.data %}
        {% for game in week[1] %}
            {% if game['Home'] == player %}
                {% assign week_weight = game["Darts"] | times: game["Avg"] %}
                {% assign week_darts = game["Darts"] %}
                {% assign week_hundreds = game["100s"] | split: " " | size %}
                {% assign weighted = weighted | plus: week_weight %}
                {% assign darts = darts | plus: week_darts %}
                {% assign hundreds = hundreds | plus: week_hundreds %}
            {% endif %}
        {% endfor %}
    {% endfor %}
    {% if weighted > 0 %}
        {% assign season_avg = weighted | divided_by: darts %}
    {% else %}
        {% assign season_avg = 0 %}
    {% endif %}

    {% for player_data in site.data.players %}
        {% if player == player_data.forename %}
<div style="display: flex; align-items: center; margin-bottom: 20px;">
    <img src="{{ baseurl }}/assets/images/{{ player }}.png" alt="{{ player.Name }}" style="width: 200px; height: auto; margin-right: 15px;" />
    <div>
    <h3>{{ player_data.forename }}</h3>
    <p>Season average: {{ season_avg }}</p>
    <p>100s: {{ hundreds }}</p>
    </div>
</div>
        {% endif %}
    {% endfor %}
{% endfor %}
