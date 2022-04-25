#!/usr/bin/python3

# Importing python3 from local, just use "python3 <binary>" if is not the same location

# Imports

# Function declarations
class Particle:

    def __init__(self, x, y, w, h, id):
        self.__x = x
        self.__y = y
        self.__w = w
        self.__h = h
        self.__score = 0
        self.__chosen = False
        self.__id = id

    def get_coords(self):
        return self.__x, self.__y, self.__w, self.__h

    def get_score(self):
        return self.__score

    def get_chosen(self):
        return self.__chosen

    def get_id(self):
        return self.__id

    def set_score(self, score):
        self.__score = score

    def set_chosen(self, bool):
        self.__chosen = bool
