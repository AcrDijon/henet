<div class="page-header">
<h1>{{_('Moderate comments')}}</h1>
</div>

<table class="table table-striped">
  <thead>
  <tr>
   <th>{{_('Date')}}</th>
   <th>{{_('Author')}}</th>
   <th>{{_('Comment')}}</th>
   <th>{{_('Article')}}</th>
   <th>{{_('Actions')}}</th>
   </tr>
  </thead>
<tbody>
% for comment in comments:
<tr>
 <td>{{ comment.date.strftime('%d/%m/%Y') }}</td>
 <td>{{ comment.author }}</td>
 <td>
   <a href="#" data-toggle="tooltip" title="{{ comment.html }}">
     {{ comment.summary }}
   </a>
  </td>
 <td>
  {{comment.articles[0]}}
 </td>
 <td>
  <form action="/comments/{{ comment.uuid }}/activate"
        method="POST">
    <button type="submit" class="btn btn-xs btn-success">
      <span class="glyphicon glyphicon-ok"></span>
    </button>
  </form>
  <form action="/comments/{{ comment.uuid }}/reject"
        method="POST">
    <button type="submit" class="btn btn-xs btn-danger">
      <span class="glyphicon glyphicon-remove"></span>
    </button>
  </form>
 </td>

</tr>
% end
</tbody>
</table>

<script>
  $(document).ready(function(){
      $('[data-toggle="tooltip"]').tooltip();
  });
</script>

% rebase('base.tpl', page_title="_('Moderation')")
