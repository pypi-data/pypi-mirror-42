from setuptools import setup, find_packages

setup(
    name = 'bayo-sanity',
    version = '0.0.3',
    description = 'This is a dummy package.',
    packages = find_packages(),
)

raise RuntimeError("This is a dummy package that was never ment to be actually installed. Please contact platform(at)kiwi.com.")

