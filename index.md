---
layout: page
title: Team
---

{% for player in site.data.season %}
<div style="display: flex; align-items: center; margin-bottom: 20px;">
    <img src="/assets/images/{{ player.name | downcase }}.png" alt="{{ player.Name }}" style="width: 200px; height: auto; margin-right: 15px;" />
    <div>
        <h3>{{ player.name }}</h3>
        <p>Games: {{ player.games }}</p>
        <p>Season average: {{ player.average }}</p>
        <!-- <p>100s: {{ player_ }}</p> -->
    </div>
</div>
{% endfor %}
