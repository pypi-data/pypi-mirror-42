from setuptools import setup

setup(
    name='SAW',
    version='0.1.1',
    packages=['SAW', 'scripts'],
    license='MIT License',
    description='SAW, a Python SimFin API Wrapper',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Vilhelm Melkstam',
    author_email='vilhelm.melkstam@gmail.com',
    entry_points='''
        [console_scripts]
        saw=scripts.saw:main
    ''',
    install_requires=['peewee', 'requests'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Topic :: Documentation :: Sphinx',
        'Topic :: Office/Business :: Financial',
        'Topic :: Office/Business :: Financial :: Investment',
        'Topic :: Utilities'
    ],
)