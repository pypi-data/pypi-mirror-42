#!/usr/bin/env python

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'scenery',
        version = '1.0.0',
        description = 'A pattern-based scene release renamer',
        long_description = 'A command-line tool that automates renaming of so-called "Scene Release"\nfiles by fetching episode names (from TVMaze) and which uses pattern-based generic building\nblocks (show name, season number, episode number, episode title) to format the output.\n',
        author = 'Dachaz',
        author_email = 'dachaz@dachaz.net',
        license = 'MIT',
        url = 'https://github.com/dachaz/scenery',
        scripts = [],
        packages = [
            'scenery',
            'scenery.model'
        ],
        namespace_packages = [],
        py_modules = [],
        classifiers = [
            'Programming Language :: Python',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Intended Audience :: End Users/Desktop',
            'License :: OSI Approved :: MIT License',
            'Topic :: Communications :: File Sharing',
            'Topic :: Multimedia',
            'Topic :: Multimedia :: Video',
            'Topic :: Utilities'
        ],
        entry_points = {
            'console_scripts': ['scenery = scenery:main']
        },
        data_files = [],
        package_data = {},
        install_requires = [],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        keywords = '',
        python_requires = '',
        obsoletes = [],
    )
