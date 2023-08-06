"""Module to be reloaded."""

from reload_count import get_count

count = get_count()

class B(object):
  def f(self): return count

class S(B):
  """`super` testing."""
  def f(self): return super(S, self).f()

class CM(B):
  """`classmethod` testing."""
  @classmethod
  def f(self): return count

class SCM(CM):
  """`classmethod` with `super`."""
  @classmethod
  def f(self): return super(SCM, self).f()

class SM(B):
  """`staticmethod` testing."""
  @staticmethod
  def f(): return count


# we need a more sophisticated closure handling to
#  support general decorators
##class D(B):
##  """decorator testing."""
##  def add_param(f):
##    def wrapped(self, *args, **kw): return f(self, 1, *args, **kw)
##    return wrapped

##  @add_param
##  def f(self, i): return count
