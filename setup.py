import setuptools

setuptools.setup(
    name="flux-sa",
    version="1.0.0",
    author="Alexandru Stoica",
    author_email="stoica.alexandru2000@gmail.com",
    description="Syntactic analizer for flux.",
    url="https://github.com/alexandrustoica/flux.syntactic.analyzer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
