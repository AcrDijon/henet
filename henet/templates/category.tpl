<div class="page-header">
<h1>{{ data['title'] }}</h1>
</div>

<table class="table table-striped">
  <thead>
  <tr>
   <th>{{_('Date')}}</th>
   <th>{{_('Title')}}</th>
   <th>{{_('URL')}}</th>
   % if use_comments:
   <th>{{_('Comments')}}</th>
   % end
   <th>{{_('Suppression')}}</th>
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
 % if use_comments:
 <td>
  {{article['comments_count']}}
 </td>
 % end
 <td>
  <form action="/delete/category/{{ category }}/{{article['filename']}}"
        method="POST" onsubmit="return confirm('{{_('Do you really want to suppress this?')}}');">
   <input type="hidden" name="_csrf_token" value="{{ csrf_token }}">
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
  <h4>{{_('Adding an article')}}</h4>
</div>

<form role="form" action="/create" method="POST"  accept-charset="utf8">
 <input type="hidden" name="_csrf_token" value="{{ csrf_token }}">
 <div class="form-group">
   <label for="title">{{_('Title')}}:</label>
   <input class="form-control" id="title" type="text" name="title"></input>
 </div>

 <p>

    <input id="actu" type="submit" class="btn btn-lg btn-primary"
           name="cat_add_{{category}}" value="{{_('Add')}}"></input>
 </p>
</form>
% end


% rebase('base.tpl', page_title=data['title'])
