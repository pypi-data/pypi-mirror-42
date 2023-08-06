from __future__ import absolute_import

from sys import path
from os.path import dirname
from unittest import TestCase

from .. import func

class Layer(object):
  @classmethod
  def setUp(cls):
    # manipulate `sys.path` to be able to make a top level import of `reload_module`
    path.insert(0, dirname(__file__))
    import reload_module
    B = reload_module.B
    cls.oclss = oclss = [
      C for C in
      (getattr(reload_module, n) for n in dir(reload_module) if not n.startswith("_"))
      if isinstance(C, type) and issubclass(C, B)
      ] + [B]
    cls.objs = objs = [C() for C in oclss]
    cls.ofs = ofs = [func(o.f) for o in objs]
    from .. import patch_top_level_reload, patch_handle_super_and_methods
    patch_top_level_reload()
    patch_handle_super_and_methods()
    from plone.reload.xreload import Reloader
    Reloader(reload_module).reload()
    cls.nclss = [getattr(reload_module, C.__name__) for C in oclss]

  @classmethod
  def tearDown(cls):
    raise NotImplementedError

class TestReload(TestCase):
  layer = Layer

  def test_classes_inplace(self):
    layer = self.layer
    self.assertEqual(layer.oclss, layer.nclss)

  def test_fs_inplace(self):
    layer = self.layer
    self.assertEqual(layer.ofs, [func(o.f) for o in layer.objs])

  def test_fs_call(self):
    for o in self.layer.objs:
      self.assertEqual(o.f(), 1, o.__class__.__name__)
