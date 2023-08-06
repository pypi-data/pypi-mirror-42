from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
     name='aaps',  
     packages=['aaps',],
     version='0.1',
     author="Deepak Kumar",
     author_email="deepak.kumar.iet@gmail.com",
     description='Paquete con todas las herramientas para la aplicacion AAPS-LAB.',
     url="https://github.com/sergio-chumacero/aaps",
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )