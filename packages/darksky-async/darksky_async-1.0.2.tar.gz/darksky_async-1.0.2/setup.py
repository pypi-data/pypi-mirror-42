import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="darksky_async",
    version="1.0.2",
    author="Cerulean",
    author_email="cerulean.connor@gmail.com",
    description="An async wrapper for DarkSky",
    long_description=long_description,
    url="https://github.com/AggressivelyMeows/darksky_async",
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    classifiers=[
        "Framework :: AsyncIO ",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)