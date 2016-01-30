
<div class="page-header">
  <h1>{{_('Website management')}}</h1>
</div>

  % if content_changed:
<p>
  <strong>Le site a été modifié</strong>
</p>
  % end

<form role="form" action="/build" method="POST"  accept-charset="utf8">
  <input type="submit" class="btn btn-lg btn-danger" value="Mettre à jour le site"></input>
</form>



<div class="row">
 <div class="col-xs-8 col-sm-6">


<div class="page-header">
  <h2>Ajout d'un article</h2>
</div>
<form role="form" action="/create" method="POST"  accept-charset="utf8">
 <div class="form-group">
   <label for="title">Titre de l'article:</label>
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
</div>
<div class="col-xs-8 col-sm-6">

<div class="page-header">
  <h2>Ajout d'une page</h2>
</div>

 <div class="form-group">
   <label for="title">Titre de la page:</label>
   <input class="form-control" id="title" type="text" name="title"></input>
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