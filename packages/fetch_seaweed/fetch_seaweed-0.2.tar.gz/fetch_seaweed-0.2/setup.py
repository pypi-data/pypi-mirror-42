from setuptools import setup

setup(
        name='fetch_seaweed',
        version='0.2',
        scripts=['fetch_seaweed.py'],
        install_requires=[
            'opencv-python',
            'numpy',
            'requests'
            ]
    )
