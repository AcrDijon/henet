
<div class="form-group">

  <input type="text" style="width: 90%;" value="{{ article['title'] }}"></input>
  <textarea class="form-control" style="min-height: 400px;width: 90%; font-family:Consolas,Monaco,Lucida Console,Liberation Mono,DejaVu Sans Mono,Bitstream Vera Sans Mono,Courier New, monospace;
"

rows="5" id="content">{{article['body']}}</textarea>
</div>


% rebase base title = "article"
