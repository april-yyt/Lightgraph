from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="lightgraph",
    version="0.1.0",
    author="April Yang",
    author_email="aprilyangyyt@gmail.com",
    description="A lightweight framework for serving LangGraph runnables",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/april-yyt/lightgraph",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
    install_requires=[
        "fastapi",
        "pydantic",
        "langchain-core",
    ],
)