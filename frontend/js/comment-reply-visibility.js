// reply-button
// individual-reply

const replySections = document.querySelectorAll('.individual-reply');
const replyButtons = document.querySelectorAll('.reply-button');
// replySections.style.display = "none";

let replyID = 0;
let buttonID = 0;

replySections.forEach(replySec => {
    replySec.setAttribute('id', "replyID"+replyID);
    replySec.style.display = "none";
    replyID++;
});
replyButtons.forEach(replyButton => {
    replyButton.setAttribute('id', "buttonID"+buttonID);
    buttonID++;
});

function displayHideForm (id)  {
    const numericID = id.replace("buttonID",'');    
    const replyForm = document.getElementById(`replyID${numericID}`);
    // console.log(replyForm.style.display);
    
    if (replyForm.style.display == "none" ) {
        replyForm.style.display = "block";
    } else {
        replyForm.style.display = "none";

    }


    // let formDisplaying = false;
    // if (!formDisplaying) {
    //     replyForm.style.display == "block";
    //     formDisplaying = true;
    // } else {
    //     replyForm.style.display == "none";
    //     formDisplaying = false;
    // }
}