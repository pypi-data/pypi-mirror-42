import re
import setuptools

with open("botpie/__init__.py", "r") as fh:
    ptn = r"^__version__\s*=\s*['\"]([^'\"]*)['\"]"
    matched = re.search(ptn, fh.read(), re.M)

if not matched:
    raise RuntimeError("failed to find version")

version = matched.group(1)

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="botpie",
    version=version,
    author="gwilkes",
    description="A Python framework for managing chatbots",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gwilkes/botpie",
    packages=setuptools.find_packages(),
    include_package_data=True,
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)