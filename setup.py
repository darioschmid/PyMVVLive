from setuptools import find_packages, setup

setup(
    name="MVVsBahn",
    packages=find_packages(include=["MVVsBahn"]),
    version="0.0.1",
    description="MVV S-Bahn Departures",
    author="Dario Schmid",
    author_email="darioschmid99@outlook.com",
    license="?",
    install_requires=['soupsieve==2.3.2', 'beautifulsoup4==4.11.1', 'requests'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
    url='https://github.com/darioschmid/MVVsBahn',
)