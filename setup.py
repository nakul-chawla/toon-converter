"""Setup script for TOON Converter."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="toon-converter",
    version="0.1.0",
    author="Nakul Chawla",
    author_email="nakul.chawla1312@gmail.com",
    description="Token-Oriented Object Notation - Compact JSON serialization for LLM prompts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nakul-chawla/toon-converter",
    project_urls={
        "Bug Tracker": "https://github.com/nakul-chawla/toon-converter/issues",
        "Documentation": "https://toon-converter.readthedocs.io",
        "Source Code": "https://github.com/nakul-chawla/toon-converter",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing",
    ],
    python_requires=">=3.8",
    install_requires=[],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "api": [
            "fastapi>=0.104.0",
            "uvicorn[standard]>=0.24.0",
            "pydantic>=2.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "toon=cli.main:main",
        ],
    },
    keywords="json toon llm serialization converter token-efficient",
    license="MIT",
)
