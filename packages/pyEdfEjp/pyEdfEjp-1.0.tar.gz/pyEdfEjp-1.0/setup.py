from distutils.core import setup

setup(
    name='pyEdfEjp',
    packages=['pyEdfEjp'],  # this must be the same as the name above
    install_requires=['urllib.request'],
    version='1.0',
    description='a simple python3 library for the E.D.F. EJP Pricing',
    author='Hydreliox',
    author_email='hydreliox@gmail.com',
    url='https://github.com/HydrelioxGitHub/pyEdfEjp',  # use the URL to the github repo
    download_url='https://github.com/HydrelioxGitHub/pyEdfEjp/tarball/1.0',
    keywords=['EDF', 'EJP', 'Energy', 'API'],  # arbitrary keywords
    classifiers=[],
)
