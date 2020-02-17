Adding a Custom Domain to a Github Pages Project Site
=====================================================

This is remarkably simple nowadays. The Github Pages documentation is
a little confusing: they only talk about user and organization pages,
and *not* about project pages. There are `numerous posts
<https://stackoverflow.com/questions/9082499/custom-domain-for-github-project-pages>`__
on the internet that suggest that adding a custom domain to a *project
page* has been cumbersome in the past - these days are over,
apparently. Following is what I did.

1. For the ``openheating-pages`` project, configure a custom domain

   (Enforcing HTTPS also makes sense, while we are at it)

   .. image:: custom-domain.png

   All this does is to create a :file:`docs/CNAME`; pull the changes,

   .. code-block:: shell

      $ cd $HOME/openheating-pages
      $ git pull

2. Point ``www.openheating.org`` to ``jfasch.github.io``

   At your DNS provider, create a ``CNAME`` DNS record for
   ``www.openheating.org`` and set its value to point to
   ``jfasch.github.io``. Wait some time (minutes?) for the changes to
   propagate. Check like so,

   .. code-block:: shell

      $ dig www.openheating.org
      
      ; <<>> DiG 9.11.14-RedHat-9.11.14-2.fc31 <<>> www.openheating.org
      ;; global options: +cmd
      ;; Got answer:
      ;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 29463
      ;; flags: qr rd ra; QUERY: 1, ANSWER: 5, AUTHORITY: 0, ADDITIONAL: 0
      
      ;; QUESTION SECTION:
      ;www.openheating.org.		IN	A
      
      ;; ANSWER SECTION:
      www.openheating.org.	3600	IN	CNAME	jfasch.github.io.
      jfasch.github.io.	3600	IN	A	185.199.110.153
      jfasch.github.io.	3600	IN	A	185.199.108.153
      jfasch.github.io.	3600	IN	A	185.199.111.153
      jfasch.github.io.	3600	IN	A	185.199.109.153
      
      ;; Query time: 66 msec
      ;; SERVER: 192.168.1.1#53(192.168.1.1)
      ;; WHEN: Tue Feb 18 00:21:04 CET 2020
      ;; MSG SIZE  rcvd: 131
      
   In the ``ANSWER SECTION`` you can see that ``www.openheating.org.``
   (the trailing dot says this is a FQDN "Fully Qualified Domain
   Name") is an alias (``CNAME``) for ``jfasch.github.io.``. And btw.,
   ``jfasch.github.io.`` has four addresses (``A``).

3. Done; surf to `https://www.openheating.org
   <https://www.openheating.org>`__.
