let hideAdButton = document.querySelector('.ad-header button');
let hideAdButton2 = document.querySelector('.ad-header-2 button');

hideAdButton.addEventListener('click', () => {
    let adSection = document.getElementById('advertisement-slide');
    adSection.style.display = "none";
    //No social media actually hides ads forever
    setTimeout(() => {
        adSection.style.display = "block";
    }, 15000)
})
hideAdButton2.addEventListener('click', () => {
    let adSection = document.getElementById('advertisement-slide-2');
    adSection.style.display = "none";
    //No social media actually hides ads forever
    setTimeout(() => {
        adSection.style.display = "block";
    }, 15000)
})

// Day la phan backend

function vote(voteButton) {
    
    var $voteDiv = $(voteButton).parent().parent();
    var $data = $voteDiv.data();
    var direction_name = $(voteButton).attr('title');
    var vote_value = null;
    if (direction_name == "upvote") {
        vote_value = 1;
    } else if (direction_name == "downvote") {
        vote_value = -1;
    } else {
        return;
    }
    $.ajax({
        type: 'POST',
        url: '/vote/',
        data: {
            what: $data.whatType,
            what_id: $data.whatId,
            vote_value: vote_value,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(response) {
                    if (response.error == null) {
            var voteDiff = response.voteDiff;
            var $score = null;
            var $upvoteArrow = null;
            var $downArrow = null;
            if ($data.whatType == 'post') {
                $score = $voteDiv.find("p.score");
                $upvoteArrow = $voteDiv.children("div").children('i.fas.fa-arrow-alt-circle-up');
                $downArrow = $voteDiv.children("div").children('i.fas.fa-arrow-alt-circle-down');
            } 
            // else if ($data.whatType == 'comment') {
            //     var $medaiDiv = $voteDiv.parent().parent();
            //     var $votes = $medaiDiv.children('div.media-left').children('div.vote').children('div');
            //     $upvoteArrow = $votes.children('i.fa.fa-chevron-up');
            //     $downArrow = $votes.children('i.fa.fa-chevron-down');
            //     $score = $medaiDiv.find('div.media-body:first').find("a.score:first");

            // }

            // update vote elements

            if (vote_value == -1) {
                if ($upvoteArrow.hasClass("voted")) { // remove upvote, if any.
                    $upvoteArrow.removeClass("voted")
                }
                if ($downArrow.hasClass("voted")) { // Canceled downvote
                    $downArrow.removeClass("voted")
                } else {                                // new downvote
                    $downArrow.addClass("voted")
                }
            } else if (vote_value == 1) {               // remove downvote
                if ($downArrow.hasClass("voted")) {
                    $downArrow.removeClass("voted")
                }

                if ($upvoteArrow.hasClass("voted")) { // if canceling upvote
                    $upvoteArrow.removeClass("voted")
                } else {                                // adding new upvote
                    $upvoteArrow.addClass("voted")
                }
            }

            // update score element
            var scoreInt = parseInt($score.text());
            $score.text(scoreInt += voteDiff);
        }
        }
    })

}
