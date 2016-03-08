<div class="page-header">
<h1>{{_('Media management')}}</h1>
</div>

<div class="container-fluid">
<div class="grid">
<div class="grid-sizer col-xs-3"></div>
 % for file in files:
 <div class="grid-item">
 <div class="grid-item-content">
  <a  href="/media/{{ file['name'] }}" data-lightbox="{{file['name']}}" id="a-{{file['name']}}">
   <img src="/thumbnail/200x200/{{ file['name'] }}"/>
  </a>
   <span class="imagetext">{{ file['name'] }}</span>

   <form action="/delete/media/{{file['name']}}"
         method="POST" onsubmit="return confirm('{{_('Do you really want to suppress this?')}}');">
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


% if total_pages > 1:
<div class="batch">
  % for page in range(total_pages):
  % if page == current_page:
  <span class="active">{{page}}</span>
  % else:
  <span class="inactive">
    <a href="/media?page={{page}}">{{page}}</a>
  </span>
  % end
  % end
</div>
<div style="clear:both"/>
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

$(window).load(function() {
  $('.grid').masonry({
    itemSelector: '.grid-item',
    columnWidth: 209,  //'.grid-sizer',
    percentPosition: true
 });
});
</script>

% rebase('base.tpl', page_title=_('Media Management'))
