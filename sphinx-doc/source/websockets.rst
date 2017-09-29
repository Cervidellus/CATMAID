.. _websockets:

WebSockets and ASGI
===================

WebSockets allows CATMAID instances to push data to the client even if the
client didn't request it. This can be useful to inform the client about updates
on the server. An example is the notification about new messages, created e.g.
by cropping a sub-volume out of the image data.

Without WebSockets, the CATMAID web front-end will ask the server for updates
every minute. Avoiding these requests especially with many clients lowers the
resource requirements of CATMAID. ASGI is the protocol used for this
bi-directional communication and a separate ASGI server (the asynchronous
sibling of WSGI). A common choice for this server is
`Daphne <https://github.com/django/daphne>`_. It is used below for an example
setup.

Note that ``manage.py runserver`` supports ASGI out of the box. This however is
not meant to be used for production setups.


Setting up an ASGI server
-------------------------

Daphne is already installed as part of CATMAID's dependencies. To run it use the
following command::

    daphne -b 127.0.0.1 -p 8001 mysite.asgi:channel_layer

This will start a new Daphne server, listening on port ``8001`` on the localhost
network interface. Additionally, workers are required to process requests. This
can be done with::

    manage.py runworker

A rule of thumb is to have as many workers as there are processors available.

Route ASGI requests to ASGI server
----------------------------------

To make the ASGI server available to the client, the public facing webserver has
to know about it. Of course it would be possible to replace existing *WSGI*
setups altogether and use only Daphne for both ASGI and WSGI. There are many
situations where this is impractical and could cause problems. Therefore we
recommend to only route ASGI requests to the ASGI server and let everything else
be handled by the regular WSGI server.

To make this easier, CATMAID makes all ASGI endpoints available under::

    <CATMAID-URL>/channels/

With this we can tell Nginx (or similar in other webservers) to route all URLs
starting with ``/channels/`` to the ASGI server. This is accomplished by the
following ``location`` block:

.. code-block:: nginx

    location /channels/ {
        proxy_pass http://127.0.0.1:8001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        proxy_redirect     off;
        proxy_set_header   Host $host;
        proxy_set_header   X-Real-IP $remote_addr;
        proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Host $server_name;
    }

Be sure to use your sub-directory structure as a prefix, if you use any. Also,
if you see errors like "``(104: Connection reset by peer) while reading response
header from upstream``" make sure to increase the available file handles on the
OS level by setting::

    sysctl -w fs.file-max=65536

Make sure to persist this in ``/etc/sysctl.conf``. Additionally, allow Nginx
more fie handles by setting this on the most outer level in
``/etc/nginx.conf``::

    worker_rlimit_nofile 10000;

Process management with Supervisord
-----------------------------------

Supervisord is used as an example for a process management configuration in
other parts of this documentation and so we use it here to show how the above
ASGI configuration can be managed alongside the existing Supervisord
configuration. This assumes a Supervisor process group named "catmaid" is
defined in the following file::

    /etc/supervisord/conf.d/catmaid.conf

Add the following lines to this file, between the last ``[program:<name>]``
section and the ``[group:catmaid]`` section:

.. code-block:: ini

    [program:catmaid-daphe]
    directory = /opt/catmaid/django/projects/
    command = /opt/catmaid/django/env/bin/daphne -b 127.0.0.1 -p 8001 mysite.asgi:channel_layer
    user = www-data
    stdout_logfile = /opt/catmaid/django/projects/mysite/daphne.log
    redirect_stderr = true

    [program:catmaid-daphe-worker]
    directory = /opt/catmaid/django/projects/
    command = /opt/catmaid/django/env/bin/python manage.py runworker
    user = www-data
    stdout_logfile = /opt/catmaid/django/projects/mysite/daphne-worker.log
    redirect_stderr = true
    autorestart = true
    process_name = "Daphne worker %(process_num)s"
    numprocs = <NUM-CPUS>

Replace ``<NUM-CPUS>`` in the last line with the number of CPUs on your system.
It should however be fine to use a lower number in most cases and probably even
1 will most of the time not cause problems.
