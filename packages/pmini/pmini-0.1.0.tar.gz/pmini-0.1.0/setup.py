import setuptools

with open("README.md", "r") as fp:
    long_description = fp.read()



setuptools.setup(
    name='pmini',
    version="0.1.0",
    author="Ryan",
    author_email='1172683546@qq.com',
    description='A test programmes',
    long_description=long_description, 
    long_description_content_type="text/markdown",   
    url='http://www.vnpy.org',
    packages=setuptools.find_packages(),
    classifiers=[
                 'Programming Language :: Python :: 3',
                 'License :: OSI Approved :: MIT License',
                 'Operating System :: Microsoft :: Windows :: Windows 8',
                 'Operating System :: Microsoft :: Windows :: Windows 10',
                 'Operating System :: Microsoft :: Windows :: Windows Server 2008'
    ]
)