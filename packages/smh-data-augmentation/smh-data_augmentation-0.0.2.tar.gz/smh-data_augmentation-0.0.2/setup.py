import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="smh-data_augmentation",
    version="0.0.2",
    author="Samuel M.H.",
    author_email="samuel.mh@gmail.com",
    description="A data augmentator package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/beeva-samuelmunoz/data_augmentator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'scikit-image>=0.14.2',
    ]
)

'''
FLOW from: https://packaging.python.org/tutorials/packaging-projects/

# Build
python3 setup.py sdist bdist_wheel

# Reqs
python3 -m pip install --user --upgrade twine

# Test
python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
python3 -m pip install --index-url https://test.pypi.org/simple/ example-pkg-your-username

# Production
python3 -m twine upload dist/*
'''
