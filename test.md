---
layout: page
title: Test
permalink: /test/
---

{% assign num_darts = 0 %}

{% for game in site.data.games-2024-09-05 %}
{% assign scores = game["Scores"] | split: " " %}
{% for score in scores %}
{% if score contains 'x' %}
{% assign final_score = score | split: 'x' %}
{% assign num_darts = num_darts | plus: final_score[1] %}
{% else %}
{% assign num_darts = num_darts | plus: 3 %}
{% endif %}
{% endfor %}
{% endfor %}

Game was {{ scores | split: " " }}

{{ num_darts }} darts