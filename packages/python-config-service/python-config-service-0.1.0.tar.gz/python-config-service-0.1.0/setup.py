import setuptools
setuptools.setup(
    name="python-config-service",
    version="0.1.0",
    url="https://gitlab.host-h.net/DanieCilliers/python-config-service",
    author="Danie Cilliers",
    author_email="email@gmail.com",
    description="Python package to communicate with the config service",
    long_description=open('README.md').read(),
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
)