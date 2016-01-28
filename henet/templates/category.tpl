<div class="page-header">
<h1>{{ data['title'] }}</h1>
</div>

<table class="table table-striped">
  <thead>
  <tr>
   <th>Date</th>
   <th>Titre</th>
   <th>URL</th>
   <th>Commentaires</th>
   <th>Suppression</th>
   </tr>
  </thead>
<tbody>
% for article in articles:
<tr>
 <td>{{ article['metadata'].get('date', now).strftime('%d/%m/%Y') }}</td>
 <td>
  <a href="/category/{{ category }}/{{article['filename']}}">
    {{ article['title'] }}
  </a>
 </td>
 <td><a href="{{ article['url'] }}">{{ article['url'] }}</a></td>
 <td>
  {{article['comments_count']}}
 </td>
 <td>
  <form action="/delete/category/{{ category }}/{{article['filename']}}"
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

% if can_create:
<hr/>
<div class="page-header">
  <h4>Ajout d'un article</h4>
</div>

<form role="form" action="/create" method="POST"  accept-charset="utf8">
 <div class="form-group">
   <label for="title">Titre de l'article:</label>
   <input class="form-control" id="title" type="text" name="title"></input>
 </div>

 <p>

    <input id="actu" type="submit" class="btn btn-lg btn-primary"
           name="cat_add_{{category}}" value="Ajouter"></input>
 </p>
</form>
% end


% rebase('base.tpl', page_title=data['title'])
