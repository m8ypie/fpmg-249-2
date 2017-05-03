<!DOCTYPE html>
<html>
<head lang="en">
    <meta charset="UTF-8">
    <meta name="author" content="Your Name">
    <title>Welcome to Psst!</title>
    <link rel="stylesheet" href="/static/psst.css" type="text/css">
    <script src='http://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js'></script>
    <script src="/static/scripts.js"></script>
</head>
<body>

<!-- these are sample psst messages to use in your design,
     use as many as you wish to best illustrate your
     design

     Note that you need to add other elements to this page - branding, navigation, links, advertising...
     -->
<div classes="staticBars">
    <section class="top">
        <img class="ico" src="/static/psst.png"/>
        <div class="nav">
            <ul>
                <li class="home"><a href="/">Home</a></li>
                <li class="users"><a href="/users">Users</a></li>
                <li class="about"><a href="/about">About</a></li>
                <li class="login">
                        %if logged_in=="True":
                            <a class="logoutToggle" href="#">{{nickname}}</a>
                            <form id="logoutform" class="logoutform" action="/logout" method="post"/>
                                <button type="submit">Logout</button>
                            </form>
                        %else:
                            <a class="loginToggle" href="#">Login</a>
                            <form id="loginform" class="loginform" action="/login" method="post">
                                <label><b>Username</b></label>
                                <input type="text" placeholder="Enter Username" name="nick" required>

                                <label><b>Password</b></label>
                                <input type="password" placeholder="Enter Password" name="password" required>

                                <button type="submit">Login</button>
                                <div class="registerText">Not a member? <a href="/register">Register here.</a></div>
                            {{loginFailed}}
                        %end
                    </form>
                </li>
            </ul>
        </div>
    </section>
    <div class='sidebar'>
        <div class="sidetitle">Whats trending?</div>
        <div class="sidenav">
            <ul>
                <li><a class="mentionsTrigger">Mentions</a></li>
                <li><a class="hashtagsTrigger">Hashtags</a></li>
            </ul>
        </div>
        <ul class='mentions', id="references"></ul>
        <ul class='hashtags', id="references"></ul>
    </div>
</div>

{{!base}}

</body>
</html>