# -*- coding: utf-8 -*-

from setuptools import setup

setup(
        name='dperf',
        version='0.0.1',
        author='lychee',
        author_email='lycheenice@gmail.com',
        url='https://cn.linkedin.com/in/lycheenice',
        description='Deep Learning System Performance Profiler',
        packages=['dperf'],
        install_requires=[],
        entry_points={
            'console_scripts':['dperf=dperf:dperf']
            }

        )
