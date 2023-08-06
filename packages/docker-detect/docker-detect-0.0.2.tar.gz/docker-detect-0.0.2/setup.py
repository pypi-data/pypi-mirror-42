import setuptools

with open("README.md", "rb") as fh:
    long_description = fh.read().decode()

setuptools.setup(
    name="docker-detect",
    version="0.0.2",
    author="agmarx",
    author_email="agmarx@protonmail.com",
    description="Detect whether the current process is running inside Docker/Kubernetes/LXC container",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/agmarx/docker-detect",
    packages=setuptools.find_packages(),
    install_requires=[
    ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
