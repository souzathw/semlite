from setuptools import setup, find_packages

setup(
    name="semlite",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "semopy",
        "statsmodels"
    ],
    author="PontesTI",
    description="Pacote simplificado para análise de equações estruturais (MEE) ou SEM, com foco em mediação e moderação acessível via R",
    long_description = open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Education",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
