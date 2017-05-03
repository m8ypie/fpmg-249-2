% rebase("index.tpl")
<section class="messaging">
    <table class="users">
        %for rows in users:
            <tr class="test">
            %for user in rows:
                <td class="test">
                    <div class='userList'>
                        <img src={{user[1]}} class='profile'/>
                        <div class='name'><a href="/users/{{user[0]}}">{{user[0]}}</a></div>
                    </div>
                </td>
            %end
            </tr>
        %end
    </table>
</section>