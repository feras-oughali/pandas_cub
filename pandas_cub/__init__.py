import numpy as np

__version__ = '0.0.1'


class DataFrame:

    def __init__(self, data):
        """
        A DataFrame holds two dimensional heterogeneous data. Create it by
        passing a dictionary of NumPy arrays to the values parameter

        Parameters
        ----------
        data: dict
            A dictionary of strings mapped to NumPy arrays. The key will
            become the column name.
        """
        # check for correct input types
        self._check_input_types(data)

        # check for equal array lengths
        self._check_array_lengths(data)

        # convert unicode arrays to object
        self._data = self._convert_unicode_to_object(data)

        # Allow for special methods for strings
        self.str = StringMethods(self)
        self._add_docs()

    def _check_input_types(self, data):
        if not isinstance(data, dict):
            raise TypeError('Data must be a `dict`')
        
        for key, val in data.items():
            if not isinstance(key, str):
                raise TypeError('keys must be strings')
            if not isinstance(val, np.ndarray):
                raise TypeError('values must be numpy arrays')
            if val.ndim != 1:
                raise ValueError('values must be 1-d arrays')
        

    def _check_array_lengths(self, data):
        for i, val in enumerate(data.values()):
            if i==0:
                length = len(val)
            elif length != len(val):
                raise ValueError('lenght of values in `data` must be equal')


    def _convert_unicode_to_object(self, data):
        new_data = {}
        for key, val in data.items():
            if val.dtype.kind == 'U':
                new_data[key] = data[key].astype('object')
            else:
                new_data[key] = data[key]
        return new_data

    def __len__(self):
        """
        Make the builtin len function work with our dataframe

        Returns
        -------
        int: the number of rows in the dataframe
        """
        return len(next(iter(self._data.values())))

    @property
    def columns(self):
        """
        _data holds column names mapped to arrays
        take advantage of internal ordering of dictionaries to
        put columns in correct order in list. Only works in 3.6+

        Returns
        -------
        list of column names
        """
        return list(self._data) #this will retrun the a list of keys only!

    @columns.setter
    def columns(self, columns):
        """
        Must supply a list of columns as strings the same length
        as the current DataFrame

        Parameters
        ----------
        columns: list of strings

        Returns
        -------
        None
        """
        if not isinstance(columns, list):
            raise TypeError('A list is expected')
        if len(columns) != len(self._data):
            raise ValueError('length of `columns` must equals to Dataframe\'s columns')
        for col in columns:
            if not isinstance(col, str):
                raise TypeError('all column names must be strings')
        if len(columns) != len(set(columns)):
            raise ValueError('list of `columns` must have no duplicates')
        self._data = dict(zip(columns, self._data.values()))
        

    @property
    def shape(self):
        """
        Returns
        -------
        two-item tuple of number of rows and columns
        """
        return len(self), len(self._data)

    def _repr_html_(self):
        """
        Used to create a string of HTML to nicely display the DataFrame
        in a Jupyter Notebook. Different string formatting is used for
        different data types.

        The structure of the HTML is as follows:
        <table>
            <thead>
                <tr>
                    <th>data</th>
                    ...
                    <th>data</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>{i}</strong></td>
                    <td>data</td>
                    ...
                    <td>data</td>
                </tr>
                ...
                <tr>
                    <td><strong>{i}</strong></td>
                    <td>data</td>
                    ...
                    <td>data</td>
                </tr>
            </tbody>
        </table>
        """
        # copied form solution manual!
        
        html = '<table><thead><tr><th></th>'
        for col in self.columns:
            html += f"<th>{col:10}</th>"

        html += '</tr></thead>'
        html += "<tbody>"

        only_head = False
        num_head = 10
        num_tail = 10
        if len(self) <= 20:
            only_head = True
            num_head = len(self)

        for i in range(num_head):
            html += f'<tr><td><strong>{i}</strong></td>'
            for col, values in self._data.items():
                kind = values.dtype.kind
                if kind == 'f':
                    html += f'<td>{values[i]:10.3f}</td>'
                elif kind == 'b':
                    html += f'<td>{values[i]}</td>'
                elif kind == 'O':
                    v = values[i]
                    if v is None:
                        v = 'None'
                    html += f'<td>{v:10}</td>'
                else:
                    html += f'<td>{values[i]:10}</td>'
            html += '</tr>'

        if not only_head:
            html += '<tr><strong><td>...</td></strong>'
            for i in range(len(self.columns)):
                html += '<td>...</td>'
            html += '</tr>'
            for i in range(-num_tail, 0):
                html += f'<tr><td><strong>{len(self) + i}</strong></td>'
                for col, values in self._data.items():
                    kind = values.dtype.kind
                    if kind == 'f':
                        html += f'<td>{values[i]:10.3f}</td>'
                    elif kind == 'b':
                        html += f'<td>{values[i]}</td>'
                    elif kind == 'O':
                        v = values[i]
                        if v is None:
                            v = 'None'
                        html += f'<td>{v:10}</td>'
                    else:
                        html += f'<td>{values[i]:10}</td>'
                html += '</tr>'

        html += '</tbody></table>'
        return html

    @property
    def values(self):
        """
        Returns
        -------
        A single 2D NumPy array of the underlying data
        """
        return np.column_stack(list(self._data.values()))

    @property
    def dtypes(self):
        """
        Returns
        -------
        A two-column DataFrame of column names in one column and
        their data type in the other
        """
        DTYPE_NAME = {'O': 'string', 'i': 'int', 'f': 'float', 'b': 'bool'}
        col_names = np.array(list(self._data.keys()))
        types = [DTYPE_NAME[val.dtype.kind] for val in self._data.values()]
        types = np.array(types)
        new_data = {'column name':col_names, 'data type':types}
        return DataFrame(new_data)

    def __getitem__(self, item):
        """
        Use the brackets operator to simultaneously select rows and columns
        A single string selects one column -> df['colname']
        A list of strings selects multiple columns -> df[['colname1', 'colname2']]
        A one column DataFrame of booleans that filters rows -> df[df_bool]
        Row and column selection simultaneously -> df[rs, cs]
            where cs and rs can be integers, slices, or a list of integers
            rs can also be a one-column boolean DataFrame

        Returns
        -------
        A subset of the original DataFrame
        """
        if isinstance(item, str):
            return DataFrame({item:self._data[item]})
        if isinstance(item, list):\
            return DataFrame({i:self._data[i] for i in item})
        if isinstance(item, DataFrame):
            if len(item.columns) != 1: raise ValueError('DataFrame must have one col only')
            b_arr = next(iter(list(item._data.values())))
            if b_arr.dtype.kind !='b': raise TypeError('DataFrame must be of bool type')
            return DataFrame({col:val[b_arr] for col,val in self._data.items()})



    def _getitem_tuple(self, item):
        # simultaneous selection of rows and cols -> df[rs, cs]
        pass

    def _ipython_key_completions_(self):
        # allows for tab completion when doing df['c
        return self.columns

    def __setitem__(self, key, value):
        # adds a new column or a overwrites an old column
        if not isinstance(key, str):
            raise NotImplementedError('DataFrame can set only one column at a time')
        if isinstance(value, np.ndarray):
            if value.ndim != 1:
                raise ValueError('Array must be 1-D numpy array')
            if value.shape[0] != self.shape[0]:
                raise ValueError('Length of array is not matching length of DataFrame')
        elif isinstance(value, DataFrame):
            if self.shape[1] != 1:
                raise ValueError('New values must be a single column DataFrame')
            if len(value) != len(self):
                raise ValueError('Length of new values is not matching length of DataFrame')
            value = next(iter(self._data.values()))
        elif isinstance(value, (int, bool, str, float)):
            value = np.repeat(value, len(self))
        else: 
            raise TypeError('Provided new value is not valid')
        
        if value.dtype.kind == 'U':
            value = value.astype('object')
        
        self._data[key] = value

    def head(self, n=5):
        """
        Return the first n rows

        Parameters
        ----------
        n: int

        Returns
        -------
        DataFrame
        """
        return DataFrame({key:val[:n] for key, val in self._data.items()})

    def tail(self, n=5):
        """
        Return the last n rows

        Parameters
        ----------
        n: int
        
        Returns
        -------
        DataFrame
        """
        return DataFrame({key:val[-n:] for key, val in self._data.items()})

    #### Aggregation Methods ####

    def min(self):
        return self._agg(np.min)

    def max(self):
        return self._agg(np.max)

    def mean(self):
        return self._agg(np.mean)

    def median(self):
        return self._agg(np.median)

    def sum(self):
        return self._agg(np.sum)

    def var(self):
        return self._agg(np.var)

    def std(self):
        return self._agg(np.std)

    def all(self):
        return self._agg(np.all)

    def any(self):
        return self._agg(np.any)

    def argmax(self):
        return self._agg(np.argmax)

    def argmin(self):
        return self._agg(np.argmin)

    def _agg(self, aggfunc):
        """
        Generic aggregation function that applies the
        aggregation to each column

        Parameters
        ----------
        aggfunc: str of the aggregation function name in NumPy
        
        Returns
        -------
        A DataFrame
        """
        new_data = {}
        for col, val in self._data.items():
            try: 
                new_data[col]= np.array([aggfunc(val)])
            except TypeError:
                pass
        return DataFrame(new_data)

    def isna(self):
        """
        Determines whether each value in the DataFrame is missing or not

        Returns
        -------
        A DataFrame of booleans the same size as the calling DataFrame
        """
        new_data = {}
        for key, val in self._data.items():
            if val.dtype.kind=='O':
                new_data[key] = val==None
            else:
                new_data[key] = np.isnan(val)
        return DataFrame(new_data)

    def count(self):
        """
        Counts the number of non-missing values per column

        Returns
        -------
        A DataFrame
        """
        new_data = {}
        na_count = self.isna().sum()
        for key, val in na_count._data.items():
            new_data[key]= len(self)-val
        return DataFrame(new_data)

    def unique(self):
        """
        Finds the unique values of each column

        Returns
        -------
        A list of one-column DataFrames
        """
        dfs = []
        for key, val in self._data.items():
            new_data = {}
            new_data[key] = np.unique(val)
            dfs.append(DataFrame(new_data))
        if len(dfs)==1:
            return dfs[0]
        return dfs

    def nunique(self):
        """
        Find the number of unique values in each column

        Returns
        -------
        A DataFrame
        """
        new_data = {}
        for key, val in self._data.items():
            new_data[key]=np.array([len(np.unique(val))])
        return DataFrame(new_data)

    def value_counts(self, normalize=False):
        """
        Returns the frequency of each unique value for each column

        Parameters
        ----------
        normalize: bool
            If True, returns the relative frequencies (percent)

        Returns
        -------
        A list of DataFrames or a single DataFrame if one column
        """
        dfs = []
        for key, val in self._data.items():
            uniques, counts = np.unique(val, return_counts=True)
            order = np.argsort(-counts)
            uniques = uniques[order]
            counts = counts[order]
            if normalize:
                counts = counts/counts.sum()
            dfs.append(DataFrame({key:uniques, 'count':counts}))
        if len(dfs)==1:
            return dfs[0]
        return dfs

        

    def rename(self, columns):
        """
        Renames columns in the DataFrame

        Parameters
        ----------
        columns: dict
            A dictionary mapping the old column name to the new column name
        
        Returns
        -------
        A DataFrame
        """
        if not isinstance(columns, dict):
            raise TypeError('Columns must be a `dict`')
        new_data = {}
        for key, val in self._data.items():
            new_col = columns.get(key, key)
            new_data[new_col]=val
        return DataFrame(new_data)

    def drop(self, columns):
        """
        Drops one or more columns from a DataFrame

        Parameters
        ----------
        columns: str or list of strings

        Returns
        -------
        A DataFrame
        """
        if isinstance(columns, str):
            columns = [columns]
        elif not isinstance(columns, list):
            raise TypeError('columns must be a `str` or a `list`')
        new_data = {}
        for key, val in self._data.items():
            if not key in columns:
                new_data[key]=val
        return DataFrame(new_data)


    #### Non-Aggregation Methods ####

    def abs(self):
        """
        Takes the absolute value of each value in the DataFrame

        Returns
        -------
        A DataFrame
        """
        return self._non_agg(np.abs)

    def cummin(self):
        """
        Finds cumulative minimum by column

        Returns
        -------
        A DataFrame
        """
        return self._non_agg(np.minimum.accumulate)

    def cummax(self):
        """
        Finds cumulative maximum by column

        Returns
        -------
        A DataFrame
        """
        return self._non_agg(np.maximum.accumulate)

    def cumsum(self):
        """
        Finds cumulative sum by column

        Returns
        -------
        A DataFrame
        """
        return self._non_agg(np.cumsum)

    def clip(self, lower=None, upper=None):
        """
        All values less than lower will be set to lower
        All values greater than upper will be set to upper

        Parameters
        ----------
        lower: number or None
        upper: number or None

        Returns
        -------
        A DataFrame
        """
        return self._non_agg(np.clip, a_min=lower, a_max=upper)

    def round(self, n):
        """
        Rounds values to the nearest n decimals

        Returns
        -------
        A DataFrame
        """
        return self._non_agg(np.round, decimals=n)

    def copy(self):
        """
        Copies the DataFrame

        Returns
        -------
        A DataFrame
        """
        return self._non_agg(np.copy)

    def _non_agg(self, funcname, **kwargs):
        """
        Generic non-aggregation function
    
        Parameters
        ----------
        funcname: str of NumPy name
        kwargs: extra keyword arguments for certain functions

        Returns
        -------
        A DataFrame
        """
        new_data = {}
        for key, val in self._data.items():
            if val.dtype.kind=='O':
                new_data[key] = val.copy()
            else:
                new_data[key] = funcname(val, **kwargs)
        return DataFrame(new_data)

    def diff(self, n=1):
        """
        Take the difference between the current value and
        the nth value above it.

        Parameters
        ----------
        n: int

        Returns
        -------
        A DataFrame
        """
        def func(value):
            value = value.astype('float')
            shifted_value = np.roll(value, n)
            value = value - shifted_value
            if n>=0:
                value[:n]=np.nan
            else:
                value[n:]=np.nan
            return value

        return self._non_agg(func)

    def pct_change(self, n=1):
        """
        Take the percentage difference between the current value and
        the nth value above it.

        Parameters
        ----------
        n: int

        Returns
        -------
        A DataFrame
        """
        def func(value):
            value = value.astype('float')
            shifted_value = np.roll(value, n)
            value = (value - shifted_value) / shifted_value
            if n>=0:
                value[:n]=np.nan
            else:
                value[n:]=np.nan
            return value

        return self._non_agg(func)

    #### Arithmetic and Comparison Operators ####

    def __add__(self, other):
        return self._oper('__add__', other)

    def __radd__(self, other):
        return self._oper('__radd__', other)

    def __sub__(self, other):
        return self._oper('__sub__', other)

    def __rsub__(self, other):
        return self._oper('__rsub__', other)

    def __mul__(self, other):
        return self._oper('__mul__', other)

    def __rmul__(self, other):
        return self._oper('__rmul__', other)

    def __truediv__(self, other):
        return self._oper('__truediv__', other)

    def __rtruediv__(self, other):
        return self._oper('__rtruediv__', other)

    def __floordiv__(self, other):
        return self._oper('__floordiv__', other)

    def __rfloordiv__(self, other):
        return self._oper('__rfloordiv__', other)

    def __pow__(self, other):
        return self._oper('__pow__', other)

    def __rpow__(self, other):
        return self._oper('__rpow__', other)

    def __gt__(self, other):
        return self._oper('__gt__', other)

    def __lt__(self, other):
        return self._oper('__lt__', other)

    def __ge__(self, other):
        return self._oper('__ge__', other)

    def __le__(self, other):
        return self._oper('__le__', other)

    def __ne__(self, other):
        return self._oper('__ne__', other)

    def __eq__(self, other):
        return self._oper('__eq__', other)

    def _oper(self, op, other):
        """
        Generic operator function

        Parameters
        ----------
        op: str name of special method
        other: the other object being operated on

        Returns
        -------
        A DataFrame
        """
        pass

    def sort_values(self, by, asc=True):
        """
        Sort the DataFrame by one or more values

        Parameters
        ----------
        by: str or list of column names
        asc: boolean of sorting order

        Returns
        -------
        A DataFrame
        """
        pass

    def sample(self, n=None, frac=None, replace=False, seed=None):
        """
        Randomly samples rows the DataFrame

        Parameters
        ----------
        n: int
            number of rows to return
        frac: float
            Proportion of the data to sample
        replace: bool
            Whether or not to sample with replacement
        seed: int
            Seeds the random number generator

        Returns
        -------
        A DataFrame
        """
        pass

    def pivot_table(self, rows=None, columns=None, values=None, aggfunc=None):
        """
        Creates a pivot table from one or two 'grouping' columns.

        Parameters
        ----------
        rows: str of column name to group by
            Optional
        columns: str of column name to group by
            Optional
        values: str of column name to aggregate
            Required
        aggfunc: str of aggregation function

        Returns
        -------
        A DataFrame
        """
        pass

    def _add_docs(self):
        agg_names = ['min', 'max', 'mean', 'median', 'sum', 'var',
                     'std', 'any', 'all', 'argmax', 'argmin']
        agg_doc = \
        """
        Find the {} of each column
        
        Returns
        -------
        DataFrame
        """
        for name in agg_names:
            getattr(DataFrame, name).__doc__ = agg_doc.format(name)


