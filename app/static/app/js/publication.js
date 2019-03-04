$("#search_criteria").keyup(function(event) {
    if (event.keyCode === 13) {
        $("#search-button").click();
    }
});


$("#search-button").on("click", function () {
    var criterion = $("#search_criteria").val().toLowerCase();
    $(".card").each(function () {
        var paperInfo = $(this).find(".card-title").text().toLowerCase();
        var conference = $(this).find(".card-subtitle").text().toLowerCase();
        var authors = $(this).find(".card-text").text().toLowerCase();

        var existsInPaperInfo = paperInfo.includes(criterion);
        var existsInConference = conference.includes(criterion);
        var existsInAuthors = authors.includes(criterion);


        if(!existsInAuthors && !existsInConference && !existsInPaperInfo)
        {
            $(this).parent().hide();
        }
        else{
             $(this).parent().show();
        }
    })

});
