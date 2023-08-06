from setuptools import setup, find_packages


with open('README.md') as fh:
    long_description = fh.read()


setup(
    name='avilabs-plotter',
    version='0.3.3',
    description='Python plotting APIs',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Avilay Parekh',
    author_email='avilay@gmail.com',
    license='MIT',
    url='https://bitbucket.org/avilay/plotter',
    packages=find_packages(),
    install_requires=['matplotlib', 'numpy'],
)
