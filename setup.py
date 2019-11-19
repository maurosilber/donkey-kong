from setuptools import setup

setup(
    name='donkey-kong',
    version='0.0.0',
    packages=['donkey_kong'],
    url='https://github.com/maurosilber/sciluigi',
    license='MIT',
    author='Mauro Silberberg',
    author_email='maurosilber@gmail.com',
    description='A monkey-patching of Luigi.',
    install_requires=['luigi', 'click'],
    extras_requires=['numpy', 'pandas', 'tifffile'],
    entry_points={'console_scripts': ['donkey-kong = donkey_kong.scripts.main:main']}
)
