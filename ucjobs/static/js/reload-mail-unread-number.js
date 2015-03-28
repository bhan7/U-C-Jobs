$(document).ready( function() {
	reload_mail_unread_number();
    setInterval(reload_mail_unread_number, 10000);
});


// mail refresh with number
function reload_mail_unread_number(){
    // alert("ok");
    $.ajax({
        url: "/ucjobs/reload_mail_unread_number",
        type: "GET",
        success: function(data){
            var mail_unread_number = data;
            document.getElementsByClassName('unread_number')[0].innerHTML = mail_unread_number;
        }
    });
}