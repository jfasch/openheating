Github Pages as Hosting Platform
================================

Github Pages is a website hosting feature provided by Github. It can
be used by users, organizations and projects (like this one) to deploy
and serve websites.

By default (this is a big part of the feature) you have a repository
containing `markdown
<https://daringfireball.net/projects/markdown/>`__ source; it is that
source that is built by the Github Pages machinery, using the `Jekyll
<https://jekyllrb.com/>`__ static site generator, to form the
website. The OpenHeating project uses Sphinx, so Jekyll does not make
any sense. Nevertheless we want to host the generated
content. :doc:`Read here <sphinx-gh-pages>` for how this is done.

Another feature is you can assign a `"Custom domain"
<https://help.github.com/en/github/working-with-github-pages/about-custom-domains-and-github-pages>`__
to a website you serve through Github Pages. OpenHeating's domain is
``openheating.org``; :doc:`read here <custom-domain-gh-pages>` how we
point ``www.openheating.org`` at our Github-served website.

.. toctree::

   sphinx-gh-pages
   custom-domain-gh-pages
