# tablat

A simple way to print output in a table

### Basic usage
Just create a `Table` object and give it a headers list and the data. The number of columns will be calculated from the number of headers.

### Installation
You can intall the package using [pip](https://pip.pypa.io/en/stable/) (Python Package Installer)
```sh
pip install tablat
```
or
```sh
python -m pip install tablat
```

### Code sample

#### Code
```py
from pathlib import Path
from tablat import Table

folder_path = Path('./')
header = ['FILE_NAME', 'FOLDER', 'FILES_IN']
data = []

for file_path in folder_path.iterdir():
    data.append(file_path.name)
    if file_path.is_dir():
        data.extend(['YES', len([f for f in file_path.iterdir()])])

    else:
        data.extend(['NO', 0])

my_table = Table(data, header)
my_table.print_table()
```

#### Output
<img src="/assets/tablat_output.png" alt="table_output">

#### Notes
You can retrieve data form the table using indices

```py
# Get first row data
my_table[0]

# Get third row, second column
my_table[2][1]
```
