import setuptools

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name="python_dice",
    version="0.0.5",
    author="Mark Brockett Robson",
    author_email="mark.brockett.robson@gmail.com",
    description="a statistical dice library for python",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/markbrockettrobson/python_dice",
    packages=[
        "python_dice",
        "python_dice.interface",
        "python_dice.interface.python_dice_expression",
        "python_dice.interface.python_dice_syntax",
        "python_dice.src",
        "python_dice.src.python_dice_expression",
        "python_dice.src.python_dice_syntax",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "matplotlib==3.1.1",
        "rply==0.7.7",
        "networkx==2.3",
        "numpy==1.17.3",
        "pillow==6.2.1",
    ],
    python_requires=">=3.6",
)
