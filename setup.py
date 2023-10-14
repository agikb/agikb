from setuptools import setup, find_packages

setup(
    name="agikb",
    version="0.0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "agikb=agikb.server.cli:cli",
        ],
    },
    author="starkwang",
    author_email="starkwanglab@gmail.com",
    description="Retrieval-Augmented Generation (RAG) applications.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/agiclass/agikb",
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    include_package_data=True,
    install_requires=[
        "weaviate-client>=3.23.1",
        "python-dotenv>=1.0.0",
        "openai>=0.27.9",
        "wasabi>=1.1.2",
        "spacy",
        "fastapi>=0.102.0",
        "uvicorn[standard]",
        "click>= 8.1.7",
    ],
    extras_require={"dev": ["pytest", "wheel", "twine", "black", "setuptools"]},
)
