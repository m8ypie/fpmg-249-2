% rebase("index.tpl")
<section class="messaging">
    <form class="register" action="/register">
        <label><b>Username*</b></label>
        <input class="registerUsername" type="text" placeholder="Enter Username" name="nick" required>/n

        <label><b>Password*</b></label>
        <input class="registerPassword" type="password" placeholder="Enter Password" name="password" required>

        <label><b>Avatar</b></label>
        <input type="text" placeholder="Enter link to image" name="avatar" required>

        <button class="registerButton" type="submit">Register</button>
    </form>
</section>