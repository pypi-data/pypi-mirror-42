import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dlprepare",
    version="0.0.2",
    packages = ["dlprepare"],
    include_package_data=True,
    author="Moti Gadian",
    author_email="motkeg@gmail.com",
    #download_url = "https://gitlab.com/motkeg/Dlprepare/-/archive/v0.1/Dlprepare-v0.1.tar.gz",
    description="A data preparetion package for deep learning.",
    keywords = ['deep-learning', 'data preparetion', 'tensorflow'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/motkeg/Dlprepare",
    install_requires=["pandas", "scikit-learn" , "tensorflow"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
        ]
)
                 