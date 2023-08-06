import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='lighteda',
     version='0.0.2',
     # scripts=['dokr'],
     author="Johnny Li",
     author_email="l.johnny@outlook.com",
     description="A package for exploratoriy data analysis.",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/j84lee/lighteda",
     packages=setuptools.find_packages(),
     keywords=['EDA', 'Data Science'],
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
