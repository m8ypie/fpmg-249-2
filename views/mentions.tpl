% rebase("index.tpl")
<section class="messaging">
    <div class="psst", id="you">
        <div class='user'>
            <img class='profile', src="{{userpic}}"/>
            <div class='name'>@{{name}}</div>
        </div>
    </div>
    %for post in posts:
        <div class='psst'>
            <div class='user'>
                <img src={{post[3]}}, class='profile'/>
                <div class='name'><a href="/users/{{post[1]}}">{{post[1]}}</a></div>
            </div>
            <div class="timestamp">{{post[0]}}</div>
            <div class="message">{{!post[2]}}</div>
        </div>
</messaging>
