# csv tables for Foliant

This preprocessor converts csv data to markdown tables.


## Installation

```shell
$ pip install foliantcontrib.csvtables
```


## Config

To enable the preprocessor with default options, add `csvtables` to `preprocessors` section in the project config:

```yaml
preprocessors:
  - csvtables
```

The preprocessor has a number of options (default values stated below):

```yaml
preprocessors:
    - csvtables:
        delimiter: ';'
        padding_symbol: ' '
        paddings_number: 1
```

`delimiter`
:   Delimiter of csv data.

`padding_symbol`
:   Symbol combination that will be places around datum (reversed on the right side).

`paddings_number`
:   Symbol combination multiplier.


## Usage

You can place csv data in `csvtable` tag.

```
<csvtable>
    Header 1;Header 2;Header 3;Header 4;Header 5
    Datum 1;Datum 2;Datum 3;Datum 4;Datum 5
    Datum 6;Datum 7;Datum 8;Datum 9;Datum 10
</csvtable>
```

Or in external `file.csv`.

```
<csvtable src="table.csv"></csvtable>
```

You can reassign setting for certain csv tables.

```
<csvtable delimiter=":" padding_symbol=" *">
    Header 1:Header 2:Header 3:Header 4:Header 5
    Datum 1:Datum 2:Datum 3:Datum 4:Datum 5
    Datum 6:Datum 7:Datum 8:Datum 9:Datum 10
</csvtable>
```


## Example

`Usage` section will be converted to this:

You can place csv data in `csvtable` tag.

```
| Header 1 | Header 2 | Header 3 | Header 4 | Header 5 |
|----------|----------|----------|----------|----------|
| Datum 1  | Datum 2  | Datum 3  | Datum 4  | Datum 5  |
| Datum 6  | Datum 7  | Datum 8  | Datum 9  | Datum 10 |

```

Or in external `file.csv`.

```
| Header 1 | Header 2 | Header 3 | Header 4 | Header 5 |
|----------|----------|----------|----------|----------|
| Datum 1  | Datum 2  | Datum 3  | Datum 4  | Datum 5  |
| Datum 6  | Datum 7  | Datum 8  | Datum 9  | Datum 10 |

```

You can reassign setting for certain csv tables.

```
| *Header 1* | *Header 2* | *Header 3* | *Header 4* | *Header 5* |
|------------|------------|------------|------------|------------|
| *Datum 1*  | *Datum 2*  | *Datum 3*  | *Datum 4*  | *Datum 5*  |
| *Datum 6*  | *Datum 7*  | *Datum 8*  | *Datum 9*  | *Datum 10* |

```
