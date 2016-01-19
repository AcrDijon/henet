

<div class="page-header">
  <h1>Ajout d'article</h1>
</div>
<form role="form" action="/create" method="POST"  accept-charset="utf8">
 <div class="form-group">
   <label for="title">Titre de l'article:</label>
   <input class="form-control" id="title" type="text" name="title"></input>
 </div>

 <p>
  <input id="actu" type="submit" class="btn btn-lg btn-primary"
         name="add_actus" value="Actualité"></input>
  <input id="actu" type="submit" class="btn btn-lg btn-primary"
         name="add_resultat" value="Résultat"></input>
  <input id="actu" type="submit" class="btn btn-lg btn-primary"
         name="add_foulees" value="Foulées"></input>
 </p>
</form>

% rebase base title = "Home"