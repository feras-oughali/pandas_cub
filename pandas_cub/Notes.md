# Notes from pandas_cub project

This note highlights some concepts and tools that have been used throughout this project. 

The project aims at replicating some of the functionalities of the famous `Pandas` library. The size of the project and the concepts used within are prefect for those who are looking forward to enhance their development skills and tackle a project that is interesting, managable, and informative at the same time. 

This project was developed by Ted Petrou. You can refer to [this link](https://online.dunderdata.com/courses/build-a-data-analysis-library-from-scratch-in-python) for more details about the project.

I added a flavour of `git` to the project to maximize the benefits. 

## Concepts covered in the project

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


## Takeaways from the project 

* Understand structure of building a library 
* Handling and raising errors
* Creating and using private methods
* Use python decorators
* OOP in Python
* Python _data model_ and _special methods_
* Use the `isinstance` function
* Use the `getattr` function
* Use `_repr_html_` ipython method to produce a represenation of objects in jupyter 
* Use `_ipython_key_completions_` ipython method 
* Use `zip`, `enumerate`, `iter`, `next`
* Understand and use `*args` and `**kwargs`* 
* Create a group of methods with the an `accessor` like _pandas_ `str`, `dt`, and `cat`
* Automatically add documentation
* Use a defaultdict


### numpy
* `ndim`
* `repeat`
* `unique`
* `roll`
* `isnan`
* `argsort`
* `lexsort`
* `random.choice`
* `array.dtype.kind`
* `unicode` type array
* Reverse a list or np array
```python 
a[::-1]
```

### python
* Some of the Magic functions used in the project
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
    * `@property.setter`
```Python
@property
    def columns(self):

@columns.setter
    def columns(self, columns):
```




