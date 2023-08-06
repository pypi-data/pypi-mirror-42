import setuptools

# with open("README.md", 'r') as f:
#     long_description = f.read()

setuptools.setup(
   name='fontcell',
   version='1.0',
   description='FOntCell - A software tool for automatic parallel computed fusion of ontologies',
   # long_description=long_description,
   # license="LICENSE",
   author='Javier Cabau Laporta',
   author_email='jcabaulaporta@outlook.es',
   # url="https://gitlab.com/jcabaulaporta/FOntcell",
   install_requires=['StringDist>=1.0.9', 'graphviz>=0.10.1', 'matplotlib>=2.2.4', 'networkx>=2.2', 'numpy>=1.16.1',
                     'pandas>=0.24.1', 'plotly>=3.6.1', 'pyexcel>=0.5.12', 'pyexcel-ods>=0.5.4', 'seaborn>=0.9.0',
                     'bigmpi4py>=1.2.3', 'mpi4py>=3.0.1'],
   include_package_data=True,
   packages=setuptools.find_packages(),
   classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
      "Operating System :: OS Independent",
   ],
)
