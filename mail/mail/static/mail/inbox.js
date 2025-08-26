function send_email(event){
    event.preventDefault();
    let recipients = document.querySelector("#compose-recipients").value;
    let subject = document.querySelector("#compose-subject").value;
    let body = document.querySelector("#compose-body").value

    fetch('/emails', 
      { method: "POST", body: JSON.stringify({recipients, subject, body}), 
      headers: {"Content-Type": "application/json"} })
      .then(response => response.json())
      .then(result =>{
        console.log(result)
        load_mailbox('sent');
      })
  }

document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  document.getElementById('compose-form').addEventListener('submit', send_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

}

function reply(recipients, subject, body, timestamp) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = recipients;
  document.querySelector('#compose-subject').value = `Re: ${subject}`;
  document.querySelector('#compose-body').value = `On ${timestamp} ${recipients} wrote: ${body}`;
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  function view_email(id) {
    document.querySelector('#emails-view').style.display = 'none';
    const email_view = document.querySelector('#email-view');
    email_view.style.display = 'block';
    email_view.innerHTML = '';

    fetch(`/emails/${id}`)
    .then(response => response.json())
      .then(email => {
        console.log(email)
      email_view.innerHTML = `
        <h3>${email.subject}</h3>
        <p><strong>From:</strong> ${email.sender}</p>
        <p><strong>To:</strong> ${email.recipients}</p>
        <p><strong>Subject:</strong> ${email.subject}</p>
        <p><strong>Timestamp:</strong> ${email.timestamp}</p>
        <span></span>
        <hr>
        <p>${email.body}</p>
      `;
          
          if (mailbox !== 'sent'){
            const element = document.createElement('button');
            element.innerHTML = `Reply`;
            element.classList.add('btn', 'btn-sm', 'btn-outline-primary')
            element.addEventListener('click', () => reply(email.sender, email.subject, email.body, email.timestamp));
            document.querySelector('span').append(element);

            const archive_btn = document.createElement('button');
            archive_btn.classList.add('btn', 'btn-sm', 'btn-outline-primary')
            if (mailbox == 'archive'){
            archive_btn.innerHTML = 'Unarchive';
            archive_btn.addEventListener('click', function(){
              fetch(`/emails/${id}`, {
                method: 'PUT',
                body: JSON.stringify({
                  archived: false
                })
              })
              .then(() => load_mailbox('inbox'))
            });
          } else{
            archive_btn.innerHTML = 'Archive';
            archive_btn.addEventListener('click', function(){
              fetch(`/emails/${id}`, {
                method: 'PUT',
                body: JSON.stringify({
                  archived: true
                })
              })
              .then(() => load_mailbox('inbox'))
            });
          }
            document.querySelector('span').append(archive_btn);
          }
          
          
          
        });

    fetch(`/emails/${id}`, {
      method: 'PUT',
      body: JSON.stringify({
        read: true
      })
    })
  }

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
    .then(result =>{
      console.log(result)
      result.forEach(email => {
        const element = document.createElement('div');
        if (mailbox == 'sent'){
          element.innerHTML = `<p><strong>${email.recipients}</strong>${email.subject}</p><p>${email.timestamp}</p>`;
        }else{
          element.innerHTML = `<p><strong>${email.sender}</strong>${email.subject}</p><p>${email.timestamp}</p>`;
        }
        element.classList.add(email.read ? 'read' : 'unread');
        element.addEventListener('click', () => view_email(email.id));
        document.querySelector('#emails-view').append(element);
      });
    })
}