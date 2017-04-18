% rebase("index.tpl")
<section class="messaging">
    %if logged_in=="True":
        <div class="psst", id="you">
            <div class='user'>
                <img class='profile', src="{{picture}}"/>
                <div class='name'>{{username}}</div>
            </div>
            <form id="postform" class="postform" action="/post" method="post">
                <textarea name="post" class="textbox", maxlength="200"></textarea>
                <input type="submit" value="Send"/>
            </form>
        </div>
    %end
    %for post in posts:
        <div class='psst'>
            <div class='user'>
                <img src={{post[3]}}, class='profile'/>
                <div class='name'><a href="/users/{{post[1]}}">{{post[1]}}</a></div>
            </div>
            <div class="timestamp">{{post[0]}}</div>
            <div class="message">{{post[2]}}</div>
        </div>
</messaging>
