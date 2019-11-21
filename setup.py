from setuptools import setup, find_packages

setup(
    name='donkey-kong',
    version='0.0.0',
    packages=find_packages(),
    url='https://github.com/maurosilber/donkey-kong',
    license='MIT',
    author='Mauro Silberberg',
    author_email='maurosilber@gmail.com',
    description='A monkey-patching of Luigi.',
    install_requires=['luigi', 'click', 'tabulate'],
    extras_requires=['numpy', 'pandas', 'tifffile'],
    entry_points={'console_scripts': ['donkey-kong = donkey_kong.scripts.main:main']}
)
