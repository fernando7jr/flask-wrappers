from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='flask_wrappers',
    packages=['flask_wrappers'],
    version='1.0.2',
    description='Decorators to facilitate flask enpoints implementation',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='metadeta96',
    author_email='fernando.settijunior@gmail.com',
    url='https://github.com/metadeta96/flask-wrappers',
    download_url='https://github.com/metadeta96/flask-wrappers',
    keywords=['flask', 'decorator', 'route', 'wrapper'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3'
)
