from setuptools import setup



setup(
    name = 'ganesh',
    version = 1.0,
    description = 'trying to upload it to pypi',
    author='ganesh',
    author_email='ganesh@server.com',
    url="http://www.foopackage.com/",
    packages=['ganesh'],
    install_requires=['flask', 'flask-restful'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

)
