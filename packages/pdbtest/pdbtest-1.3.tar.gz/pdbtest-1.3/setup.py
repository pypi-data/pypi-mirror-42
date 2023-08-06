from distutils.core import setup
setup(
    name='pdbtest',
    packages=['pdbtest'],
    version='1.3',
    description='A unittest shim to make PDB debugging of test cases easy.',
    author='Zachary J. McCord',
    author_email='zjmccord@gmail.com',
    url='https://github.com/zack112358/pdbtest/',
    keywords=['testing', 'pdb', 'unittest'],
    classifiers=["Programming Language :: Python :: 3",
                 "Programming Language :: Python :: 2",
                 "Topic :: Software Development :: Debuggers",
                 "Topic :: Software Development :: Testing",
                 "License :: OSI Approved :: Apache Software License"],
)
