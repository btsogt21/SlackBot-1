from setuptools import setup, find_packages

setup(
    name = 'ShiftClaimer',
    version='0.1',
    packages = find_packages(),
    install_requires = ['selenium', 'beautifulsoup4'],
    python_requires = '>=3.9.7',
    description='Automated script for claiming shifts in Slack.',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourgithub/shiftclaimer',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Build Tools',
    ],
    keywords='slack automation shifts selenium',
    license='MIT'
)