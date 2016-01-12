<h1>{{ category }}</h1>
<hr/>

<table class="table">
<tr>
   <th>Date</th>
   <th>Titre</th>
   <th>Url</th>
 </tr>
% for article in articles:
<tr class="article">
 <td>{{ article['metadata']['date'].strftime('%d/%m/%Y') }}</td>
 <td>
  <a href="/category/{{ category }}/{{article['filename']}}">
    {{ article['title'] }}
  </a>
 </td>
 <td>
  <a href="http://acr-dijon.org/{{article['url']}}">
    {{ article['url'] }}
  </a>
 </td>

<tr>
% end

</table>

% rebase base title = category
