<div class="page-header">
<h1>{{ data['title'] }}</h1>
</div>

<table class="table table-striped">
  <thead>
  <tr>
   <th>Date</th>
   <th>Titre</th>
   <th>Action</th>
   </tr>
  </thead>
<tbody>
% for article in articles:
<tr>
 <td>{{ article['metadata'].get('date', now).strftime('%d/%m/%Y') }}</td>
 <td>
  <a href="/category/{{ category }}{{article['filename']}}">
    {{ article['title'] }}
  </a>
 </td>
 <td>
  <form action="/delete/category/{{ category }}{{article['filename']}}"
        method="POST" onsubmit="return confirm('Confirmez-vous la suppression?');">
    <button type="submit" class="btn btn-xs btn-danger">
      <span class="glyphicon glyphicon-trash"></span>
    </button>
  </form>
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
