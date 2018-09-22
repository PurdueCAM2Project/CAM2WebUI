$('.card-deck-wrapper').on('click', function(event) {
    alert('You clicked the Bootstrap Card');
});


$("#search_criteria").on("keyup", function () {
    var criterion = $(this).val().toLowerCase();
    // $(".card .card-body .card-title, .card .card-body .card-subtitle, .card .card-body .card-text").each(function () {
    //     var string = $(this).text();
    //
    //     if(string.indexOf(criterion) != -1)
    //     {
    //         console.log("I'm hiding");
    //         $(this).parent().parent().hide();
    //     }
    //     else {
    //         console.log("I'm showing");
    //         $(this).parent().parent().show();
    //     }
    // });

    $(".card .card-body").each(function () {
        var paperInfo = $(this).find(".card-title").text().toLowerCase();
        var conference = $(this).find(".card-subtitle").text().toLowerCase();
        var authors = $(this).find(".card-text").text().toLowerCase();

        var existsInPaperInfo = paperInfo.includes(criterion);
        var existsInConference = conference.includes(criterion);
        var existsInAuthors = authors.includes(criterion);


        if(!existsInAuthors && !existsInConference && !existsInPaperInfo)
        {
            console.log("I'm hiding");
            $(this).parent().parent().hide();
        }
        else{
            console.log("I'm show");
             $(this).parent().parent().show();
        }
    })







});




