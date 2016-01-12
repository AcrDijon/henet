
<form role="form">
 <div class="form-group">
   <label for="title">Titre:</label>
   <input class="form-control" id="title" type="text" value="{{ article['title'] }}"></input>
 </div>

 <div class="form-group">
   <label for="date">Date:</label>
   <div>
     <input class="form-control" id="date" type="text" value="{{article['metadata']['date'].strftime('%d/%m/%Y') }}"></input>
   </div>
 </div>


 <div class="form-group">
   <textarea class="form-control" id="body" rows="5" id="content">{{article['body']}}</textarea>
  </div>

<div class="form-group">
  <iframe id="preview"
        src="/category/{{ category }}/{{filename}}/preview">
Preview
</iframe>
  </div>

 <button type="submit" class="btn btn-default">Sauvegarder</button>

</form>

<script src="/resources/js/editor.js"></script>
<script src="/resources/js/jquery-linedtextarea.js"></script>

<script>
 $('#date').datepicker({
   format: "dd/mm/yyyy",
   language: "fr"
 });

$("#body").linedtextarea();

 window.baseTitle = $('head title').text();

 $('textarea#body').bind('change', genPreview);
 timerId = window.setInterval(genPreview, 900);

 $('textarea#body').scroll(syncScrollPosition);

</script>

% rebase base title = "article"
