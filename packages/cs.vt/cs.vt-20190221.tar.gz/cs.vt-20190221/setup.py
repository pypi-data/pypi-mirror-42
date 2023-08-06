#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.vt',
  description = 'A content hash based data store with a filesystem layer, using variable sized blocks, arbitrarily sized data and utilising some domain knowledge to aid efficient block boundary selection.',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20190221',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Development Status :: 3 - Alpha', 'Environment :: Console', 'Programming Language :: Python :: 3', 'Topic :: System :: Filesystems', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
  entry_points = {'console_scripts': ['vt = cs.vt.__main__:main', 'mount.vtfs = cs.vt.__main__:mount_vtfs']},
  install_requires = ['cs.buffer', 'cs.app.flag', 'cs.binary', 'cs.cache', 'cs.debug', 'cs.deco', 'cs.excutils', 'cs.fileutils', 'cs.inttypes', 'cs.later', 'cs.lex', 'cs.logutils', 'cs.mappings', 'cs.packetstream', 'cs.pfx', 'cs.progress', 'cs.py.func', 'cs.py.stack', 'cs.queues', 'cs.range', 'cs.resources', 'cs.result', 'cs.seq', 'cs.serialise', 'cs.socketutils', 'cs.threads', 'cs.tty', 'cs.units', 'cs.x', 'icontract', 'lmdb'],
  keywords = ['python3'],
  long_description = 'A content hash based data store with a filesystem layer, using\nvariable sized blocks, arbitrarily sized data and utilising some\ndomain knowledge to aid efficient block boundary selection.\n\n*NOTE*: pre-Alpha; alpha release following soon once the packaging\nis complete.\n\nThe package provides the `vt` command to access\nthese facilities from the command line.\n\nThis system has two main components:\n* Stores: storage areas of variable sized data blocks\n  indexed by the cryptographic hashcode of their content\n* Dirents: references to filesystem entities\n  containing hashcode based references to the content\n\nThese are logically disconnected.\nDirents are not associated with particular Stores;\nit is it sufficient to have access to any Store\ncontaining the required blocks.\n\nThe other common entity is the Archive,\nwhich is just a text file containing\na timestamped log of revisions of a Dirent.\nThese can be mounted as a FUSE filesystem,\nand the `vt pack` command simply stores\na directory tree into the current Store,\nand records the stored reference in an Archive file.\n\nSee also the Plan 9 Venti system:\n(http://library.pantek.com/general/plan9.documents/venti/venti.html,\nhttp://en.wikipedia.org/wiki/Venti)\nwhich is also based on variable sized blocks.\n\n## Function `totext(data)`\n\nRepresent a byte sequence as a hex/text string.',
  long_description_content_type = 'text/markdown',
  package_dir = {'': 'lib/python'},
  packages = ['cs.vt'],
)
