from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="taskflow-ai",
    version="1.1.0",
    description="Herramienta CLI con IA para gestión de tareas con Taskwarrior y GitHub",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="TaskFlow AI Team",
    author_email="contact@taskflow-ai.com",
    url="https://github.com/taskflow-ai/taskflow-ai",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=requirements,
    extras_require={
        "openai": ["openai>=1.0.0"],
        "local-llm": ["transformers>=4.30.0", "torch>=2.0.0"],
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "taskflow=taskflow.cli.main:cli",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Office/Business :: Scheduling",
    ],
    keywords="taskwarrior github ai cli productivity",
)