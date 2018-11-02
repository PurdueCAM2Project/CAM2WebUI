$('.card-deck-wrapper').on('click', function(event) {
    alert('You clicked the Bootstrap Card');
});


$("#search-button").on("click", function () {
    var criterion = $("#search_criteria").val().toLowerCase();
    $(".card .card-body").each(function () {
        var paperInfo = $(this).find(".card-title").text().toLowerCase();
        var conference = $(this).find(".card-subtitle").text().toLowerCase();
        var authors = $(this).find(".card-text").text().toLowerCase();

        var existsInPaperInfo = paperInfo.includes(criterion);
        var existsInConference = conference.includes(criterion);
        var existsInAuthors = authors.includes(criterion);


        if(!existsInAuthors && !existsInConference && !existsInPaperInfo)
        {
            $(this).parent().parent().hide();
        }
        else{
             $(this).parent().parent().show();
             // $(this).parent().parent().toggle("highlight");
        }
    })

});




