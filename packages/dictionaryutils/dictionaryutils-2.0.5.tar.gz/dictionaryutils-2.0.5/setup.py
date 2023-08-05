from setuptools import setup, find_packages


setup(
    name="dictionaryutils",
    version='2.0.5',
    packages=find_packages(),
    install_requires=["PyYAML>=4.2b1", "jsonschema>=2.5.1"],
    package_data={"dictionaryutils": ["schemas/*.yaml"]},
)
