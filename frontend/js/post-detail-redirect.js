window.addEventListener('click', function(e){   
    if (!document.querySelector('.main-content-section').contains(e.target)){
        //redirect users to index if they click outside the modal
        //since we open up a new post-detail window, consider close the post-detail window if users wish to redirect to index
        window.location.href = "newsfeed.html";
        // window.close(); => this is to close window;
    }
});