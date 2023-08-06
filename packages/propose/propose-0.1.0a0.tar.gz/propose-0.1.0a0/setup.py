import setuptools

with open('propose/VERSION', 'r') as file:
    version = file.read()
with open('README.md', 'r') as file:
    readme = file.read()

setuptools.setup(
    name='propose',
    version='0.1.0-alpha',
    author='Jonas Hübotter',
    author_email='me@jonhue.me',
    description='Build truthtables with your command line',
    long_description=readme,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    package_data={'propose': ['VERSION']},
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.6'
    ],
    install_requires=['colorama==0.4.1', 'docopt==0.6.2', 'rply==0.7.6'],
    extras_require={
        'dev': ['pytest==4.1.0']
    },
    entry_points={
        'console_scripts': [
            'propose=propose:main'
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/jonhue/propose/issues',
        'Source': 'https://github.com/jonhue/propose'
    }
)
