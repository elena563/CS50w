function create_post(event){
    event.preventDefault();
    let image = document.querySelector("#image").value;
    let content = document.querySelector("#content").value

    fetch('/post', 
      { method: "POST", body: JSON.stringify({image, content}), 
      headers: {"Content-Type": "application/json"} })
      .then(response => response.json())
      .then(result =>{
        console.log(result)
        window.location.href = '/';
      })
  }

document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('post-form').addEventListener('submit', create_post);
});

document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.like-btn').forEach(button => {
    button.addEventListener('click', function() {
      const postDiv = this.closest('.post');
      const postId = postDiv.getAttribute('data-post-id');
      fetch(`/like/${postId}/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      })
      .then(response => response.json())
      .then(data => {
        postDiv.querySelector('.like-count').textContent = data.likes;
      });
    });
  });
});

document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.edit-btn').forEach(button => {
    button.addEventListener('click', function() {
      const postDiv = this.closest('.post');
      postDiv.querySelector('.post-content').style.display = 'none';
      postDiv.querySelector('.edit-area').style.display = 'block';
      postDiv.querySelector('.save-btn').style.display = 'inline-block';
    });
  });

  document.querySelectorAll('.save-btn').forEach(button => {
    button.addEventListener('click', function() {
      const postDiv = this.closest('.post');
      const postId = postDiv.getAttribute('data-post-id');
      const newContent = postDiv.querySelector('.edit-area').value;
      fetch(`/edit/${postId}/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content: newContent })
      })
      .then(response => response.json())
      .then(data => {
        postDiv.querySelector('.post-content').textContent = data.content;
        postDiv.querySelector('.post-content').style.display = 'block';
        postDiv.querySelector('.edit-area').style.display = 'none';
        postDiv.querySelector('.save-btn').style.display = 'none';
      });
    });
  });
});