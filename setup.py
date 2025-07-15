from setuptools import setup, find_packages
import os

readme_path = os.path.join(os.path.dirname(__file__), "README.md")
try:
    with open(readme_path, encoding="utf-8") as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "Pacote simplificado para análise de equações estruturais (MEE) com moderação e mediação"

setup(
    name="semlite",
    version="0.1",
    packages=find_packages(),
    include_package_data=True, 
    install_requires=[
        "pandas",
        "semopy",
        "statsmodels", 
    ],
    author="PontesTI",
    description="Pacote simplificado para análise de equações estruturais (MEE) ou SEM, com foco em mediação e moderação acessível via R",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Education",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
