from setuptools import find_packages, setup

setup(
    name="mvv_sbahn",
    packages=find_packages(include=["mvv_sbahn"]),
    version="0.0.1",
    description="MVV S-Bahn Departures",
    author="Dario Schmid",
    author_email="darioschmid99@outlook.com",
    license="?",
    install_requires=['beautifulsoup4==4.11.1', 'requests'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
    url='https://github.com/darioschmid/mvv_sbahn',
)