from setuptools import setup, find_packages

setup(
    name='avilabs-plotter',
    version='0.3.0',
    description='Python plotting APIs',
    author='Avilay Parekh',
    author_email='avilay@avilaylabs.net',
    license='MIT',
    url='https://bitbucket.org/avilay/plotter',
    packages=find_packages(),
    install_requires=['matplotlib', 'numpy'],
)
