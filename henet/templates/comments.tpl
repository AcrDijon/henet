<div class="page-header">
<h1>Modération des commentaires</h1>
</div>

<table class="table table-striped">
  <thead>
  <tr>
   <th>Date</th>
   <th>Auteur</th>
   <th>Commentaire</th>
   <th>Activer</th>
   <th>Rejeter</th>
   </tr>
  </thead>
<tbody>
% for comment in comments:
<tr>
 <td>{{ comment.date.strftime('%d/%m/%Y') }}</td>
 <td>{{ comment.author }}</td>
 <td>
   <a href="#" data-toggle="tooltip" title="Commentaire complet: {{ comment.text }}">
     {{ comment.summary }}
   </a>
  </td>
 <td>
  <form action="/comments/{{ comment.uuid }}/activate"
        method="POST">
    <button type="submit" class="btn btn-xs btn-success">
      <span class="glyphicon glyphicon-ok"></span>
    </button>
  </form>
 </td>
 <td>
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

% rebase('base.tpl', page_title="Modération")
