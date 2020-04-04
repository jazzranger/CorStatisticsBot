{% for item in news_arr %} 
[{{ item.title }}]({{ item.url }}) 
{{ item.description }}
{% endfor %}