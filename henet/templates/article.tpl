
<form role="form">
 <div class="form-group">
   <label for="title">Titre:</label>
   <input class="form-control" id="title" type="text" value="{{ article['title'] }}"></input>
 </div>

 <div class="form-group">
   <label for="date">Date:</label>
   <div>
     <input class="form-control" id="date" type="text" value="{{article['metadata']['date'] }}"></input>
   </div>
 </div>


 <div class="form-group">
   <textarea class="form-control" id="body"
            style="min-height: 400px;width: 90%; font-family:Consolas,Monaco,Lucida Console,Liberation Mono,DejaVu Sans Mono,Bitstream Vera Sans Mono,Courier New, monospace;" rows="5" id="content">{{article['body']}}</textarea>
  </div>

 <button type="submit" class="btn btn-default">Sauvegarder</button>

</form>

% rebase base title = "article"
