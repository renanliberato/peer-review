from setuptools import setup, find_packages

setup(
    name="peer-review",
    version="0.1.0",
    description="A CLI tool to rephrase text using OpenRouter API",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "python-dotenv>=0.19.0",
        "rich",
    ],
    entry_points={
        "console_scripts": [
            "peer-review=app:main",
        ],
    },
    python_requires=">=3.7",
)
