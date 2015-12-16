# Random-Table-Roller
A graphical application for rolling against custom random event tables. Meant for use with tabletop RPGs such as Dungeons and Dragons.

## To-do
- [x] Read tables from CSV files
- [x] Roll against tables generated from CSV files
- [x] Graphical user interface
- [x] Load multiple tables
- [x] Usage
- [ ] Windows executable
- [ ] Command line interface

## Installation

The standalone app and source code can be downloaded on the
[Releases](https://github.com/whonut/Random-Table-Roller/releases/) page. It is
possible to build the app from source yourself using [py2app](https://pythonhosted.org/py2app/).
(It might be possible to build a Windows executable with [py2exe](https://pypi.python.org/pypi/py2exe/),
I haven't tried).

## Usage

### Interface 

The standalone app can be opened as any other. Table files can be loaded by pressing
the "Load tables..." button. A table can then be selected from the dropdown. Pressing
the roll button will simulate a roll against the selected table and the resulting event
description will be shown in the centre of the window.

### Table file format

Table files are two-column CSV files. The first row is meant to be used for headers
describing each column, must start with a `%` and will be ignored.The first column of
all other rows specifies a roll (number) or range of rolls, whilst the second column
specifies the event associated with that roll.Roll ranges are specified with dashes.
For example, '3-5' means "a roll of 3, 4 or 5".

Every roll between the maximum and minimum present in the file must have an
associated event. Roll ranges cannot overlap and no roll can be associated with
more than one event. Event descriptions containing commas must be wrapped in
double quotes, `"`.

The contents of an example table file, `Example CSVs/Criminal - Personality Traits.csv`, are given below.

````
%d8,Personality Trait
1,I always have a plan for what to do when things go wrong.
2,"I am always calm, no matter what the situation. I never raise my voice or let my emotions control me."
3,The first thing I do in a new place is note the locations of everything valuable - or where such things could be hidden.
4,I would rather make a new friend than a new enemy.
5,I am incredibly slow to trust. Those who seem the fairest often have the most to hide.
6,I don't pay attention to the risks in a situation. Never tell me the odds.
7,The best way to get me to do something is to tell me I can't do it.
8,I blow up at the slightest insult.
````

## Credits
- Icon by [iconcubic](http://iconcubic.deviantart.com/).
