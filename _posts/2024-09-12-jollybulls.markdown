---
layout: post
title:  "Q-Army vs Jolly Bulls"
date: 2024-09-12
categories: matchnight
---

## Doubles

{% assign date_key = page.date | date: "%Y-%m-%d" %}

| Home | Score | Away |
| - | - | - |{% for game in site.data[date_key] %}{% if game['Home'] contains '&' %}
| {{ game['Home'] }} | {{ game['Score'] }} | {{ game['Away'] }} |{% endif %}{% endfor %}

## Singles

| Home | Score | Away | Avg | 100s |
| - | - | - | - | - |{% for game in site.data[date_key] %}{% unless game['Home'] contains '&' %}
| {{ game['Home'] }} | {{ game['Score'] }} | {{ game['Away'] }} | {{ game['Avg'] }} | {{ game['100s'] }} |{% endunless %}{% endfor %}