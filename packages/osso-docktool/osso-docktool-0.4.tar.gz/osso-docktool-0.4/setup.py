# osso-docktool -- HDD administration and maintenance
# Copyright (C) 2015-2019 OSSO B.V.
from distutils.core import setup
from os.path import dirname, join


if __name__ == '__main__':
    long_descriptions = []
    with open(join(dirname(__file__), 'README.rst')) as file:
        long_descriptions.append(file.read())
    version = '0.4'

    setup(
        name='osso-docktool',
        version=version,
        data_files=[('share/doc/osso-docktool', [
            'README.rst', 'local_settings.py.template'])],
        entry_points={'console_scripts': [
            'osso-docktool = osso_docktool.docktool:main']},
        packages=['osso_docktool'],
        description='HDD administration and maintenance',
        long_description=('\n\n\n'.join(long_descriptions)),
        author='OSSO B.V.',
        author_email='dev+osso-docktool@osso.nl',
        url='https://git.osso.nl/osso-io/docktool',  # osso-int[ernal]?
        license='Undecided',
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'Intended Audience :: End Users/Desktop',
            'Intended Audience :: System Administrators',
            # ('License :: OSI Approved :: GNU General Public License v3 '
            #  'or later (GPLv3+)'),
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Topic :: System :: Filesystems',
            'Topic :: Utilities',
        ],
        install_requires=[
            'requests',
        ],
    )

# vim: set ts=8 sw=4 sts=4 et ai tw=79:
