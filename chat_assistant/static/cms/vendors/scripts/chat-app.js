$(document).ready(function () {
    setTimeout(function(){

        const chatBubbles = document.querySelectorAll('#mCSB_1 ul li a');
        const sendMessage = document.querySelector('#send-message');
        const chatProfileImage = $('.chat-profile-photo');
        const chatProfileName = $('.chat-profile-name');
        const chatOrganizationName = $('.chat-profile-name p');
        const chatChannelName = $('.chat-profile-name p');
        const typingAnimation = $('.chat-box .clearfix.typing-animation');
        

        for (let clickEventCounter = 0; clickEventCounter < chatBubbles.length; clickEventCounter++) {
            chatBubbles[clickEventCounter].addEventListener('click',  chatBubblesClickEvent.bind(this, clickEventCounter), false);
        }
        sendMessage.addEventListener('click',  sendMessageClickEvent.bind(this, 0), false);


        //start typing animation on key press
        $('#input-message').keyup(function(){
            setTimeout(function(){
                if ($('#input-message').val().length >= 1) {
                    typingAnimation.attr('class', 'clearfix typing-animation');
                    $("#mCSB_2").animate({ scrollTop: $("#mCSB_2")[0].scrollHeight}, 1000);
                }
                if ($('#input-message').val().length === 0) {
                    typingAnimation.attr('class', 'clearfix typing-animation d-none');
                    $("#mCSB_2").animate({ scrollTop: $("#mCSB_2")[0].scrollHeight}, 1000);
                }
            }, 500);
        });


        function UpdateActiveChatAssistant(){
            const activeChatImage = $("#mCSB_1 ul li.active img");
            const activeChatName = $("#mCSB_1 ul li.active h3");
            const activeChatOrganization = $("#mCSB_1 ul li.active p span.organization-name");
            const activeChatChannel = $("#mCSB_1 ul li.active p span.channel-name");
            const activeChatBubbleImg = activeChatImage.attr('src');
            const activeChatBubbleName = activeChatName.html();
            const activeOrganizationName = activeChatOrganization.html();
            const activeChannelName = activeChatChannel.html();
            chatProfileImage.children('img').attr('src', activeChatBubbleImg);
            chatProfileName.children('h3').html(activeChatBubbleName);
            chatOrganizationName.children('span.organization-name').html(activeOrganizationName);
            chatChannelName.children('span.channel-name').html(activeChannelName);
        }

        UpdateActiveChatAssistant()

        function chatBubblesClickEvent(elementCounter, element){
            const activeBubbleSelector = "#mCSB_1 ul li";
            
            const activeChatBubble = $(activeBubbleSelector);
           
            activeChatBubble.attr('class', '');  //remove active class from all elements
            activeChatBubble[elementCounter].className = 'active'; //add active class on current element

            UpdateActiveChatAssistant();
        }

        function sendMessageClickEvent(elementCounter, element){
            
            if ($('#input-message').val().length !== 0) {
                const collection = document.querySelectorAll('.clearfix.typing-animation.admin_chat');

                for (const elem of collection) {
                    elem.remove();
                }
                const message = $('#input-message').val();
                const requestMessageHtml = `<li class="clearfix">
                                                <span class="chat-img">
                                                    <img src="/static/vendors/images/chat-img2.jpg" alt="">
                                                </span>
                                                <div class="chat-body clearfix">
                                                    <p>`+ $('#input-message').val(); +`</p>
                                                    <div class="chat_time">09:40PM</div>
                                                </div>
                                            </li>`
                $('#input-message').val('');
                $(".chat-box ul li:last").before(requestMessageHtml);
                if ($('#input-message').val().length === 0) {
                    typingAnimation.attr('class', 'clearfix typing-animation d-none');
                }
                const responseMessageHtml = `<li class="clearfix typing-animation admin_chat">
                                                <span class="chat-img">
                                                    <img src="/static/vendors/images/logo-icon.png" alt="">
                                                </span>
                                                <div class="chat-body clearfix">
                                                <div class="chat-bubble">
                                                    <div class="typing">
                                                        <div class="dot"></div>
                                                        <div class="dot"></div>
                                                        <div class="dot"></div>
                                                    </div>
                                                </div>
                                                </div>
                                            </li>`
                setTimeout(function(){
                    $(".chat-box ul li:last").before(responseMessageHtml);
                }, 1000);
                const collectiveName = $("#mCSB_1 ul li.active a").attr('data-collective-name');
                const channelName = $("#mCSB_1 ul li.active a").attr('data-channel-name');
                const assistantName = $("#mCSB_1 ul li.active a").attr('data-assistant-name');
                
                askQuestionApiCall(collectiveName, channelName, assistantName, message);
            }
        }

        function askQuestionApiCall(collectiveName,channelName,assistantName, message) {
            console.log(collectiveName,channelName,assistantName, message)
            const form_data = new FormData();
            form_data.append("collective_name",collectiveName);
            form_data.append("channel_name",channelName);
            form_data.append("assistant_name",assistantName);
            form_data.append("question",message);
            $.ajax({
                url: "http://54.153.101.88/api/ask-question/",
                type:'POST',
                headers: {
                    Authorization: 'Token 43fabf04a553ce72448fc6c015f37f8d194fc05f'
                },
                data: form_data,
                cache: false,
                processData: false,
                contentType: false,
                // async: asyncValue,
                // timeout: 5000,
                success: function (response) {
                    // console.log(response)
                    if(response.length >=1){
                        const collection = document.querySelectorAll('.clearfix.typing-animation.admin_chat');

                        for (const elem of collection) {
                            elem.remove();
                        }

                        for(count = 0; count < response.length; count++){
                            // setTimeout(function(){
                                if(count == 0){
                                    let responseMessageHtml = `<li class="clearfix admin_chat">
                                                    <span class="chat-img">
                                                        <img src="/static/vendors/images/logo-icon.png" alt="">
                                                    </span>
                                                    <div class="chat-body clearfix">
                                                        <div class="chat-bubble">
                                                            <div class="chat-body clearfix">
                                                                <p>`+response[count].default+`</p>
                                                                <div class="chat_time">09:40PM</div>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </li>`
                                    $(".chat-box ul li:last").before(responseMessageHtml);
                                    
                                }
                                if(count == 1){
                                    let responseMessageHtml = `<li class="clearfix admin_chat">
                                                    <span class="chat-img">
                                                        <img src="/static/vendors/images/logo-icon.png" alt="">
                                                    </span>
                                                    <div class="chat-body clearfix">
                                                        <div class="chat-bubble">
                                                            <div class="chat-body clearfix">
                                                                <img width="300" src=`+response[count].default+`></img>
                                                                <div class="chat_time">09:40PM</div>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </li>`
                                    $(".chat-box ul li:last").before(responseMessageHtml);
                                }
                                // $("#div1").animate({ scrollTop: $('#div1').prop("scrollHeight")}, 1000);
                                
                            // }, 2000);
                        }
                        console.log(response);
                    
                    }
                    else{
                        // for file feature extractor
                        console.log("response ==>", response);
                        return response;
                    }
    
                },
                error: function (data) {

                }
            });
        }

    }, 2000);
});