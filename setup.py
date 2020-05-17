import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vibrance",
    version="0.0.2",
    author="Wesley Chalmers",
    author_email="wesleyjchalmers@gmail.com",
    description="Crowd-based concert lighting system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Breq16/vibrance",
    packages=["vibrance"],
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 2 - Pre-Alpha"
    ],
    license="MIT",
    python_requires='>=3.6',
    install_requires=[],
    extras_require={
        "midi": ["mido"],
        "relay": ["websockify"],
        "uart": ["pyserial"],
    }
)
