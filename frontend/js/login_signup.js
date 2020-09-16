const loginSwitchBtn = document.querySelector('.form_switch .login_switch')
const signupSwitchBtn = document.querySelector('.form_switch .signup_switch')
loginSwitchBtn.addEventListener('click',() => {
    loginSwitchBtn.classList.add('active')
    signupSwitchBtn.classList.remove('active')
    document.getElementById('signup').style.display = 'none'
    document.getElementById('login').style.display = 'block'
})

signupSwitchBtn.addEventListener('click',() => {
    signupSwitchBtn.classList.add('active')
    loginSwitchBtn.classList.remove('active')
    document.getElementById('login').style.display = 'none'
    document.getElementById('signup').style.display = 'block'
})
