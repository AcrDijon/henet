<div class="page-header">
  <h1>{{_('Edition of file')}} "{{ filename }}"</h1>
</div>


<form role="form" action="/category/{{category}}/{{filename}}" method="POST"  accept-charset="utf8">
 <input type="hidden" name="_csrf_token" value="{{ csrf_token }}">
 <div class="form-group">
   <label for="title">{{_('Title')}}:</label>
   <input class="form-control" id="title" type="text" name="title" value="{{ article['title'] }}"></input>
 </div>

 <div class="form-group">
   <label for="title">{{_('Location')}}:</label>
   <input class="form-control" name="location" id="location" type="text" value="{{ article['metadata'].get('location', '') }}"></input>
 </div>

 <div class="form-group">
   <label for="date">{{_('Date')}}:</label>
   <input class="form-control" id="date" name="date" type="text" value="{{article['metadata'].get('date', now).strftime('%Y-%m-%d') }}"></input>
 </div>

 <div class="form-group">
   <label for="eventdate">{{_('Event Date')}}:</label>
   <input class="form-control" id="eventdate" name="eventdate" type="text" value="{{article['metadata'].get('eventdate', now).strftime('%Y-%m-%d') }}"></input>
 </div>


 <div class="form-group">
    <textarea id="body" rows="5" id="content" name="body">{{article['body']}}</textarea>
    <iframe id="preview" src="/preview">
     Preview
    </iframe>
    <span style="clear: both"></span>
 </div>

 <button type="submit" id="save" class="btn btn-default">{{_('Save')}}</button>

</form>

<script src="/resources/js/editor.js"></script>
<script src="/resources/js/jquery-linedtextarea.js"></script>

<script>
 $('#date').datepicker({
   format: "yyyy-mm-dd",
   language: "fr"
 });

 $('#eventdate').datepicker({
   format: "yyyy-mm-dd",
   language: "fr"
 });


 $("#body").linedtextarea();

 window.baseTitle = $('head title').text();

 $('textarea#body').bind('change', genPreview);
 timerId = window.setInterval(genPreview, 900);

 //$('textarea#body').scroll(syncScrollPosition);
 $("#preview").height($("div.linedwrap").outerHeight());
 $("#preview").width($("div.linedwrap").outerWidth());

</script>

% rebase('base.tpl', page_title=article['title'], actionbar=False, span=12)
