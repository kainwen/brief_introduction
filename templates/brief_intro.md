{{ title }}
===========

{% for card in cards %}
## [NO.{{ loop.index }}] {{ card["title"] }}: *{{ card["label"] }}*

### 摘要

{{ card["abstract"] }}
  
### 简评

{% for cm in card["comments"] %}
**{{ cm["name"] }}:**{{ cm["text"] }}

   
{% endfor %}

----------------
  
{% endfor %}


