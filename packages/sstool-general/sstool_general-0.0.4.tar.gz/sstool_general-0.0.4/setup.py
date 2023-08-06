import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sstool_general",
    version="0.0.4",
    license='MIT',
    author="Iryna Lokhvytska",
    author_email="ilokh@softserveinc.com",
    description="A general code for the sstool.",
    long_description=long_description,
    packages=setuptools.find_packages(),
    platforms='any',
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'aio_pika==4.6.3',
        'aiohttp==3.4.4',
        'aioredis==1.2.0',
        'motor==2.0.0',
        'sanic>=0.8.3',
        'attrs>=18.2.0'
    ],
    keywords='sanic swagger jira',
    python_requires='==3.6.*',
)
