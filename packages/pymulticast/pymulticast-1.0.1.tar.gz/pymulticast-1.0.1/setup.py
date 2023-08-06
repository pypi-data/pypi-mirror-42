"""
send or receive multicast udp
"""
import sys
from setuptools import setup

setup(
    name='pymulticast',
    version='1.0.1',
    url='https://github.com/wangpeng2020/multicast.git',
    license='MIT',
    author='Peng Wang',
    author_email='wp2ypy@gmail.com',
    description=__doc__.strip('\n'),
    #packages=[],
    scripts=['bin/pymulticast'],
    #include_package_data=True,
    zip_safe=False,
    platforms='Linux',
    install_requires=['docopt', 'pip>=1.5.0'],
    classifiers=[
        # As from https://pypi.python.org/pypi?%3Aaction=list_classifiers
        #'Development Status :: 1 - Planning',
        #'Development Status :: 2 - Pre-Alpha',
        #'Development Status :: 3 - Alpha',
        'Development Status :: 4 - Beta',
        #'Development Status :: 5 - Production/Stable',
        #'Development Status :: 6 - Mature',
        #'Development Status :: 7 - Inactive',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Topic :: System :: Networking',
    ]
)
