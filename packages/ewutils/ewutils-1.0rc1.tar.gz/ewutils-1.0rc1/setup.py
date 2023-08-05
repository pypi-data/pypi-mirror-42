import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='ewutils',
    version='1.0rc1',
    description='A collection of tools and utilities that I put together to make programming a little easier',
    url='https://github.com/Ewpratten/ewutils',
    author='Evan Pratten',
    author_email='ewpratten@gmail.com',
    license='GPLv3',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=['requests'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable"
    ],
)