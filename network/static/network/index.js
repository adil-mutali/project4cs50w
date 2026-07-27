// add new post
document.addEventListener("DOMContentLoaded", function(){
    document.querySelector('#post').onclick = () => {
        const post_content = document.querySelector('#text').value
        fetch('/posts/new', {
            method: "POST",
            headers: {
                "X-CSRFToken": csrftoken
            },

            body: JSON.stringify({
                post_content: post_content
            })
        }).then(response => response.json())
        .then(data => {
    const newPostHTML = `
        <div style="border: solid 2px;">
            <h1><a href="/${data.user_id}">${data.username}</a></h1>
            <button class="edit">Edit</button>
            <p><b data-id="${data.id}">${data.post_content}</b></p>
            <p>${data.timestamp}</p>
            <span class="white">🤍</span>
            <span class="red" style="display:none">❤️</span>
            <b class="num_of_likes">0</b>
        </div>
    `;
    document.querySelector('#allposts').insertAdjacentHTML('afterbegin', newPostHTML);
    document.querySelector('#text').value = '';
})
    }

})


