from setuptools import setup, find_packages

setup(
    name='myfs-project',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A file system management tool with encryption and metadata handling.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/myfs-project',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        # Add your project dependencies here
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)