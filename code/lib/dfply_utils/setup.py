import setuptools

setuptools.setup(
    name="dfply_utils",
    version="0.0.1",
    author="March",
    author_email="m2.march@gmail.com",
    description="Herramientas para dfply",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
