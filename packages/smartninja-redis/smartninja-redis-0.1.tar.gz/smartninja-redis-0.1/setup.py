import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='smartninja-redis',
    url='https://github.com/smartninja/smartninja-redis',
    author='Matej Ramuta',
    author_email='matej.ramuta@gmail.com',
    packages=['smartninja_redis'],
    install_requires=[
        'tinydb',
        'redis',
    ],
    version='0.1',
    license='MIT',
    description='SmartNinja Redis - a wrapper that simulates Redis on localhost and uses real Redis in production.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
