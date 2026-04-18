from setuptools import find_packages, setup

#using readme file to populate description
with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="RollOutGui",
    version="0.0.1",
    description="A graphical user interface that analyzes eye movements per video frame",
    package_dir={"":"RollOutGui"},
    packages=find_packages(where="RollOutGui"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thebearslab/VReyetrack",
    author="FevroniaVanSickle",
    license="MIT",
    classifiers=[
                "License :: OSI Approved :: MIT License",
                "Programming Language :: Python :: 3.11",
                "Operating System :: OS Independent"],
    install_requires=["labelme", "pandas >= 2", "tk", "matplotlib >= 3.5", "opencv-python >= 4.5", "shapely >= 2", "Pillow >= 9.5"],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"]
    },
    python_requires=">=3.6",
    entry_points={"console_scripts": ["rolloutmethod=src.main:main"]}



)
print("installed")