from setuptools import setup, find_packages

setup(
    name='steamwrapper',
    version='0.1262',
    description='API wrapper for Steam written in Python',
    long_description=open('README.txt', 'r').read(),
    author='truedl',
    author_email='dauzduz1@gmail.com',
    url='https://github.com/truedl/steamwrapper',
    packages=find_packages(),
    license='MIT',
    install_requires=['requests', 'aiohttp'],
)