class StringMethods:

    def __init__(self, df):
        self._df = df

    def capitalize(self, col):
        return self._str_method(str.capitalize, col)

    def center(self, col, width, fillchar=None):
        if fillchar is None:
            fillchar = ' '
        return self._str_method(str.center, col, width, fillchar)

    def count(self, col, sub, start=None, stop=None):
        return self._str_method(str.count, col, sub, start, stop)

    def endswith(self, col, suffix, start=None, stop=None):
        return self._str_method(str.endswith, col, suffix, start, stop)

    def startswith(self, col, suffix, start=None, stop=None):
        return self._str_method(str.startswith, col, suffix, start, stop)

    def find(self, col, sub, start=None, stop=None):
        return self._str_method(str.find, col, sub, start, stop)

    def len(self, col):
        return self._str_method(str.__len__, col)

    def get(self, col, item):
        return self._str_method(str.__getitem__, col, item)

    def index(self, col, sub, start=None, stop=None):
        return self._str_method(str.index, col, sub, start, stop)

    def isalnum(self, col):
        return self._str_method(str.isalnum, col)

    def isalpha(self, col):
        return self._str_method(str.isalpha, col)

    def isdecimal(self, col):
        return self._str_method(str.isdecimal, col)

    def islower(self, col):
        return self._str_method(str.islower, col)

    def isnumeric(self, col):
        return self._str_method(str.isnumeric, col)

    def isspace(self, col):
        return self._str_method(str.isspace, col)

    def istitle(self, col):
        return self._str_method(str.istitle, col)

    def isupper(self, col):
        return self._str_method(str.isupper, col)

    def lstrip(self, col, chars):
        return self._str_method(str.lstrip, col, chars)

    def rstrip(self, col, chars):
        return self._str_method(str.rstrip, col, chars)

    def strip(self, col, chars):
        return self._str_method(str.strip, col, chars)

    def replace(self, col, old, new, count=None):
        if count is None:
            count = -1
        return self._str_method(str.replace, col, old, new, count)

    def swapcase(self, col):
        return self._str_method(str.swapcase, col)

    def title(self, col):
        return self._str_method(str.title, col)

    def lower(self, col):
        return self._str_method(str.lower, col)

    def upper(self, col):
        return self._str_method(str.upper, col)

    def zfill(self, col, width):
        return self._str_method(str.zfill, col, width)

    def encode(self, col, encoding='utf-8', errors='strict'):
        return self._str_method(str.encode, col, encoding, errors)

    def _str_method(self, method, col, *args):
        pass


def read_csv(fn):
    """
    Read in a comma-separated value file as a DataFrame

    Parameters
    ----------
    fn: string of file location

    Returns
    -------
    A DataFrame
    """
    pass
