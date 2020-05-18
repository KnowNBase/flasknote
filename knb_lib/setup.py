from setuptools import setup, find_packages  # type: ignore

setup(
      name="knowbase",
      version="0.1",
      url="https://github.com/intey/knb-core",
      license="MIT",
      author="Intey",
      author_email="ziexe0@gmail.com",
      description="Core domain for making knowledge base",
      packages=[
            '.',
            'errors',
            'use_cases',
            'utils',
            ],
      long_description=open("README.md").read(),
      zip_safe=False,
)
