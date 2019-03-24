# Notes from pandas_cub project

This note highlights some concepts and tools that I have acquired and used throughout this project. 

## Tools

* conda
* git
* jupyter
* VS Code
* ipython kernels
* pytest

## Concepts 

* Structure for building a library from scratch
* Creating and using development environments
* Test-Driven development

## Python

* Reverse a list or np array
```python 
a[::-1]
```
* Handling and raising errors
* Creating and using private methods
* Python _data model_ and _special methods_
    * `__len__`
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
* Use data type `array.dtype.kind` of numpy
* Use python decorators
* Understand and handle numpy `unicode` type array
* Use `zip`, `enumerate`, `iter`, `next`
* OOP in Python
* Use `_repr_html_` ipython method to produce a represenation of objects in jupyter 
* Use `_ipython_key_completions_` ipython method 
* `List` and `Dictionary` comprehension 
* Understand and use `**kwargs`
* 

numpy
* `ndim`
* `repeat`
* `unique`
* 


