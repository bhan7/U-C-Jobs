$(document).ready( function() {
    search_company_result();
});

// search result show by Ajax
function search_company_result(){
    $(".search").click( function(){
        var location = $('[name="location"]').val();
        var company_type = $('[name="company_type"]').val();
        var company_name = $('[name="company_name"]').val();
        var token = $('input[name="csrfmiddlewaretoken"]').prop('value');
        $.ajax({
            url: "/ucjobs/search_company_result",
            type: "POST",
            data: { csrfmiddlewaretoken: token, location: location, company_type: company_type, company_name: company_name},
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