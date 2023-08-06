import pathlib
import setuptools

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setuptools.setup(
    name='driveline',
    version='0.14.0',
    author='1533 Systems',
    author_email='info@1533.io',
    description='Driveline client',
    long_description=README,
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://github.com/1533-systems/python3-sdk',
    packages=setuptools.find_packages(),
    keywords="driveline performance database streaming document",
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6.0',
    install_requires=[
        'websockets~=7.0',
        'cbor~=1.0',
    ]
)
