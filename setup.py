import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python_dice",
    version="0.0.1",
    author="Mark Brockett Robson",
    author_email="mark.brockett.robson@gmail.com",
    description="a statistical dice library for python",
    long_description=long_description,
    url="https://github.com/markbrockettrobson/python_dice",
    packages=[
        'python_dice',
        'python_dice.interface',
        'python_dice.interface.python_dice_expression',
        'python_dice.interface.python_dice_syntax',
        'python_dice.src',
        'python_dice.src.python_dice_expression',
        'python_dice.src.python_dice_syntax'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'matplotlib',
        'rply',
        'networkx',
        'numpy'
    ],
    python_requires='>=3.6',
)