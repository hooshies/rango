$(document).ready(function(){
    $('h2#top').click(function () {
        $(this).next('div')
            .slideToggle()
            .toggleClass('displayed')
    });
});
