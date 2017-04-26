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
        registerButton.disabled = true
        usernameInput.change(function(){verification(usernameInput, passwordInput, registerButton, errorMessage)})
        passwordInput.change(function(){verification(usernameInput, passwordInput, registerButton, errorMessage)})
    }

    $(".mentionsTrigger").click(function(){
        console.log("mentions outer")
        if(!$(".mentions").is(":visible")){
        console.log("mentions inner")
            $(".mentions").toggle()
            $(".hashtags").toggle()
        }
    })
    $(".hashtagsTrigger").click(function(){
        console.log("hashtags outer")
        console.log($(".hashtags").is(":visible"))
        if(!$(".hashtags").is(":visible")){
            console.log("hashtags inner")
            $(".mentions").toggle()
            $(".hashtags").toggle()
        }
    })
})



function verification(usernameInput, passwordInput, registerButton, errorMessage) {
    usernameInput.css("border","2px inset rgb(0, 0, 0)")
    passwordInput.css("border","2px inset rgb(0, 0, 0)")
    errorMessage.text("")
    var text = usernameInput.val()
    console.log(text)
    if(text.length > 6){
        $.ajax({
            type:"POST",
            url: "/register/validation",
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            data: JSON.stringify({"nick":text}),
            success: function(data){
                console.log("hi")
                console.log("here")
                if(!data.invalid){
                    passwordInput.css("border","2px inset rgb(0, 0, 0)")
                    if(passwordInput.val().length > 8){
                        registerButton.disabled = false
                    }else{
                        console.log("here?")
                        passwordInput.css("border","2px inset red")
                        errorMessage.text("Password must be at least 8 characters long")
                    }
                }else{
                    console.log("or here?")
                    usernameInput.css("border","2px inset red")
                    errorMessage.text(data.invalid)
                }
            },
            error: function(err){console.log(err)}
            })
    }else{
        console.log("or here")
        errorMessage.text("Username must be al least 6 characters long")
        usernameInput.css("border","2px inset red")
    }
    console.log(errorMessage.text())
}


function getMentions(){
    $.get("/mentioncount",
    function(data, status){
         var mentionsList = document.getElementsByClassName("mentions")[0]
         console.log(mentionsList)
         var mentions = data.mentions
         for (mention in mentions){
             var item = document.createElement('li')
             var a = document.createElement('a')
             a.appendChild(document.createTextNode(mentions[mention][0]))
             a.setAttribute("href", "/users/"+mentions[mention][0].replace('@', ''))
             item.appendChild(a)
             mentionsList.appendChild(item)
         }
    })
}

function getHashtags(){
    $.get("/hashtagcount",
    function(data, status){
        var hashtagList = document.getElementsByClassName("hashtags")[0]
        var hashtags = data.hashtags
        for(hashtag in hashtags){
            var item = document.createElement('li')
            item.appendChild(document.createTextNode(hashtags[hashtag][0]))
            hashtagList.appendChild(item)
        }
    })
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