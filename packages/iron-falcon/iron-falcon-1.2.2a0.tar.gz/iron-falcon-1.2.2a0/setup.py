from setuptools import setup, find_packages
try:
    from pip.req import parse_requirements
except ModuleNotFoundError as e:
    # pip 10 compatibility
    from pip._internal.req import parse_requirements

import glob
import os


program_name = 'iron-falcon'

install_reqs = parse_requirements('requirements.txt', session='iron_falcon')
reqs = [str(ir.req) for ir in install_reqs]


setup(
    name=program_name,

    version='1.2.2a0',

    description='',
    long_description='Embrace the power of marshmallow with falcon speed.',

    url='https://gitlab.guvenfuture.com/cagri.ulas/iron-falcon',

    author='',
    author_email='',

    maintainer='Çağrı ULAŞ',
    maintainer_email='cagriulas@gmail.com',

    license='LGPLv3+',

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',

        'Natural Language :: English',

        'Operating System :: POSIX :: Linux',

        'Intended Audience :: Developers',

        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',

        'Programming Language :: Python :: 3.6',
    ],

    keywords='falcon',

    install_requires=reqs,

    packages=find_packages(),

)
