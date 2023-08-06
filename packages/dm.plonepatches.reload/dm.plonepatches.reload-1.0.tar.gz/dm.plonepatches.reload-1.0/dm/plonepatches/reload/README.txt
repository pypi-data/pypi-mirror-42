This package provides patches to improve ``plone.reload``.

Calling its ``patch_top_level_reload`` applies a patch
for (`#10 <https://github.com/plone/plone.reload/issues/10>`_)
making it possible to reload top level modules in place.

Calling its ``patch_handle_super_and_methods`` applies a patch
for (`#1 <https://github.com/plone/plone.reload/issues/1>`_)
and (`#11 <https://github.com/plone/plone.reload/issues/11>`_)
improving the reload on methods involving ``super`` and classmethods
(in Python 3).
