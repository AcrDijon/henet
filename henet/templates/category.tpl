<div class="page-header">
<h1>{{ data['title'] }}</h1>
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
  <a href="/category/{{ category }}{{article['filename']}}">
    {{ article['title'] }}
  </a>
 </td>
</tr>
% end
</tbody>
</table>
% if total_pages > 1:
  % for page in range(total_pages):
  % if page == current_page:
    {{page}}
  % else:
    <a href="/category/{{ category }}?page={{page}}">{{page}}</a>
  % end
  % end
% end

% rebase('base.tpl', page_title=data['title'])
