from setuptools import setup, find_packages
from stackedit import __VERSION__, __AUTHOR__, __AUTHOR_EMAIL__
import os, sys


def get_requirements():
    return open('requirements.txt').read().splitlines()


if sys.argv[-1] == 'build':
    os.system('rm -rf build dist *.egg-info')
    os.system('python setup.py sdist bdist_wheel')
    sys.exit()

if sys.argv[-1] == 'clear':
    os.system('rm -rf build dist *.egg-info django.log')
    sys.exit()

if sys.argv[-1] == 'publish':
    os.system('rm -rf build dist *.egg-info django.log')
    os.system('python setup.py sdist bdist_wheel')
    os.system('twine upload dist/*')
    sys.exit()

if sys.argv[-1] == 'tag':
    os.system(f"git tag -a {__VERSION__} -m 'version {__VERSION__}'")
    os.system("git push --tags")
    sys.exit()

setup(
    name='django-stackedit',
    version=__VERSION__,
    packages=find_packages(exclude=["*demo"]),
    include_package_data=True,
    zip_safe=False,
    description='Django Stackedit Markdown Editor',
    url='https://gitee.com/qtch/django-stackedit',
    # download_url='https://github.com/agusmakmun/django-markdown-editor/tarball/v%s' % __VERSION__,
    keywords=['stackedit', 'django markdown', 'django markdown editor'],
    long_description=open('README.rst').read(),
    license='GNUGPL-v3',
    author=__AUTHOR__,
    author_email=__AUTHOR_EMAIL__,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: JavaScript',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
    install_requires=get_requirements(),
)
