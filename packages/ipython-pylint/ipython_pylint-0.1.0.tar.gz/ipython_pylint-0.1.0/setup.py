#!/usr/bin/env python3

from setuptools import setup


SETUP_KWARGS = dict(
    name='ipython_pylint',
    version='0.1.0',
    packages=('ipython_pylint',),
    url='https://github.com/HoverHell/ipython_pylint',
    license='MIT',
    author='HoverHell',
    author_email='hoverhell@gmail.com',
    install_requires=[
        'pylint',
        'IPython',
    ],
    tests_require=[],
    description=(
        'pylint-invoker ipython magic command'),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        # 'Development Status :: 2 - Pre-Alpha',
        'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
    ])


if __name__ == '__main__':
    setup(**SETUP_KWARGS)
