window.onload = function checkError(){
  var education_form = document.getElementById("education");
  var work_form = document.getElementById("work_exp");
  if (document.getElementsByClassName("errorlist").length > 0) {
    education_form.style.display = "block";
    work_form.style.display = "block";

  }
}


var i = 1;
function Education(a) {
	if((a+i)%2==1)
		document.getElementById("education").style.display="none";
	else
		document.getElementById("education").style.display="block";
	i = i + 1;
}

var j = 1;
function Work(a) {

	if((a+j)%2==1)
		document.getElementById("work_exp").style.display="none";
	else
		document.getElementById("work_exp").style.display="block";
	j = j + 1;
}
