from setuptools import setup

setup(
    name='nanolife',
    version='1.0.0',
    description='Conway\'s Game of Life implemented with PyGame.',
    url='https://github.com/DevDungeon/PyGameOfLife',
    author='DevDungeon',
    author_email='nanodano@devdungeon.com',
    license='GPL-3.0',
    packages=['nanolife'],
    scripts=[
        'bin/nanolife',
        'bin/nanolife.bat',
    ],
    zip_safe=False,
    install_requires=[
        'pygame'
    ]
)