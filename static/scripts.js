
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
        var registerButton = $(".registerButton")
        registerButton.prop('disabled', true)
        usernameInput.change(function(){verification(usernameInput, passwordInput, registerButton, errorMessage)})
        passwordInput.change(function(){verification(usernameInput, passwordInput, registerButton, errorMessage)})
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



function verification(usernameInput, passwordInput, registerButton, errorMessage) {
    usernameInput.css("border","2px inset rgb(0, 0, 0)")
    passwordInput.css("border","2px inset rgb(0, 0, 0)")
    errorMessage.text("")
    var text = usernameInput.val().trim()
    if(text.length > 6){
        $.ajax({
            type:"POST",
            url: "/register/validation",
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            data: JSON.stringify({"nick":text}),
            success: function(data){
                if(!data.invalid){
                    passwordInput.css("border","2px inset rgb(0, 0, 0)")
                    if(passwordInput.val().length > 8){
                        registerButton.prop('disabled', false)
                    }else{
                        passwordInput.css("border","2px inset red")
                        errorMessage.text("Password must be at least 8 characters long")
                        registerButton.prop('disabled', true)
                    }
                }else{
                    usernameInput.css("border","2px inset red")
                    errorMessage.text(data.invalid)
                    registerButton.prop('disabled', true)
                }
            }
            })
    }else{
        errorMessage.text("Username must be al least 6 characters long")
        usernameInput.css("border","2px inset red")
        registerButton.prop('disabled', true)
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

function attemptLogin(){
    var uname = document.getElementById("uname").value
    var pwd = document.getElementById("pwd").value
    $.post("/login",
    {
        username:uname,
        passwrod:pwd
    },
    function(data, status){

    })
}

function main(){
    getMentions()
    getHashtags()
}

main()

//        <ul class='mentions'>
//            %for mention in mentions:
//                <li href="/users/{{mention[0]}}">{{mention[1]}}</li>
//            %end
//        </ul>
//        <ul class='hashtags'>
//            %for hashtag in hashtags:
//                <li href='#'>{{hashtag}}</li>
//            %end
//        </ul>