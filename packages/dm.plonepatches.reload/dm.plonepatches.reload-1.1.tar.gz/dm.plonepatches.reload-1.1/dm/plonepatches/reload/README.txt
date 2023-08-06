This package provides patches to improve ``plone.reload``.

Calling its ``patch_top_level_reload`` applies a patch
for (`#10 <https://github.com/plone/plone.reload/issues/10>`_)
making it possible to reload top level modules in place.

Calling its ``patch_handle_super_and_decorators`` applies a patch
for (`#1 <https://github.com/plone/plone.reload/issues/1>`_)
and (`#11 <https://github.com/plone/plone.reload/issues/11>`_)
improving the reload on methods involving ``super`` and classmethods
(in Python 3). In addition, it
improves the reload of simple decoratored functions/methods.

**BE WARNED**: even with all patches applied, ``plone.reload``
is not yet perfect. For example, it still cannot change reliably
function default values for parameters.
Should you observe surprising behaviour after
you made a reload, restart and see whether the behaviour changes.


History
=======

1.1
  new ``patch_handle_super_and_decorators``

  ``patch_handle_super_and_methods`` is now an alias for
  ``patch_handle_super_and_decorators``

1.0
  initial version
