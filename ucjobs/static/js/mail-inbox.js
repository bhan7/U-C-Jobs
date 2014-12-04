window.onload = function() {
	if (!document.getElementsByClassName("mail_read")) return false;
	var mails = document.getElementsByClassName("mail_read");
	for (var i=0; i<mails.length; i++) {
		mails[i].style.fontWeight="bold";
	}
}
