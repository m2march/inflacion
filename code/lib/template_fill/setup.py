import setuptools

setuptools.setup(
    name="template_fill",
    version="0.0.1",
    author="March",
    author_email="m2.march@gmail.com",
    description="Herramientas para compilar un archivo template usando Jinja",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    scripts=['scripts/template_fill'],
    python_requires=">=3.6",
)
