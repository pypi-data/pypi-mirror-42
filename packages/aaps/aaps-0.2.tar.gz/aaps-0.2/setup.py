import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='aaps',  
     packages=setuptools.find_packages(),
     version='0.2',
     author="Sergio Chumacero",
     author_email="sergio.chumacero.fi@gmail.com",
     description='Paquete con todas las herramientas para la aplicacion AAPS-LAB.',
     long_description = long_description,
     url="https://github.com/sergio-chumacero/aaps",
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
     install_requires=[
        'numpy',
        'pandas',
        'shapely',
        'fiona',
        'six',
        'pyproj',
        'geopandas',
        'jupyter',
        'jupyterlab',
        'ipywidgets',
        'ipyleaflet',
    ],
 )
