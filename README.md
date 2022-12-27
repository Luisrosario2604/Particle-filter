# Particle filter

Visual tracking with particle filter method

## Steps

1) Initial considerations
2) Initialisation
3) Evaluation
4) Estimation
5) Selection
6) Diffusion
7) Prediction


## Requirements

* Python 3.7+
* Requirements = Requirement.txt

```bash
$ pip install -r requirements.txt
```
###### numpy (1.21.3)
###### opencv_python (4.5.5.64)

## Usage

######Press a key to skip image

#### With static perturbation
```bash
$ python main_filter.py --directory="data"
```

#### With proportional perturbation
```bash
$ python main_filter.py --directory="data" -p
```

## Example

![example](./Pictures/Screen.png)

## Authors

* **ROSARIO TREMOULET, LUIS** - *Initial work* - [Luis](https://github.com/Luisrosario2604)
