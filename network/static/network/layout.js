function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');



document.addEventListener("DOMContentLoaded", function(){
    // edit post
    if (document.querySelector("#spaceedit")){
        document.querySelector("#spaceedit").style.display = "none";
    }
    document.querySelectorAll('.edit').forEach(edit => {
            edit.onclick = () => {            
            if(document.querySelector("#newpost")){
                document.querySelector("#newpost").style.display = "none";
            }

            if(document.querySelector("#allposts")){
                document.querySelector("#allposts").style.display = "none"
            }

            if (document.querySelector("#all")){
                document.querySelector("#all").style.display = 'none';
            }

            if (document.querySelector("#prev")){
                document.querySelector("#prev").style.display = "none";
            }
            if (document.querySelector("#next")){
                document.querySelector("#next").style.display = "none";
            }
            if (document.querySelector('#table')){
                document.querySelector("#table").style.display = "none";
            }
            document.querySelector("#spaceedit").style.display = "block";

            const div = edit.parentElement;
            edit_post_id= div.querySelector("b").dataset.id
            


    document.querySelector('#save').onclick = () => {
                edited_post = document.querySelector("#editarea").value
                fetch('/editposts', {
                    method: 'PUT',
                    headers: {
                        'X-CSRFToken': csrftoken
                    },
                    body: JSON.stringify({
                        new_content: edited_post,
                        edit_post_id: edit_post_id
                    })       
                }).then(response => response.json())
                .then(data =>{
                    div.querySelector(`[data-id="${edit_post_id}"]`).innerHTML = data.edited;
                    document.querySelector("#spaceedit").style.display = 'none';
                    document.querySelector("#allposts").style.display = "block";
                    document.querySelector("#newpost").style.display = "block";
                    document.querySelector("#all").style.display = 'block';

                    
                })
                .catch(error =>{
                    console.log("Error: ", error)
                }
                )

            }
        }
    });

    document.addEventListener('click', event => {
    const element = event.target
    if (element.className !== 'white' && element.className !== 'red') {
        return; 
    }
    let div = element.parentElement;
    let id = div.querySelector('b').dataset.id;
    let likes = div.querySelector('.num_of_likes')
    let message;
    if (element.className === "white") {
            console.log("like clicked");
            message = 'like';
        }

    else if (element.className === "red"){
            console.log("like clicked");
            message = 'dislike';
    }
    
    if (element.className === 'white' || element.className === 'red'){
        fetch("/editposts", {
            method: "POST",
            headers: {
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                message: message,
                post_id: id
                })
            })
        .then(response => response.json())
        .then(data => {
            if (data.error){
                console.log("Ошибка:", data.error);
                return;
            }
                console.log(data.likes)
                element.style.display = 'none';
                if (message === 'like'){
                    div.querySelector('.red').style.display = 'block';
                }
                else{
                    div.querySelector('.white').style.display = 'block';
                }
                likes.innerHTML = data.likes
                }
            )
        .catch(error => console.log("Error: ", error))
    }

})

})


// display all posts
function load_posts(){

}