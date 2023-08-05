An easier way to send an Email.

Features
========

TODO

Create an Email object and send
===============================

.. code-block:: python

  from cheesefactory-Email import Email

  email = Email(
      recipients=['bob@example.com',],
      host='localhost',
      port='25',
      username='emailuser',
      password='emailpassword',
      sender='tom@example.com',
      subject='Fishing trip',
      body='Dear Bob,\nHow was the fishing trip?\n\nTom',
      use_tls=False,
      attachments=['file1.txt', 'file2.txt']
  )
