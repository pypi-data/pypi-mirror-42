# basictable
Small library to print structured data in tables

# License

MIT

# Installation

```bash
pip3 install basictable
```

# Data Format

The recordset format is a list of dictionaries where the dictionary keys are the column headings. All the
records are required to have the same number of columns and same heading values (keys)

```python
[
    {'Col1':data1, 'Col2': data2, 'Col3':data2, 'Col4':'data4'},
    {'Col1':data1, 'Col2': data2, 'Col3':data2, 'Col4':'data4'},
    {'Col1':data1, 'Col2': data2, 'Col3':data2, 'Col4':'data4'},
    {'Col1':data1, 'Col2': data2, 'Col3':data2, 'Col4':'data4'},
]
```
# Usage

```bash
>>> from basictable import print_table
>>> data = []
>>> for i in range(20):
...  data.append({'Col1':1, 'Col2': "test", 'Col3':'test test', 'Col4':'some longer string'})
...
>>> print_table(data)
    Col3               Col4            Col1     Col2
  ---------     ------------------     ----     ----
  test test     some longer string     1        test
  test test     some longer string     1        test
  test test     some longer string     1        test
  test test     some longer string     1        test
  test test     some longer string     1        test
  test test     some longer string     1        test
  test test     some longer string     1        test
  test test     some longer string     1        test
  test test     some longer string     1        test
  test test     some longer string     1        test
  test test     some longer string     1        test
  test test     some longer string     1        test
  test test     some longer string     1        test
  test test     some longer string     1        test
  test test     some longer string     1        test
  test test     some longer string     1        test
  test test     some longer string     1        test
  test test     some longer string     1        test
  test test     some longer string     1        test
  test test     some longer string     1        test
>>> print_table(data, border=True)
|------------------------------------------------------|
|    Col3     |         Col4         |  Col1  |  Col2  |
|-------------+----------------------+--------+--------|
|  test test  |  some longer string  |  1     |  test  |
|-------------+----------------------+--------+--------|
|  test test  |  some longer string  |  1     |  test  |
|-------------+----------------------+--------+--------|
|  test test  |  some longer string  |  1     |  test  |
|-------------+----------------------+--------+--------|
|  test test  |  some longer string  |  1     |  test  |
|-------------+----------------------+--------+--------|
|  test test  |  some longer string  |  1     |  test  |
|-------------+----------------------+--------+--------|
|  test test  |  some longer string  |  1     |  test  |
|-------------+----------------------+--------+--------|
|  test test  |  some longer string  |  1     |  test  |
|-------------+----------------------+--------+--------|
|  test test  |  some longer string  |  1     |  test  |
|-------------+----------------------+--------+--------|
|  test test  |  some longer string  |  1     |  test  |
|-------------+----------------------+--------+--------|
|  test test  |  some longer string  |  1     |  test  |
|-------------+----------------------+--------+--------|
|  test test  |  some longer string  |  1     |  test  |
|-------------+----------------------+--------+--------|
|  test test  |  some longer string  |  1     |  test  |
|-------------+----------------------+--------+--------|
|  test test  |  some longer string  |  1     |  test  |
|-------------+----------------------+--------+--------|
|  test test  |  some longer string  |  1     |  test  |
|-------------+----------------------+--------+--------|
|  test test  |  some longer string  |  1     |  test  |
|-------------+----------------------+--------+--------|
|  test test  |  some longer string  |  1     |  test  |
|-------------+----------------------+--------+--------|
|  test test  |  some longer string  |  1     |  test  |
|-------------+----------------------+--------+--------|
|  test test  |  some longer string  |  1     |  test  |
|-------------+----------------------+--------+--------|
|  test test  |  some longer string  |  1     |  test  |
|-------------+----------------------+--------+--------|
|  test test  |  some longer string  |  1     |  test  |
|------------------------------------------------------|
>>> print_table(data, headings_justify='left')
  Col3          Col4                   Col1     Col2
  ---------     ------------------     ----     ----
  test test     some longer string     1        test
  test test     some longer string     1        test
  test test     some longer string     1        test
  test test     some longer string     1        test
  test test     some longer string     1        test
  test test     some longer string     1        test
  test test     some longer string     1        test
  test test     some longer string     1        test
  test test     some longer string     1        test
  test test     some longer string     1        test
  test test     some longer string     1        test
  test test     some longer string     1        test
  test test     some longer string     1        test
  test test     some longer string     1        test
  test test     some longer string     1        test
  test test     some longer string     1        test
  test test     some longer string     1        test
  test test     some longer string     1        test
  test test     some longer string     1        test
  test test     some longer string     1        test
>>> print_table(data, headings_justify='left', order=('Col4','Col3','Col2','Col1'))
  Col4                   Col3          Col2     Col1
  ------------------     ---------     ----     ----
  some longer string     test test     test     1
  some longer string     test test     test     1
  some longer string     test test     test     1
  some longer string     test test     test     1
  some longer string     test test     test     1
  some longer string     test test     test     1
  some longer string     test test     test     1
  some longer string     test test     test     1
  some longer string     test test     test     1
  some longer string     test test     test     1
  some longer string     test test     test     1
  some longer string     test test     test     1
  some longer string     test test     test     1
  some longer string     test test     test     1
  some longer string     test test     test     1
  some longer string     test test     test     1
  some longer string     test test     test     1
  some longer string     test test     test     1
  some longer string     test test     test     1
  some longer string     test test     test     1
>>> print_table(data, data_justify='center', order=('Col1',))
  Col1     Col2            Col4              Col3
  ----     ----     ------------------     ---------
   1       test     some longer string     test test
   1       test     some longer string     test test
   1       test     some longer string     test test
   1       test     some longer string     test test
   1       test     some longer string     test test
   1       test     some longer string     test test
   1       test     some longer string     test test
   1       test     some longer string     test test
   1       test     some longer string     test test
   1       test     some longer string     test test
   1       test     some longer string     test test
   1       test     some longer string     test test
   1       test     some longer string     test test
   1       test     some longer string     test test
   1       test     some longer string     test test
   1       test     some longer string     test test
   1       test     some longer string     test test
   1       test     some longer string     test test
   1       test     some longer string     test test
   1       test     some longer string     test test
>>> print_table(data, data_justify='center', order=('Col1','Col2','Col3'))
  Col1     Col2       Col3               Col4
  ----     ----     ---------     ------------------
   1       test     test test     some longer string
   1       test     test test     some longer string
   1       test     test test     some longer string
   1       test     test test     some longer string
   1       test     test test     some longer string
   1       test     test test     some longer string
   1       test     test test     some longer string
   1       test     test test     some longer string
   1       test     test test     some longer string
   1       test     test test     some longer string
   1       test     test test     some longer string
   1       test     test test     some longer string
   1       test     test test     some longer string
   1       test     test test     some longer string
   1       test     test test     some longer string
   1       test     test test     some longer string
   1       test     test test     some longer string
   1       test     test test     some longer string
   1       test     test test     some longer string
   1       test     test test     some longer string
>>> print_table(data, data_justify='center', border=True, order=('Col1','Col2','Col3'))
|------------------------------------------------------|
|  Col1  |  Col2  |    Col3     |         Col4         |
|--------+--------+-------------+----------------------|
|   1    |  test  |  test test  |  some longer string  |
|--------+--------+-------------+----------------------|
|   1    |  test  |  test test  |  some longer string  |
|--------+--------+-------------+----------------------|
|   1    |  test  |  test test  |  some longer string  |
|--------+--------+-------------+----------------------|
|   1    |  test  |  test test  |  some longer string  |
|--------+--------+-------------+----------------------|
|   1    |  test  |  test test  |  some longer string  |
|--------+--------+-------------+----------------------|
|   1    |  test  |  test test  |  some longer string  |
|--------+--------+-------------+----------------------|
|   1    |  test  |  test test  |  some longer string  |
|--------+--------+-------------+----------------------|
|   1    |  test  |  test test  |  some longer string  |
|--------+--------+-------------+----------------------|
|   1    |  test  |  test test  |  some longer string  |
|--------+--------+-------------+----------------------|
|   1    |  test  |  test test  |  some longer string  |
|--------+--------+-------------+----------------------|
|   1    |  test  |  test test  |  some longer string  |
|--------+--------+-------------+----------------------|
|   1    |  test  |  test test  |  some longer string  |
|--------+--------+-------------+----------------------|
|   1    |  test  |  test test  |  some longer string  |
|--------+--------+-------------+----------------------|
|   1    |  test  |  test test  |  some longer string  |
|--------+--------+-------------+----------------------|
|   1    |  test  |  test test  |  some longer string  |
|--------+--------+-------------+----------------------|
|   1    |  test  |  test test  |  some longer string  |
|--------+--------+-------------+----------------------|
|   1    |  test  |  test test  |  some longer string  |
|--------+--------+-------------+----------------------|
|   1    |  test  |  test test  |  some longer string  |
|--------+--------+-------------+----------------------|
|   1    |  test  |  test test  |  some longer string  |
|--------+--------+-------------+----------------------|
|   1    |  test  |  test test  |  some longer string  |
|------------------------------------------------------|
>>> print_table(data, data_justify='center', border=True, order=('Col1','Col2','Col3'), padding=8)
|------------------------------------------------------------------------------------------------------|
|        Col1        |        Col2        |          Col3           |               Col4               |
|--------------------+--------------------+-------------------------+----------------------------------|
|         1          |        test        |        test test        |        some longer string        |
|--------------------+--------------------+-------------------------+----------------------------------|
|         1          |        test        |        test test        |        some longer string        |
|--------------------+--------------------+-------------------------+----------------------------------|
|         1          |        test        |        test test        |        some longer string        |
|--------------------+--------------------+-------------------------+----------------------------------|
|         1          |        test        |        test test        |        some longer string        |
|--------------------+--------------------+-------------------------+----------------------------------|
|         1          |        test        |        test test        |        some longer string        |
|--------------------+--------------------+-------------------------+----------------------------------|
|         1          |        test        |        test test        |        some longer string        |
|--------------------+--------------------+-------------------------+----------------------------------|
|         1          |        test        |        test test        |        some longer string        |
|--------------------+--------------------+-------------------------+----------------------------------|
|         1          |        test        |        test test        |        some longer string        |
|--------------------+--------------------+-------------------------+----------------------------------|
|         1          |        test        |        test test        |        some longer string        |
|--------------------+--------------------+-------------------------+----------------------------------|
|         1          |        test        |        test test        |        some longer string        |
|--------------------+--------------------+-------------------------+----------------------------------|
|         1          |        test        |        test test        |        some longer string        |
|--------------------+--------------------+-------------------------+----------------------------------|
|         1          |        test        |        test test        |        some longer string        |
|--------------------+--------------------+-------------------------+----------------------------------|
|         1          |        test        |        test test        |        some longer string        |
|--------------------+--------------------+-------------------------+----------------------------------|
|         1          |        test        |        test test        |        some longer string        |
|--------------------+--------------------+-------------------------+----------------------------------|
|         1          |        test        |        test test        |        some longer string        |
|--------------------+--------------------+-------------------------+----------------------------------|
|         1          |        test        |        test test        |        some longer string        |
|--------------------+--------------------+-------------------------+----------------------------------|
|         1          |        test        |        test test        |        some longer string        |
|--------------------+--------------------+-------------------------+----------------------------------|
|         1          |        test        |        test test        |        some longer string        |
|--------------------+--------------------+-------------------------+----------------------------------|
|         1          |        test        |        test test        |        some longer string        |
|--------------------+--------------------+-------------------------+----------------------------------|
|         1          |        test        |        test test        |        some longer string        |
|------------------------------------------------------------------------------------------------------|
>>> print_table(data, border=True, records_per_page=3)
|------------------------------------------------------|
|  Col1  |    Col3     |  Col2  |         Col4         |
|--------+-------------+--------+----------------------|
|  1     |  test test  |  test  |  some longer string  |
|--------+-------------+--------+----------------------|
|  1     |  test test  |  test  |  some longer string  |
|--------+-------------+--------+----------------------|
|  1     |  test test  |  test  |  some longer string  |
|--------+-------------+--------+----------------------|
[press any key]
|  1     |  test test  |  test  |  some longer string  |
|--------+-------------+--------+----------------------|
|  1     |  test test  |  test  |  some longer string  |
|--------+-------------+--------+----------------------|
|  1     |  test test  |  test  |  some longer string  |
|--------+-------------+--------+----------------------|
[press any key]
|  1     |  test test  |  test  |  some longer string  |
|--------+-------------+--------+----------------------|
|  1     |  test test  |  test  |  some longer string  |
|--------+-------------+--------+----------------------|
|  1     |  test test  |  test  |  some longer string  |
|--------+-------------+--------+----------------------|
[press any key]
|  1     |  test test  |  test  |  some longer string  |
|------------------------------------------------------|
```

