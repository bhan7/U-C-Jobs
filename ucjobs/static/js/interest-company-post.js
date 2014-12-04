$(document).ready( function() {
    interest_company_post();
});

// click interest to add name by Ajax
function interest_company_post(){
    $(".interest-post").click( function(){
        var post_id = $(this).attr('post-id');
        $.ajax({
            url: "/ucjobs/interest_company_post/" + post_id,
            type: "GET",
            dataType: "html",
            success: function(html){
                $(".interest_list").empty();
                $(".interest_list").first().prepend(html);
            },
        });
        return false;
    });
}