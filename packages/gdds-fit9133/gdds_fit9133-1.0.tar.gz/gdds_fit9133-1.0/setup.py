import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='gdds_fit9133',
     version='1.0',
     author="lei yang",
     author_email="lei.yang@monash.edu",
     description="fit9133 module",
     long_description=long_description,
   long_description_content_type="text/markdown",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
