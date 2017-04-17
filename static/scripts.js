$(document).ready(function(){

    $(".loginToggle").click(function(){
        $(".loginform").toggle();
    })

    $(".logoutToggle").click(function(){
            console.log("being hit")
        $(".logoutform").toggle();
    })
})

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