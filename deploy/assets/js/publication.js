// Publications Filter
// This Javascript file filters the publications by name, conference, etc.
// It is only used on the list view of the publications page. The card view
// is handled in the Python file app/views/publications.py

// Allow for the user to press the enter key to search the publications
$("#search_criteria").keyup(function(event) {
    if (event.keyCode === 13) {
        $("#search-button").click();
    }
});


// Filter the cards to see if the text in the cards contains the string being queried
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