import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()  
    
setuptools.setup(
    name="paasword",
    version="1.0.1",
    license="MIT",
    author="Gilad Soffer",
    keywords=['authentication', 'jwt', 'json web token'],
    author_email="paasword.cto@gmail.com",
    description="Paas-Word authentication for Django",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.paas-word.com",
    packages=['paasword'],
    platforms='any',
    install_requires=[
          'PyJWT',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)