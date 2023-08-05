from setuptools import setup, find_packages

with open("README.md") as readme_file:
    readme = readme_file.read()

with open("HISTORY.md") as history_file:
    history = history_file.read()

requirements = ["molten>=0.7.1"]

dev_requirements = ["pytest", "pytest-cov", "tox", "jinja2>=2.10,<3.0"]

setup(
    name="molten_mail",
    version="0.1.0",
    description="A simple email component for the Molten web framework",
    long_description=readme + "\n\n" + history,
    long_description_content_type="text/markdown",
    author="Drew Bednar",
    author_email="drew@androiddrew.com",
    url="https://github.com/androiddrew/molten-mail",
    packages=find_packages(include=["molten_mail"]),
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    keywords="molten-mail molten_mail molten mail email SMTP",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    extras_require={"dev": dev_requirements,
                    "templates": ["jinja2>=2.10,<3.0"]},
)
