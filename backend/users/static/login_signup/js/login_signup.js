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


// Day la backend

$('#signup_form input').on('input',function(){
    let field = this.id.split('_')[1]
    signup_field = '#'+'signup_' + field
    signup_field_error = signup_field + '_error'


    if ($(signup_field).val() == "") {
        $(signup_field_error).text("You must fill this field")
        $(signup_field_error).siblings("input").removeClass('valid')
        $(signup_field_error).siblings("input").addClass('invalid')
        
    } else {

        if (field === 'username' || field === 'email') {
            validate_username_email(field)
        }
        else if (field === 'password1' || field === 'password2') {
            validate_passwords()
        }
        
    }

})

function validate_username_email(field) { 
    if (field === 'username') {
        let $username_error = $('#signup_username_error')
        $.ajax({
            url: '/register/',
            data: {
                field: 'username',
                username: $('#signup_username').val()
            },
            success: function(response) {
                if (response.error !== 'success') {
                    $username_error.text(response.error)
                    $username_error.siblings("input").removeClass('valid')
                    $username_error.siblings("input").addClass('invalid')
                } else {
                    $username_error.text('')
                    $username_error.siblings("input").removeClass('invalid')
                    $username_error.siblings("input").addClass('valid')
                }
            }
        })
    }
    else if (field === 'email') {
        let $email_error = $('#signup_email_error')
        $.ajax({
            url: '/register/',
            data: {
                field: 'email',
                email: $('#signup_email').val()
            },
            success: function(response) {
                if (response.error !== 'success') {
                    $email_error.text(response.error)
                    $email_error.siblings("input").removeClass('valid')
                    $email_error.siblings("input").addClass('invalid')
                } else {
                    $email_error.text('')
                    $email_error.siblings("input").removeClass('invalid')
                    $email_error.siblings("input").addClass('valid')
                }
            }
        })
    }

}

function validate_passwords() {
    let $password1 = $('#signup_password1').val()
    let $password2 = $('#signup_password2').val()
    let $password1_error = $('#signup_password1_error')
    let $password2_error = $('#signup_password2_error')
    if ($password1.length<8) {
        $password1_error.text('Your password is too short')
        $password1_error.siblings("input").removeClass('valid')
        $password1_error.siblings("input").addClass('invalid')
    } else {
        $password1_error.text('')
        $password1_error.siblings("input").removeClass('invalid')
        $password1_error.siblings("input").addClass('valid')
    }
    if ($password1 !== $password2) {
        $password2_error.text("Passwords don't match")
        $password2_error.siblings("input").removeClass('valid')
        $password2_error.siblings("input").addClass('invalid')
    } else{
        $password2_error.text("")
        $password2_error.siblings("input").removeClass('invalid')
        $password2_error.siblings("input").addClass('valid')
    }
}