document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', () => compose_email([]));

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(defaults) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  const r = document.querySelector('#compose-recipients');
  const s = document.querySelector('#compose-subject');
  const b = document.querySelector('#compose-body');
  if (defaults.length === 0) {
    r.value = '';
    s.value = '';
    b.value = '';
  }
  else {
    r.value = defaults[0];
    s.value = defaults[1];
    b.value = defaults[2];
  }

  const form = document.querySelector('#compose-form');

  form.onsubmit = function() {
    const data = new FormData(form);
    const obj = Object.fromEntries(data.entries());
    const post = {
        recipients: r.value,
        subject: s.value,
        body: b.value
      }
    fetch('/emails', {
      method: 'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify(post)
    })
    .then(response => response.json())
    .then(result => {
      console.log(result)
      load_mailbox('sent')
    });
    return false;
  }
}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(object => object.forEach(e => {

        sender = document.createElement('p');
        subject = document.createElement('p');
        time = document.createElement('p');

        sender.innerText = e.sender;
        subject.innerText = e.subject;
        time.innerText = e.timestamp;

        email = document.createElement('div');
        email.appendChild(sender);
        email.appendChild(subject);
        email.appendChild(time);

        if (e.read) {
          email.className = 'border border-rounded bg-gray p-2 my-4';
        }
        else {
          email.className = 'border border-rounded bg-white p-2 my-4';
        }

        let archivable = false;
        if (mailbox === 'sent'){
          archivable = false;
        }
        else {
          archivable = true;
        }
        email.addEventListener('click', () => getmail(e.id, archivable));

        document.querySelector('#emails-view').appendChild(email);
        document.querySelector('#emails-view').classList.add('py-2');

      }
    )
  );

}

function getmail(id, archivable) {
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(e => {

        Sender = document.createElement('h3');
        Subject = document.createElement('h3');
        Time = document.createElement('h3');
        Content = document.createElement('h3');
        Recipients = document.createElement('h3');

        Sender.innerText = 'Sender:';
        Subject.innerText = 'Subject:';
        Time.innerText = 'Time Sent:';
        Content.innerText = 'Body:';
        Recipients.innerText = 'Recipients:';

        sender = document.createElement('p');
        subject = document.createElement('p');
        time = document.createElement('p');
        content = document.createElement('p');
        recipients = document.createElement('p');

        sender.innerText = e.sender;
        subject.innerText = e.subject;
        time.innerText = e.timestamp;
        content.innerText = e.body;
        recipients.innerText = e.recipients;

        composition = [Sender, sender, Recipients, recipients, Subject, subject, Time, time, Content, content];

        let flag = true;
        email = document.createElement('div');
        composition.forEach(part => {
          email.appendChild(part);
          if (flag){
            part.className = 'font-weight-bold';
            flag = false;
          }
          else{
            flag = true;
          }
        });

        if (archivable) {
          let text = '';
          if (e.archived){
            text = 'UnArchive';
          }
          else {
            text = 'Archive';
          }
          archive = document.createElement('button');
          archive.className = 'btn btn-primary rounded';
          archive.innerText = text;
          archive.addEventListener('click', () => {
            fetch(`emails/${id}`, {
              method: 'PUT',
              headers: {'Content-Type':'application/json'},
              body: JSON.stringify({
                archived: !e.archived
              })
            });
            load_mailbox('inbox');
          });
          email.appendChild(archive);

          let line = '';
          if (e.subject.startsWith('Re:')){
            line = e.subject;
          }
          else {
            line = `Re: ${e.subject}`;
          }
          reply = document.createElement('button');
          reply.innerText = 'Reply';
          reply.className = 'btn btn-secondary m-1 p-2';
          reply.addEventListener('click', () => compose_email([e.sender, line, `On ${e.timestamp} ${e.sender} wrote:\n${e.body}`]));
          email.appendChild(reply);
        }

        if (e.read) {
          email.className = 'border border-rounded bg-white p-2 my-4';
        }
        else {
          email.className = 'border border-rounded bg-light p-2 my-4';
        }

        document.querySelector('#emails-view').innerHTML = '';
        document.querySelector('#emails-view').appendChild(email);
        document.querySelector('#emails-view').classList.add('py-2');

    }
  );
  fetch(`emails/${id}`, {
    method: 'PUT',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify({
        read: true
      })
    });
}