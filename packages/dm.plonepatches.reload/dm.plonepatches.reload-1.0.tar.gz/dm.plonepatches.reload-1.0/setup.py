from os.path import abspath, dirname, join
try:
  # try to use setuptools
  from setuptools import setup
  setupArgs = dict(
      include_package_data=True,
      namespace_packages=['dm', 'dm.plonepatches'],
      install_requires=["plone.reload", "dm.reuse>=2.1.1"],
      zip_safe=False,
      )
except ImportError:
  # use distutils
  from distutils import setup
  setupArgs = dict(
    )

cd = abspath(dirname(__file__))
pd = join(cd, 'dm', 'plonepatches', 'reload')

def pread(filename, base=pd): return open(join(base, filename)).read().rstrip()

setup(name='dm.plonepatches.reload',
      version=pread('VERSION.txt').split('\n')[0],
      description='Patch for "plone.reload": handle "super" and top level module reloads properly.',
      long_description=pread('README.txt'),
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Framework :: Plone',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
        ],
      author='Dieter Maurer',
      author_email='dieter@handshake.de',
      url='http://pypi.python.org/pypi/dm.plonepatches.reload',
      packages=['dm', 'dm.plonepatches', 'dm.plonepatches.reload'],
      keywords='reload development',
      license='GPL',
      **setupArgs
      )
