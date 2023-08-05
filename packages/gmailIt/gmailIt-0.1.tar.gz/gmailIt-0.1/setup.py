from distutils.core import setup
setup(
    name='gmailIt',
    packages=['gmailIt'],
    version='0.1',
    license='MIT',
    description='Send email via Gmail',
    author='YOUR NAME',
    author_email='mike@lemonshell.com',
    url='https://github.com/kid-on-github/gmailIt',
    download_url='https://github.com/kid-on-github/gmailIt/archive/0.1.tar.gz',
    keywords=['GMAIL', 'EMAIL'],
    install_requires=[
        'apiclient',
        'googleapiclient',
        'httplib2',
        'oauth2client',
        'email'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
)
