from setuptools import find_packages, setup

setup(
    name="mvv_sbahn",
    packages=find_packages(include=["mvv_sbahn"]),
    version="0.0.1",
    description="MVV S-Bahn Departures",
    author="Dario Schmid",
    license="MIT",
    install_requires=['beautifulsoup4==4.11.1', 'paho-mqtt==1.6.1 '],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)