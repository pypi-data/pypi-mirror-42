# LIBRERIA COMMONS
---
### Repositorio Pypi: https://pypi.org/project/ol-commons-dev/

![](https://upload.wikimedia.org/wikipedia/commons/3/34/Blue_Python_3.6_Shield_Badge.svg)
![](https://img.shields.io/badge/Flask%20-1.0.2-orange.svg) 
![](https://img.shields.io/badge/PyYAML-3.13-yellow.svg)
![](https://img.shields.io/badge/requests-2.21-blue.svg)


## Estructura del proyecto
---
```
├── commons
│   ├── ol_commons
│   │   ├── configs
│   │   │   ├── logging.yaml
│   │   ├── constants
│   │   │   ├── __init__.py
│   │   │   ├── http_codes.py
│   │   │   ├── messages.py   
│   │   ├── __init__.py
│   │   │── auth.py
│   │   ├── errors.py
│   │   ├── helpers.py
│   │── .gitignore
│   ├── PKG-INFO
│   ├── README.md
│   ├── setup.cfg
│   ├── setup.py
```
##### ARCHIVO DE CONFIGURACION
---
El archivo de configuracion setup.py debe ser modificado para los diferentes ambientes que se manejen.
Por cada nueva modificacion que se realice, se debera modificar la version que se encuentra en setup.py con la nueva.

```python

from setuptools import setup, find_packages

setup(
    name='ol-commons-{#env}',
    packages=find_packages(),  # this must be the same as the name above
    version='x.x.x',
    description='Paquete conteniente objetos reutilizables para los microservicios de OLYMPUS',
    long_description=open('README.md').read(),
    author='Jean Pier Barbieri Rios',
    author_email='jean.barbieri1996@gmail.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
    ], install_requires=['requests', 'flask', 'PyYAML']
)


```


##### COMANDOS PARA ACTUALIZAR LA LIBRERIA EN EL REPOSITORIO DE PYPI
---
Los siguientes comandos deberan ser ejecutados en el orden indicando para poder realizar un push hacia 
el repositorio de PYPI.

Solo en caso que la carpeta dist haya sido creada:
```bash
$ rm -r dist
```

Siempre para el upload de la nueva version:
```bash
$ python setup.py sdist
$ pip install twine
$ twine upload dist/*
```



Todos los derechos reservados VF CONSULTING S.A.C

