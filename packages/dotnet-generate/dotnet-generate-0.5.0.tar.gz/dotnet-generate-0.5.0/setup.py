from setuptools import setup

with open("README.md") as readme:
    long_description = readme.read()

setup(
    name='dotnet-generate',
    version='0.5.0',
    author="Kristjan Tärk",
    author_email="kristjan.tark@eesti.ee",
    description="Tool for generating dotnet code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/eskumu/dotnet-generate",
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        'Environment :: Console',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    py_modules=['dotnet_generate'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        dotnet-generate=dotnet_generate:cli
    ''',
)
