from setuptools import setup

setup(
        name='fetch_seaweed',
        version='0.1',
        scripts=['fetch_seaweed.py'],
        install_requires=[
            'opencv-python',
            'numpy',
            'requests'
            ]
    )
