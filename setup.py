from setuptools import find_packages, setup
from pathlib import Path

# read the contents of your README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="MVVLive",
    packages=find_packages(include=["MVVLive"]),
    version="0.1.0",
    description="Live public transportation data for Munich public transport",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Dario Schmid",
    author_email="darioschmid99@outlook.com",
    license="?",
    install_requires=['soupsieve==2.3.2.post1', 'beautifulsoup4==4.11.1', 'requests', 'pathlib'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
    url='https://github.com/darioschmid/PyMVVLive',
)
