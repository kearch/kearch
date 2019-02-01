import M from "materialize-css";
import "../css/index.scss";
import $ from 'jquery';

document.addEventListener('DOMContentLoaded', function() {
  M.AutoInit();
});

window.deleteAConnectionRequest = (me_host) => {
  console.log({ me_host });
  console.log({ data: $(this).data() });
  if (confirm('Are you sure?')) {
    $.ajax({
      url: '/sp/admin/delete_a_connection_request',
      type: 'DELETE',
      data: { me_host },
    }).done(() => {
      window.location.replace('/');
    }).fail(() => {
      alert("Failed to delete a connection request.");
    })
  }
}
