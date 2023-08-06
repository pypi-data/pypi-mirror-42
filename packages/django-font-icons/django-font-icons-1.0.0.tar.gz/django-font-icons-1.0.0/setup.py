import os

from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-font-icons',
    version='1.0.0',
    packages=['font_icons'],
    include_package_data=True,
    install_requires=[
        'django>1.11',
        'django-choices'
    ],
    license='BSD License',
    description='A utility for using icons in models and forms.',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/JostCrow/django-font-icons',
    author='Jorik Kraaikamp',
    author_email='jorikkraaikamp@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Utilities',
    ],
)
