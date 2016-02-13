<div class="page-header">
<h1>{{_('Media management')}}</h1>
</div>

<table class="table table-striped">
 <thead>
  <tr>
   <th>{{_('Name')}}</th>
   <th>{{_('Size')}}</th>
   <th>{{_('Modified')}}</th>
   <th>{{_('Filetype')}}</th>
   <th>{{_('Suppression')}}</th>
  </tr>
 </thead>
<tbody>
% for file in files:
<tr>
 <td><a href="/media/{{ file['name'] }}">{{ file['name'] }}</a></td>
 <td>{{ file['size'] }}</td>
 <td>{{ file['modified'].strftime('%d/%m/%Y') }}</td>
 <td><img title="{{file['type']}}" alt="{{file['type']}}" src="/resources/images/mimetypes/{{ file['image-type'] }}"></img></td>
 <td>
  <form action="/delete/media/{{file['name']}}"
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
    <a href="/media?page={{page}}">{{page}}</a>
  % end
  % end
% end

<hr/>
<div class="page-header">
  <h4>{{_('Adding a file')}}</h4>
</div>

<form role="form" action="/upload" method="POST"  accept-charset="utf8">
 <input type="hidden" name="_csrf_token" value="{{ csrf_token }}">
 <div class="form-group">
   <label for="title">{{_('File')}}:</label>
   <input class="form-control" id="file" type="file" name="file"></input>
 </div>

 <p>
 <input id="actu" type="submit" class="btn btn-lg btn-primary"
        name="upload" value="{{_('Upload')}}"></input>
 </p>
</form>


% rebase('base.tpl', page_title=_('Media Management'))