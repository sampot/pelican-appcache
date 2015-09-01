HTML5 application cache manifest generator for Pelican
=========================================================

This plugin generates a manifest file for use in HTML application cache. All published pages and articles are included,
as well as index pages. Other resources can be manually specified in ``APPCACHE_RESOURCES`` setting.

Settings
~~~~~~~~~~

* ``APPCACHE_MANIGEST_NAME``:  the name of manifest file, default is 'manifest.appcache'.

* ``APPCACHE_RESOURCES``: a list of resource files manually added to the manifest file.

Following settings are used by this plugin to determine URLs and number of index pages:
* ``SITEURL``: the site's base URL
* ``DEFAULT_PAGINATION``: default is 8 entries per page.
* ``DEFAULT_ORPHANS``: the minimum number of entries to be in its own index page.

Assumptions
~~~~~~~~~~~~

# Individual index file per page is assumed

.. code-block:: python

    PAGINATION_PATTERNS = (
        (1, '{base_name}/', '{base_name}/index.html'),
        (2, '{base_name}/page/{number}/', '{base_name}/page/{number}/index.html'),
    )

