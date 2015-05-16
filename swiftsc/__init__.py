"""swiftsc is OpenStack Swift simple client.

Initialize.
-----------

Swift tempauth
~~~~~~~~~~~~~~

Using Swift tempauth.
::

    $ python
    >>> from swiftsc import Client
    >>> client = Client(auth_uri='https://swift.example.org/auth/v1.0',
    ... username='myaccount', password='passw0rd')

KeyStone Auth
~~~~~~~~~~~~~

Using KeyStone. Not yet support Identitty API v3.
::

    $ python
    >>> from swiftsc import Client
    >>> client = Client(auth_uri='https://keystone.example.org/v2.0/tokens',
    ... username='myaccount', password='passw0rd', tenant_name='mytennant')


Create container
----------------
::

    >>> client.containers.create(name='mycontainer')
    <Response [201]>
    >>> client.containers.list().json()
    [{'bytes': 1403088360, 'count': 5, 'name': 'container-a'},
     {'bytes': 393429510, 'count': 11, 'name': 'container-b'},
     {'bytes': 410389320, 'count': 11, 'name': 'container-c'},
     ...
     {'bytes': 9690876040, 'count': 57, 'name': 'container-x'},
     {'bytes': 0, 'count': 0, 'name': 'mycontainer'}]
    >>> client.containers.detail('mycontainer')
    <Response [204]>

Create object
-------------
::

    >>> client.containers.container('mycontainer')
    >>> with open('/tmp/dummy.txt', 'w') as f:
    ...    f.write('sample')
    >>> client.containers.objects.create(name='dummy',
    ... file_path='/tmp/dummy.txt')
    <Response [201]>
    >>> client.containers.objects.list().json()
    [{'bytes': 5,
      'content_type': 'text/plain',
      'hash': '275876e34cf609db118f3d84b799a790',
      'last_modified': '2015-03-18T09:32:40.311040',
      'name': 'dummy'}]
    >>> client.containers.detail('mycontainer')
    <Response [200]>
    >>> client.containers.detail('mycontainer').text.split()
    ['dummy']
    >>> client.containers.detail('dummy').text
    'sample'
    >>> client.containers.objects.copy('dummy', 'dummy2')
    <Response [201]>
    >>> client.containers.objects.delete('dummy')
    <Response [204]>
    >>> client.containers.objects.list().json()
    [{u'bytes': 6,
      u'content_type': u'text/plain',
      u'hash': u'5e8ff9bf55ba3508199d22e984129be6',
      u'last_modified': u'2015-03-18T09:39:36.247430',
      u'name': u'dummy2'}]

"""
from swiftsc.client import Client  # silence pyflakes
