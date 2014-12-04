$(document).ready( function() {
    search_job_seeker_result();
});

// search result show by Ajax
function search_job_seeker_result(){
    $(".search").click( function(){
        var major = $('[name="major"]').val();
        var school = $('[name="school"]').val();
        var current_place = $('[name="current_place"]').val();
        var graduation_date = $('[name="graduation_date"]').val();
        var token = $('input[name="csrfmiddlewaretoken"]').prop('value');
        $.ajax({
            url: "/ucjobs/search_job_seeker_result",
            type: "POST",
            data: { csrfmiddlewaretoken: token, major: major, school: school, current_place: current_place, graduation_date: graduation_date},
            dataType: "html",
            success: function(html){
                // delete exist result and append new result
                $(".result").empty();
                $('.result').first().prepend(html);
            },
        });
        return false;
    });
}