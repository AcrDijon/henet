<div class="page-header">
  <h1>{{_('Edition of file')}} "{{ filename }}"</h1>
</div>


<form role="form" action="/page/{{page}}/{{filename}}" method="POST"  accept-charset="utf8">
  <input type="hidden" name="_csrf_token" value="{{ csrf_token }}">
  <div class="form-group">
   <label for="title">{{_('Title')}}:</label>
   <input class="form-control" id="title" type="text" name="title" value="{{ article['title'] }}"></input>
 </div>

 <div class="form-group">
   <label for="date">{{_('Date')}}:</label>
   <input class="form-control" id="date" name="date" type="text" value="{{article['metadata'].get('date', now).strftime('%d/%m/%Y') }}"></input>
 </div>


 <div class="form-group">
    <textarea rows="5" id="content" name="content">{{article['body']}}</textarea>
    <iframe id="preview" src="/preview">
     Preview
    </iframe>
    <span style="clear: both"></span>
 </div>

 <button type="submit" class="btn btn-default">{{_('Save')}}</button>

</form>

<script src="/resources/js/editor.js"></script>
<script src="/resources/js/jquery-linedtextarea.js"></script>

<script>
 $('#date').datepicker({
   format: "dd/mm/yyyy",
   language: "fr"
 });

 $("#content").linedtextarea();

 window.baseTitle = $('head title').text();

 $('textarea#content').bind('change', genPreview);
 timerId = window.setInterval(genPreview, 900);

 //$('textarea#content').scroll(syncScrollPosition);
 $("#preview").height($("div.linedwrap").outerHeight());
 $("#preview").width($("div.linedwrap").outerWidth());

</script>

% rebase('base.tpl', page_title=article['title'], actionbar=False, span=12)
