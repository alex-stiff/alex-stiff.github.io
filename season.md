---
layout: page
title: Season
permalink: /season/
---

{% assign players = "" | split: "" %}
{% for week in site.data %}

{% if week[0] contains 'match-' %}
{{ week[1] }}
{% endif %}

{% endfor %}