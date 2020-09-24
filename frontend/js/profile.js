const to_top_btn = document.querySelector('.main-content-right .to-top-btn')
window.onscroll = function() {scrollFunction()};
function scrollFunction() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
      to_top_btn.style.display = "block";
    } else {
      to_top_btn.style.display = "none";
    }
  }
to_top_btn.addEventListener('click',()=>{
    document.documentElement.scrollTop = 0;
})