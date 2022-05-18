import setuptools

with open("requirements.lock", "r", encoding="utf-8") as fh:
   requirements = [d.strip() for d in fh.readlines() if "#" not in d]

setuptools.setup( 
     name='hacktheplanets2022',
     author='Addis Antonio, Baroncelli Leonardo, Di Piano Ambra',
     author_email='antonio.addis@inaf.it, leonardo.baroncelli@inaf.it, ambra.dipiano@inaf.it',
     package_dir={'hackp': 'hackp'},
     license='BSD-3-Clause',
     python_requires=">=3.7.9",
     install_requirements=[
          #requirements
     ]
)
