"""Fixes and enhancements for `plone.reload`."""
from logging import getLogger
from os.path import exists
from sys import version_info

import six

from dm.reuse import rebindFunction

from plone.reload import xreload

logger = getLogger(__name__)

# auxiliary
def func(f): return getattr(f, "__func__", f)

# patch `xreload.Reloader.reload` (to get top level modules properly handled)
def patch_top_level_reload():
  ori_reload = func(xreload.Reloader.reload)
  if version_info.major >= 3:
    def fixing_exec(code, ns):
      if ns["__name__"].startswith("None."):
        ns["__name__"] = ns["__name__"][5:]
      exec(code, ns)
    reload = rebindFunction(ori_reload, {"exec":fixing_exec})
  else:
    # Python 2: there `exec` is a keyword and we cannot fix as above
    #  we therefore fetch the code, fix it, compile it and
    #  use the fixed definition
    fn = xreload.__file__
    if fn.endswith(".pyc"): fn = fn[:-1]
    if not exists(fn):
      raise ValueError("`plone.reload.xreload` must be available as source")
    source = open(fn).read()
    bad = "tmpns = {'__name__': '%s.%s' % (pkgname, modname),"
    if bad not in source: reload = None
    else:
      source = source.replace(bad, "tmpns = {'__name__': self.mod.__name__,")
      code = compile(source, fn, "exec")
      ns = dict((n, getattr(xreload, n)) for n in ("__name__", "__file__", "__doc__"))
      exec (code, ns)
      reload = func(ns["Reloader"].reload)

  if reload is not None:
    xreload.Reloader.reload = reload
    logger.info("Patched `plone.reload.xreload.Reloader.reload` for proper top level module reloading")


# patch "super" and (class) method handling
#  In Python 3, methods referencing `super` (or `__class__`) have
#  an implicit closure cell for `__class__`.
#  `xreload._closure_changed` does not handle this case and
#  as a consequence, the reloaded methods typically fail.
#  We replace the `_update_function` function by one
#  performing a more intelligent closure check by ignoring
#  closure cells corresponding to `__class__`.
#  Note: an extension of this approach could also allow some
#   decorated functions to be updated in place - but this
#   is likely of lesser importance (and not yet done below)
def patch_handle_super_and_methods():
  if version_info.major <= 2: _update_function = None
  else:
    # Python 3
    ori_update_function = xreload._update_function
    def _closure_changed(old, new):
      ocl = old.__closure__; ncl = new.__closure__
      if ocl is None and ncl is None: return False
      if ocl is None or ncl is None or len(ocl) != len(ncl): return True
      ofvs = old.__code__.co_freevars; nfvs = new.__code__.co_freevars
      if ofvs != nfvs or len(ofvs) != len(ocl):
        # an update in place might still be possible
        # but the situation is too complex for us
        return True
      for fv, oc, nc in zip(ofvs, ocl, ncl):
        if fv == "__class__":
          # we assume that the class is updated in place as well
          #   Note: This is a heuristic. It is possible that
          #     the `__class__` refers to a different class than
          #     the one updated in place (and then we do something wrong)
          continue
        elif oc != nc: return True
      else: return False

    _update_function_without_closure_check = rebindFunction(
      ori_update_function,
      _closure_changed=lambda o, n: False
      )
    def _update_function(old, new):
      update = ori_update_function if _closure_changed(old, new) \
               else _update_function_without_closure_check
      return update(old, new)

    # patch (class) method handling
    #   see "https://github.com/plone/plone.reload/issues/11"
    _update_method = rebindFunction(
      func(xreload._update_method),
      six=SixMockup(get_unbound_function=func),
      _update_function=_update_function, # must rebind explicitely
      )

  if _update_function is not None:
    xreload._update_function = _update_function
    xreload._update_method = _update_method
    logger.info("Patched `_update_function` and `_update_method` in `plone.reload.xreload` for improved `super' and classmethod handling")


class SixMockup(object):
  """`six` with patches."""
  def __init__(self, **overrides):
    self.overrides = overrides

  def __getattr__(self, k):
    v = self.overrides.get(k, self)
    return v if v is not self else getattr(six, v)
