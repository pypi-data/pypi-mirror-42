import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    setuptools.setup(
                     name='littlebluefox-python',  
                     version='1.0.2',
                     author="Sam",
                     author_email="sam@littlebluefox.io",
                     description="Official python client for LittleBlueFox.io API",
                     long_description=long_description,
                     long_description_content_type="text/markdown",
                     url="https://github.com/littlebluefox/littlebluefox-python",
                     packages=['littlebluefox'],
                     classifiers=[
                     "Programming Language :: Python :: 3",
                     "License :: OSI Approved :: MIT License",
                     "Operating System :: OS Independent",
                     ],
                     )
