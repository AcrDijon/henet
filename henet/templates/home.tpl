
<div class="page-header">
  <h1>{{_('Website management')}}</h1>
</div>

  % if content_changed:
<p>
  <strong>{{_('The content was modified')}}</strong>
</p>
  % end

<form role="form" action="/build" method="POST"  accept-charset="utf8">
  <input type="hidden" name="_csrf_token" value="{{ csrf_token }}">
  <input type="submit" class="btn btn-lg btn-danger" value="{{_('Update the website')}}"></input>
</form>



<div class="row">
 <div class="col-xs-8 col-sm-6">


<div class="page-header">
  <h2>{{_('Adding an article')}}</h2>
</div>
<form role="form" action="/create" method="POST"  accept-charset="utf8">
 <input type="hidden" name="_csrf_token" value="{{ csrf_token }}">
 <div class="form-group">
   <label for="title">{{_('Title')}}:</label>
   <input class="form-control" id="title" type="text" name="title"></input>
 </div>

 <p>
  % for cat, data  in categories:
    % if data['can_create']:
    <input id="actu" type="submit" class="btn btn-lg btn-primary"
           name="cat_add_{{cat}}" value="{{data['title']}}"></input>
    % end
  % end
 </p>
</form>
</div>


<div class="col-xs-8 col-sm-6">
<div class="page-header">
  <h2>{{_('Adding a page')}}</h2>
</div>
<form role="form" action="/create" method="POST"  accept-charset="utf8">
 <input type="hidden" name="_csrf_token" value="{{ csrf_token }}">
 <div class="form-group">

 <div class="form-group">
   <label for="page_title">{{_('Title')}}:</label>
   <input class="form-control" id="page_title" type="text" name="title"></input>
 </div>

 <p>
  % for page_, data  in pages:
    % if data['can_create']:
    <input type="submit" class="btn btn-lg btn-primary"
           name="page_add_{{page_}}" value="{{data['title']}}"></input>
    % end
  % end
 </p>
</form>
</div>

% rebase('base.tpl', title="Home")