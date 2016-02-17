<div class="page-header">
<h1>{{_('Media management')}}</h1>
</div>

% for file in files:
<div style="float:left; margin: 4px; max-width: 200px; max-height:200px">
  <a href="/media/{{ file['name'] }}" data-lightbox="{{file['name']}}" id="a-{{file['name']}}">
    <img src="/thumbnail/200x200/{{ file['name'] }}"/>
  </a>
  <!--form style="float:right" action="/delete/media/{{file['name']}}"
        method="POST" onsubmit="return confirm('{{_('Do you really want to suppress this?')}}');">
  <input type="hidden" name="_csrf_token" value="{{ csrf_token }}">
    <button type="submit" class="btn btn-xs btn-danger" onmouseover="$('#a-{{file['name']}}').css('pointer-events', 'none')">
      <span class="glyphicon glyphicon-trash"></span>
    </button>
  </form-->
</div>
% end
<div style="clear:both"/>


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

<script src="/resources/js/lightbox-plus-jquery.min.js"></script>

% rebase('base.tpl', page_title=_('Media Management'))
