<h1>{{ category }}</h1>

% for article in articles:
<div class="article">
  <a href="/category/{{ category }}/{{article['filename']}}">
    {{ article['title'] }}
  </a>
<div>
% end

% rebase base title = "{{ category }}"
