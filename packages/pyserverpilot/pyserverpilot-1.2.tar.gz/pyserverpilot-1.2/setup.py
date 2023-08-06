import setuptools

if __name__ == '__main__':
    with open('README.md', 'r') as fh:
        long_description = fh.read()

    setuptools.setup(
        name='pyserverpilot',
        version='1.2',
        author='opper',
        author_email='alex@opper.nl',
        description=(
            'Python wrapper for the ServerPilot API.'
        ),
        long_description=long_description,
        long_description_content_type='text/markdown',
        url='https://github.com/opper/pyserverpilot',
        packages=['pyserverpilot'],
        classifiers=(
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.7',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
        ),
        install_requires=[
            'requests',
        ],
        include_package_data=True
    )
