import setuptools

with open("README.md", "rb") as fh:
    long_description = fh.read().decode()

setuptools.setup(
    name="safersympify",
    version="0.1.18",
    author="John Dory",
    author_email="packagebot@gmail.com",
    description="Safer way to sympify unsanitized input",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jpackagebot/safersympify",
    packages=setuptools.find_packages(),
    install_requires=[
        'sympy',
    ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
