// follow and unfollow
document.addEventListener("DOMContentLoaded", function(){
    document.querySelector('#follow').onclick = function(){
        fetch(`/follow_unfollow/${want_follow}`, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrftoken
            },

            body: JSON.stringify({
                message: "follow"
        })
        }).then(response => response.json())
        .then(data => {
            console.log(data.error)
            document.querySelector('#follow').style.display = 'none';
            document.querySelector('#unfollow').style.display = 'block';
            document.querySelector("#follower").innerHTML = data.follower;
            document.querySelector("#following").innerHTML = data.following;
        })
    }

        document.querySelector('#unfollow').onclick = function(){
        fetch(`/follow_unfollow/${want_follow}`, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrftoken
            },

            body: JSON.stringify({
                message: "unfollow"
            })
        }).then(response => response.json())
        .then(data => {
            console.log(data.error)
            document.querySelector('#unfollow').style.display = 'none';
            document.querySelector('#follow').style.display = 'block';
            document.querySelector("#follower").innerHTML = data.follower;
            document.querySelector("#following").innerHTML = data.following;

        })
    }
})


