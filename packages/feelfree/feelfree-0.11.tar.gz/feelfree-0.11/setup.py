from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()
	
setup(name='feelfree',
      version='0.11',
      description='The free version of FEEL package',
	  long_description=long_description,
	  long_description_content_type="text/markdown",
      url='https://github.com/fangj99/feelfree',
      author='Lau & Fang',
      author_email='fangj99@gmail.com',
      license='GNU',
      packages=['feelfree'],
      zip_safe=False,
	  #packages=setuptools.find_packages(),
	  classifiers=[
	      "Programming Language :: Python :: 3",
		  "Operating System :: OS Independent",
	  ],
)