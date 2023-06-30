document.addEventListener('DOMContentLoaded', function () {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // Send email when user submits composition form
  document.querySelector('#compose-form').onsubmit = (event) => {
    event.preventDefault();
    console.log('before compose');
    const recipients = document.querySelector('#compose-recipients').value;
    const subject = document.querySelector('#compose-subject').value;
    const body = document.querySelector('#compose-body').value;

    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
      })
    })
      .then(response => response.json())
      .then(result => {
        //Redirect to Sent
        console.log(result);
        console.log('before load mailbox()');
        //loading sent mailbox after sending email
        load_mailbox('sent');
      });
  }

});

function compose_email() {

  // Show compose view and hide other views
  console.log('COME TO COMPOSE');

  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#openmail-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';


}

function load_mailbox(mailbox) {

  console.log('COME TO mailbox');

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#openmail-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';


  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  console.log(`come to ${mailbox} emails`);

  //fetching emails as per mailbox
  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
      console.log("before loading emails");
      console.log(emails);

      emails.forEach(email => {

        //Create condition to load appropriate emails

        //create a div for each email
        const div = document.createElement('div');
        div.className = 'btn-light'
        div.id = `${email.id}`;
        div.innerHTML = `${email.id} - ${email.sender} - ${email.subject} - ${email.timestamp}`;

        //Adding a lisrtener to when email was clicked
        div.addEventListener('click', function () {
          console.log(`This email with id - ${div.id} was clicked!`)
          //view_email(`${div.id}`);
          view_email(email.id, mailbox);
        });
        document.querySelector('#emails-view').append(div);
      });

    });
  console.log('after loading email');
}

function view_email(emailid, mailbox) {

  console.log('Come to open mail')

  //Show open mail and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#openmail-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  document.querySelector('#openmail-view').innerHTML = `<h3>${emailid}</h3>`;

  //fetching email respective to id
  fetch(`/emails/${emailid}`)
    .then(response => response.json())
    .then(email => {
      console.log(email);


      console.log('element created');

      //Opening email
      //Add archive/unarchive and reply as event listeners
      document.querySelector('#openmail-view').innerHTML = `
      <h3>${email.id}</h3>
      <h4>EmailSender:${email.sender}</h4>
      <h4>EmailRecipient:${email.recipients}</h4>
      <h5>Subject:${email.subject}</h5>
      <p>Body:${email.body}</p>
      <br>
      <p>Timestamp:${email.timestamp}`;

      console.log('loading archive button');

      //explore alternative way to test this condition
      //if (request.user.email !== email.sender) {
      const archive_button = document.createElement('button');
      archive_button.className = 'btn-dark';
      if (email.archived !== true) {
        archive_button.textContent = 'Archive';
        archive_button.id = email.id;
      }
      else if (email.archived === true) {
        archive_button.textContent = 'Unarchive';
        archive_button.id = email.id;
      }
      //This is executing automatically. Must assosciate with button
      console.log('Before clicking');
      archive_button.addEventListener('click', function () {
        console.log('button was clicked');
        archive_unarchive(email.id, archive_button.textContent);
      })

      document.querySelector('#openmail-view').append(archive_button);
      console.log('loaded archive button');
      //}


      //Making emails read after opening
      fetch(`/emails/${email.id}`, {
        method: 'PUT',
        body: JSON.stringify({
          read: true
        })
      })
      console.log('mail-read');
    });
}



function archive_unarchive(emailid, archive_status) {

  console.log('come to archive/unarchive');

  if (archive_status === 'Archive') {
    fetch(`/emails/${emailid}`, {
      method: 'PUT',
      body: JSON.stringify({
        archived: true
      })

    })
    console.log('archived');
    load_mailbox('inbox');
  }

  else if (archive_status === 'Unarchive') {
    fetch(`/emails/${emailid}`, {
      method: 'PUT',
      body: JSON.stringify({
        archived: false
      })

    })
    console.log('unarchived');
    load_mailbox('inbox');

  }
}
