% rebase("index.tpl")
<section class="messaging">
    <form class="register" id="register" action="/register/user" method="post">
    <ul class="registerList">
        <li>
            <label><b>Username*</b></label>
            <input class="registerUsername" type="text" placeholder="Enter Username" name="nick" required>
        </li>
        <li>
            <label><b>Password*</b></label>
            <input class="registerPassword" type="password" placeholder="Enter Password" name="password" required>
        </li>
        <li>
            <label><b>Avatar</b></label>
            <input type="text" class="registerAvatar" placeholder="Enter link to image" name="avatar">
        </li>
        <li>
            <button class="registerButton" type="submit">Register</button>
        </li>
        <li>
            <div class="inputError"></div>
        </li>
    </ul>
    </form>
</section>