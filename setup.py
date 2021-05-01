import setuptools  # type: ignore

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name="python_dice",
    version="2.0.0",
    author="Mark Brockett Robson",
    author_email="mark.brockett.robson@gmail.com",
    description="a statistical dice library for python",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/markbrockettrobson/python_dice",
    packages=[
        "python_dice",
        "python_dice.interface",
        "python_dice.interface.constraint",
        "python_dice.interface.expression",
        "python_dice.interface.syntax",
        "python_dice.interface.probability_distribution",
        "python_dice.src",
        "python_dice.src.constraint",
        "python_dice.src.expression",
        "python_dice.src.syntax",
        "python_dice.src.probability_distribution",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "matplotlib>=3.1.1",
        "rply>=0.7.7",
        "networkx>=2.3",
        "numpy>=1.17.3",
        "pillow>=7.2.0",
    ],
    python_requires=">=3.6",
)
