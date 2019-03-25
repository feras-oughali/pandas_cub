# Notes from pandas_cub project

This note highlights some concepts and tools that I have acquired and used throughout this project. 

The project aims at replicating some of the functionalities of the famous `pandas` library. The size of the project and the concepts used within are prefect for those who are looking forward to enhance their development skills and tackle a project that is interesting, managable, and informative at the same time. 

This project was developed by XXXX. You can refer to XXX for more details about the project.

I added a flavour of `git` to the project to maximize the benefits. 

## Concepts used in the project

* Structure for building a library from scratch
* Creating and using development environments
* Test-Driven development


## Tools and libraries used in the project

* conda
* jupyter
* VS Code
* ipython kernels
* git
* pytest
* numpy



## Python

* Reverse a list or np array
```python 
a[::-1]
```
* Handling and raising errors
* Creating and using private methods
* Python _data model_ and _special methods_
    * `__len__`
    * `__doc__`
    * `__add__`
    * `__radd__`
    * `__truediv__`
    * `__floordiv__`
    * `__pow__`
    * `__gt__`
    * `__lt__`
    * `__ge__`
    * `__ne__`
    * `__eq__`
    * `__getitem__`
    * `__setitem__`
    * `@property`
    * `@columns.setter`
```Python
@property
    def columns(self):

@columns.setter
    def columns(self, columns):
```
* Use the `isinstance` function
* Use the `getattr` function
* Use data type `array.dtype.kind` of numpy
* Use python decorators
* Understand and handle numpy `unicode` type array
* Use `zip`, `enumerate`, `iter`, `next`
* OOP in Python
* Use `_repr_html_` ipython method to produce a represenation of objects in jupyter 
* Use `_ipython_key_completions_` ipython method 
* `List` and `Dictionary` comprehension 
* Understand and use `*args` and `**kwargs`
* Automatically add documentation
* Create a group of methods with the an `accessor` like _pandas_ `str`, `dt`, and `cat`
* Use a defaultdict

numpy
* `ndim`
* `repeat`
* `unique`
* `roll`
* `isnan`
* `argsort`
* `lexsort`
* `random.choice`
* 


