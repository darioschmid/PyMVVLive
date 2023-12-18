from setuptools import find_packages, setup
from pathlib import Path

# read the contents of your README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="MVVLive",
    packages=find_packages(include=["MVVLive"]),
    version="1.0.2",
    description="Live public transportation data for Munich public transport",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Dario Schmid",
    author_email="darioschmid99@outlook.com",
    license="?",
    install_requires=['soupsieve==2.5', 'beautifulsoup4==4.12.2', 'requests',
                      'pathlib'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1', 'python-dotenv==1.0.0'],
    test_suite='tests',
    url='https://github.com/darioschmid/PyMVVLive',
)
