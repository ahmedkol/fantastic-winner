from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="rona-v5",
    version="5.0.0",
    author="Rona AI Assistant",
    author_email="rona@example.com",
    description="مساعد ذكي مع ميزة البحث في الإنترنت وتحليل قاعدة البيانات المحلية",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/rona-v5",
    packages=find_packages(),
    py_modules=[
        'rona_v5_updated',
        'internet_search',
        'run_rona',
        'quick_test',
        'test_ollama',
        'test_gui',
        'test_database',
        'test_internet_search',
        'test_application',
        'test_performance',
        'test_integration',
        'test_security',
        'test_compatibility',
        'run_all_tests'
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "rona=rona_v5_updated:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.json", "*.txt", "*.md"],
    },
    keywords="ai assistant chatbot internet search vector database langchain ollama",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/rona-v5/issues",
        "Source": "https://github.com/yourusername/rona-v5",
        "Documentation": "https://github.com/yourusername/rona-v5/blob/main/README.md",
    },
)