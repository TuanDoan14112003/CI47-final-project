let hideAdButton = document.querySelector('.ad-header button');
hideAdButton.addEventListener('click', () => {
    let adSection = document.getElementById('advertisement-slide');
    adSection.style.display = "none";
    //No social media actually hides ads forever
    setTimeout(() => {
        adSection.style.display = "block";
    }, 15000)
})