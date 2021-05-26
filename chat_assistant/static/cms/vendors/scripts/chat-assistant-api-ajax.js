

function get_training_task_info(task_id){
  $.ajax({
    type: 'GET',
    url: 'http://127.0.0.1/api/train-assistant/',
    headers: {
      Authorization: 'Token 621142f5fb4b51e7468c9aefbb0bf374a2f07045'
    },
    data: {"task_id": task_id},
    success: function (data) {
      if(data.state !== 'SUCCESS'){
        setTimeout(function () {
          get_training_task_info(task_id)
        }, 2000);
      }
      else{
        $("#train-assistant div.spinner-border").addClass('d-none');
        $("#train-success-popup").click();
      }
    },
    error: function(){
      $("#train-assistant div.spinner-border").addClass('d-none');
      $("#train-error-popup").click();
    }
  });
}
function ajax_call_to_train(assistantId){
  const form_data = new FormData();
  form_data.append("id",assistantId);
  $.ajax({
      url: 'http://127.0.0.1/api/train-assistant/',
      type:'POST',
      headers: {
        Authorization: 'Token 621142f5fb4b51e7468c9aefbb0bf374a2f07045'
      },
      cache: false,
      processData: false,
      contentType: false,
      data: form_data,
      success: function (response) {
        $("#train-assistant div.spinner-border").removeClass('d-none')
        task_id = response['response'];
        get_training_task_info(task_id);

      }
    });
}