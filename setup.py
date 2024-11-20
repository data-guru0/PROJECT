from setuptools import setup, find_packages

# Read dependencies from requirements.txt
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="mlops_project",
    version="0.1",
    author="Your Name",
    author_email="your.email@example.com",
    description="An MLOps project setup with custom logging and exception handling",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.7',
)
