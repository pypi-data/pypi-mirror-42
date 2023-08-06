import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='deep-helm-of',  
     version='1.1',
     scripts=['deep-helm-of.py'] ,
     author="David Martirosyan",
     author_email="david.mart@sadasystems.com",
     description="A punch for suckers",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/davidmart/deep-helm-of",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
