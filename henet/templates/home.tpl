

<div class="page-header">
  <h1>Ajout d'article</h1>
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
           name="add_{{cat}}" value="{{data['title']}}"></input>
    % end
  % end
 </p>
</form>

% rebase base title = "Home"