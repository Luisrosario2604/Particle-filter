# Filtro de particulas

The goal here is to find the numbers touched from a thermal photo

## Goals

- Detect where are the numbers in the photo
- Detect what numbers where touched
- Detect the order of the numbers touched

## Explanation

#### We need two files to guess the numbers.

detection_digit_position.py :

* Reads the 9 images labelled with only 1 number (that's why we kept these images in the zip)
* Deducts the centre of each number
* The algorithm generates a .pkl file with the positions of the centres of each number (1 to 9)

We will use this file in a second algorithm to be able to detect which number has been touched (by the distance to the centre)

thermal_detection.py :

* Reads a given image
* Iterates with different thermal levels.
* Detects all "spots" of a given size range
* Each spot is associated with a number (relative to the centre of each), or deleted if there is no number centre at a distance x
* Check the number of each iteration for each number (keep only those with more than y iterations)
* Deduce the order by the disappearance of each spots

## Requirements

* Python 3.7+
* Requirements = Requirement.txt
```bash
$ pip install -r requirements.txt
```
###### flirimageextractor (1.4.0)
###### matplotlib (3.3.4)
###### numpy (1.21.3)
###### opencv_python (4.5.3.56)
###### Pillow (8.4.0)

## Usage

#### Detecting center's of each number (Generating a pickle file)

```bash
$ python detection_digit_position.py
```

#### Predict number touched of an thermal image

```bash
$ python thermal_detection.py --file=./CODIGOS_ETIQUETADOS/DIGITOS_020.jpg
```

#### (Bonus) See image used and thermal value

```bash
$ python manual_digit_reader.py --file=./CODIGOS_ETIQUETADOS/DIGITOS_001.jpg
```

## Example

![example](./Pictures/Screen.jpg)

## Authors

* **ROSARIO TREMOULET, LUIS** - *Initial work* - [Luis](https://github.com/Luisrosario2604)
