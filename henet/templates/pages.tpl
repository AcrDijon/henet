<div class="page-header">
<h1>{{ data['title'] }}</h1>
</div>

<table class="table table-striped">
  <thead>
  <tr>
   <th>{{_('Date')}}</th>
   <th>{{_('Title')}}</th>
   <th>{{_('URL')}}</th>
   <th>{{_('Suppression')}}</th>
   </tr>
  </thead>
<tbody>
% for article in articles:
<tr>
 <td>{{ article['metadata'].get('date', now).strftime('%d/%m/%Y') }}</td>
 <td>
  <a href="/page/{{ page }}/{{article['filename']}}">
    {{ article['title'] }}
  </a>
 </td>
 <td><a href="{{ article['url'] }}">{{ article['url'] }}</a></td>
 <td>
  <form action="/delete/page/{{ page }}/{{article['filename']}}"
        method="POST" onsubmit="return confirm('{{_('Do you really want to suppress this?')}}');">
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
    <a href="/page/{{ page }}?page={{page}}">{{page}}</a>
  % end
  % end
% end
% if can_create:
<div class="page-header">
  <h4>{{_('Adding a page')}}</h4>
</div>

<form role="form" action="/create" method="POST"  accept-charset="utf8">
 <div class="form-group">
   <label for="title">{{_('Title')}}:</label>
   <input class="form-control" id="title" type="text" name="title"></input>
 </div>

 <p>
  <input type="submit" class="btn btn-lg btn-primary"
         name="page_add_{{page}}" value="{{_('Add')}}"></input>
 </p>

</form>

% end

% rebase('base.tpl', page_title=data['title'])
