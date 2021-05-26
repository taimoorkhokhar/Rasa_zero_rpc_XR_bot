function ajax_call_to_train(assistantId){
  $.ajax({
      url: 'http://127.0.0.1/api/train-assistant/',
      data: {
        'assistant_id': assistantId,
      },
      dataType: 'json',
      success: function (data) {
        console.log("agent trained")
      }
    });
}