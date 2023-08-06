from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(name="lineintf",
      version="1.0.0",
      description="LineIntf - Line Interface makes easy to do tkinter interfaces placing the widgets in line styles.",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="http://github.com/pointel-com-br/lineintf",
      author="Pointel.com.br",
      author_email="master@pointel.com.br",
      license="MIT",
      packages=["lineintf"],
      zip_safe=False)
