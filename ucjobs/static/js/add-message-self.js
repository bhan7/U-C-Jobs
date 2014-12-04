function add_message_self(){
    var company_profile_id = $(".post-message").attr('company-profile-id');
    var content = $('[name="content"]').val();
    var token = $('input[name="csrfmiddlewaretoken"]').prop('value');
    $.ajax({
        url: "/ucjobs/add_message_job_seeker/" + company_profile_id,
        type: "POST",
        data: { csrfmiddlewaretoken: token, content: content},
        dataType: "html",
        success: function(html){
                // delete exist message and append new message
                $('.messages').empty();
                $('.messages').first().prepend(html);
            },
        });
    return false;
}

function replyMessage(id) {
    var to = id.parentNode.childNodes[1].innerHTML;
    var reply_message = document.getElementById("message_input");
    reply_message.value = '@' + to + ': ';
    reply_message.focus();
}