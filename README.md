# midata2csv
Converts midata to a CSV format acceptable to the HomeBank software. Current version has some basic automatic detection of (UK) companies and automatic cateogorisation (e.g. cash machine withdrawal, supermarkets).

## Requirements
* python
* midata file downloaded from your bank

## Usage
```
$ python midata2csv.py [-b] <input.csv> <output.csv>
	-b		Use initial balance as transfer
	input.csv	MiData formatted file
	output.csv	Homebank CSV formatted file
```

## Tested with
* Halifax (UK)

## Limitations
* Only tested with Halfiax data so far
* Some transactions details are not included by the bank, so will have to be manually editted; these typically are starred out (*****)
* Auto detection of certain transactions is hardcoded (see get_category_and_tags function)

## TODO
Move autodetection from code to data file?
