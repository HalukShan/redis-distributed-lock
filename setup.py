from setuptools import setup
from os import path as os_path

this_directory = os_path.abspath(os_path.dirname(__file__))


def read_file(filename):
    with open(os_path.join(this_directory, filename), encoding='utf-8') as f:
        long_description = f.read()
    return long_description


setup(
  name='redis_distributed_lock',
  version="1.3",
  description="Redis distributed lock for python",
  long_description=read_file('README.md'),
  long_description_content_type="text/markdown",
  license="MIT",
  keywords='redis distributed lock',
  author='halukshan',
  author_email='halukshan@gmail.com',
  url='https://github.com/halukshan/redis-distributed-lock',
  classifiers=['Development Status :: 4 - Beta',
               'Intended Audience :: Developers',
               'Natural Language :: English',
               'Operating System :: POSIX :: Linux',
               'Programming Language :: Python :: 3.7'
  ],
  packages=['redis_distributed_lock'],
)