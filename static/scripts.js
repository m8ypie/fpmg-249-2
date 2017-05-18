
$(document).ready(function(){

    $(".loginToggle").click(function(){
        $(".loginform").toggle();
    })

    $(".logoutToggle").click(function(){
        $(".logoutform").toggle();
    })
    var usernameInput = $(".registerUsername")
    if(usernameInput){
        var errorMessage = $(".inputError")
        var passwordInput = $(".registerPassword")
        var avatarInput = $(".registerAvatar")
        var registerButton = $(".registerButton")
        registerButton.prop('disabled', true)
        usernameInput.change(function(){verification(usernameInput, passwordInput, avatarInput, registerButton, errorMessage)})
        passwordInput.change(function(){verification(usernameInput, passwordInput, avatarInput, registerButton, errorMessage)})
        avatarInput.change(function(){verification(usernameInput, passwordInput, avatarInput, registerButton, errorMessage)})
    }

    $(".mentionsTrigger").click(function(){
        if(!$(".mentions").is(":visible")){
            $(".mentions").toggle()
            $(".hashtags").toggle()
        }
    })
    $(".hashtagsTrigger").click(function(){
        if(!$(".hashtags").is(":visible")){
            $(".mentions").toggle()
            $(".hashtags").toggle()
        }
    })
})

function validationError(field, errorMessage, button, errorField){
    field.css("border","2px inset red")
    errorField.text(errorMessage)
    button.prop('disabled', true)
}


function verification(usernameInput, passwordInput, avatarInput, registerButton, errorMessage) {
    usernameInput.css("border","1px inset rgb(0, 0, 0)")
    passwordInput.css("border","1px inset rgb(0, 0, 0)")
    avatarInput.css("border","1px inset rgb(0, 0, 0)")
    errorMessage.text("")
    var text = usernameInput.val()
    isValidUsername(text, function(error){
        if(error){
            validationError(usernameInput, error, registerButton, errorMessage)
        } else {
            passwordInput.css("border","1px inset rgb(0, 0, 0)")
            var pw = passwordInput.val() 
            if(pw.length >= 6){
                avatarInput.css("border","1px inset rgb(0, 0, 0)")
                console.log("hi ", isValidAvatar(avatarInput.val()))
                if(isValidAvatar(avatarInput.val())){
                    registerButton.prop('disabled', false)
                }else{
                    validationError(avatarInput, "Invalid url, must point to either png or jpg", registerButton, errorMessage)
                }
            }else{
                validationError(passwordInput, "Password must be at least 6 characters long", registerButton, errorMessage)
            }
        }
    })               
}


function isValidAvatar(avatarInput){
    var httpRegex = /(https?:\/\/.*\.(?:png|jpg))/i
    var valid = false
    console.log(avatarInput.length < 1)
    if(avatarInput.length < 1){
        console.log("HERE")
        valid = true
    }else{
        if(httpRegex.test(avatarInput)){
            valid = true
        }else{
            valid = false
        }
    }
    return valid
}

function isValidUsername(text, cb){
    var regex = /^[a-z0-9]+$/i;
    if(regex.test(text)){
        if(text.length >= 4){
            $.ajax({
                type:"POST",
                url: "/register/validation",
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                data: JSON.stringify({"nick":text}),
                success: function(data){
                    if(!data.invalid){
                        cb()
                    }else{
                        cb(data.invalid)
                    }
                }
            })
        }else{
            cb("Username must be at least 4 characters long")
        }
    }else{
        cb("Username contains invlaid characters")
    }
}

function getMentions(){
    $.get("/mentioncount",
        function(data, status){
            var mentionsList = document.getElementsByClassName("mentions")[0]
            var mentions = data.mentions
            for (mention in mentions){
                var item = document.createElement('li')
                var a = document.createElement('a')
                a.appendChild(document.createTextNode(mentions[mention][0]))
                a.setAttribute("href", "/users/"+mentions[mention][0].replace('@', ''))
                item.appendChild(a)
                mentionsList.appendChild(item)
            }
        }
    )
}

function getHashtags(){
    $.get("/hashtagcount",
        function(data, status){
            var hashtagList = document.getElementsByClassName("hashtags")[0]
            var hashtags = data.hashtags
            for(hashtag in hashtags){
                var item = document.createElement('li')
                var a = document.createElement('a')
                a.appendChild(document.createTextNode(hashtags[hashtag][0]))
                a.setAttribute("href", "/hashtags/"+hashtags[hashtag][0].replace('#', ''))
                item.appendChild(a)
                hashtagList.appendChild(item)
            }
        }
    )
}

function main(){
    getMentions()
    getHashtags()
}

main()