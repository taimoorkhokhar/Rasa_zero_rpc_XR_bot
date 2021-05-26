$(document).ready(function () {
    
    const updateAssistantData = document.querySelector('#save-assistant-data');
    const trainAssistant = document.querySelector('#train-assistant');

    updateAssistantData.addEventListener('click',  updateAssistantDataClickEvent.bind(this), false);
    trainAssistant.addEventListener('click',  trainAssistantClickEvent.bind(this), false);

    function trainAssistantClickEvent(element){
        assistantId = element.currentTarget.getAttribute('data-assistant-id');

        ajax_call_to_train(assistantId)
    }

    function updateAssistantDataClickEvent(){
        const updateAssistantDataArr = []
        $("#edit-assistant-table div.table-responsive table tbody tr").each(function() {
            intent = $(this).attr('data-intent');
            assistantId = $(this).attr('data-assistant-id');
            intentDict = {}
            intentDict[intent] = {"removedQuestions":[],"unsavedQuestions":[],"removedResponses":[],"unsavedResponses":[]}
            $(this).find("option[data-status='removed']").each(function(){ 
                if($(this).attr('class') === 'questions-option'){
                    intentDict[intent].removedQuestions.push($(this).html());
                }
                else if($(this).attr('class') === 'responses-option'){
                    intentDict[intent].removedResponses.push($(this).html());
                }
            })
            $(this).find("option[data-status='unsaved']").each(function(){
                var td = $(this).closest('td');
                var th = td.closest('table').find('th').eq(td.index());
                var headerName = th.html();

                if(headerName == 'Questions'){
                    intentDict[intent].unsavedQuestions.push($(this).html());
                }
                else if(headerName == 'Responses'){
                    intentDict[intent].unsavedResponses.push($(this).html());
                }
            })
            if( intentDict[intent].removedQuestions.length !== 0 || intentDict[intent].unsavedQuestions.length !== 0 ||
                intentDict[intent].removedResponses.length !== 0 || intentDict[intent].unsavedResponses.length !== 0
            ){
                updateAssistantDataArr.push(intentDict);
            }
        });
        console.log(updateAssistantDataArr);
        const form_data = new FormData();
        form_data.append("assistant_id",assistantId);
        form_data.append("data",JSON.stringify(updateAssistantDataArr));
        $.ajax({
            url: "http://127.0.0.1/cms/update_assistant_examples",
            type: "POST",
            headers: {
                Authorization: 'Token 621142f5fb4b51e7468c9aefbb0bf374a2f07045'
            },
            data: form_data,
            cache: false,
            processData: false,
            contentType: false,
            success: function (response) {
                location.reload()
            },
            error: function (data) {

            }
        });
    }
});