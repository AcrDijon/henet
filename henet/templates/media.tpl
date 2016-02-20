<div class="page-header">
<h1>{{_('Media management')}}</h1>
</div>

<div class="container-fluid">
<div class="grid">
<div class="grid-sizer col-xs-3"></div>
 % for file in files:
 <div class="grid-item">
 <div class="grid-item-content" style="max-width: 200px; max-height:200px; position: relative; margin: 4px">
<!-- style="float:left; margin: 4px; max-width: 200px; max-height:200px; position: relative"-->

  <a  href="/media/{{ file['name'] }}" data-lightbox="{{file['name']}}" id="a-{{file['name']}}">
   <img src="/thumbnail/200x200/{{ file['name'] }}"/>
  </a>

   <span style="position:absolute;bottom: 2px;left: 4px; text-shadow: 1px 1px black; color: white; text-overflow: ellipsis;width:90%;font-size: 12px;white-space: nowrap;overflow: hidden;">{{ file['name'] }}</span>

   <form action="/delete/media/{{file['name']}}"
         method="POST" onsubmit="return confirm('{{_('Do you really want to suppress this?')}}');"
         style="position:absolute;top: 5px;right: 5px">

  <input type="hidden" name="_csrf_token" value="{{ csrf_token }}">
    <button type="submit" class="btn btn-xs btn-danger">
      <span class="glyphicon glyphicon-trash"></span>
    </button>
  </form>
 </div>
 </div>
% end

</div>
</div>
<!--div style="clear:both"/-->


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

<form role="form" action="/upload" method="POST"  accept-charset="utf8"
      enctype='multipart/form-data'>
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
<script src="/resources/js/masonry.pkgd.min.js">></script>
<script>

$(function() {
  $('.grid').masonry({
    itemSelector: '.grid-item',
    columnWidth: 209,  //'.grid-sizer',
    percentPosition: true
 });
});
</script>

% rebase('base.tpl', page_title=_('Media Management'))
