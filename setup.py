from setuptools import setup, find_packages

setup(
    name="braillevision-ocr",
    version="1.0.0",
    author="Sais-gallego",
    description="Computer Vision Braille Recognition & Text-to-Speech Accessibility Engine",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Sais-gallego/braillevision-ocr",
    packages=find_packages(),
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "brailleocr=brailleocr.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
    ],
)
