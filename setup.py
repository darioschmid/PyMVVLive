from setuptools import find_packages, setup

setup(
    name="MVVLive",
    packages=find_packages(include=["MVVLive"]),
    version="0.0.1",
    description="Live MVV data for Munich public transport",
    author="Dario Schmid",
    author_email="darioschmid99@outlook.com",
    license="?",
    install_requires=['soupsieve==2.3.2.post1', 'beautifulsoup4==4.11.1', 'requests'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
    url='https://github.com/darioschmid/MVVLive',
)