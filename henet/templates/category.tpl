<div class="page-header">
<h1>{{ category }}</h1>
</div>

<table class="table table-striped">
  <thead>
  <tr>
   <th>Date</th>
   <th>Titre</th>
   </tr>
  </thead>
<tbody>
% for article in articles:
<tr>
 <td>{{ article['metadata']['date'].strftime('%d/%m/%Y') }}</td>
 <td>
  <a href="/category/{{ category }}/{{article['filename']}}">
    {{ article['title'] }}
  </a>
 </td>
</tr>
% end
</tbody>
</table>

% rebase('base.tpl', page_title=category)
