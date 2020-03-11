# Clockifi Bulk Add
- add multiple work record to clockifi by csv
- more detail about clockifi https://clockify.me/

## Feature
- only work with google login
- pre formated clockifi template need to update with original data (clocki.csv)

## Pre Requirement's
- python 3.*

## How to install
- setup virtualenvirement
```bash
$ python -m venv ./venv
$ . venv/bin/activate
$ pip install -r requirement.txt
```
- run script 
```bash
$ python clockifi_update.py -u 'username@gmail.com' -p 'password' -f 'clocki.csv'
```

## Importent Point
- maximize your google chrome screen which is open by script for proper oupt put

## Contribute
- feel free to contribue

## License

The MIT License (MIT)

Copyright (c) 2020-2020 

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
