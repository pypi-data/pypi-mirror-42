from distutils.core import setup

with open("README.md", "r") as readme:
    long_description = readme.read()

setup(
    author='Zachary J. McCord',
    author_email='zjmccord@gmail.com',
    classifiers=["Programming Language :: Python :: 3",
                 "Programming Language :: Python :: 2",
                 "Topic :: Software Development :: Debuggers",
                 "Topic :: Software Development :: Testing",
                 "License :: OSI Approved :: Apache Software License",
                 "Operating System :: OS Independent"],
    description='A unittest shim to make PDB debugging of test cases easy.',
    keywords=['testing', 'pdb', 'unittest'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    name='pdbtest',
    packages=['pdbtest'],
    url='https://github.com/zack112358/pdbtest/',
    version='1.4',
)
