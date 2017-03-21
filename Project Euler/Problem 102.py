# Problem 102.py
# "Triangle containment"
#
# Result - 228
#
# Changelog:
# 03.01.2017 - Script created

from common import *

result = 0

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Triangle:
    def __init__(self, points):
        self.A = Point(int(points[0]), int(points[1]))
        self.B = Point(int(points[2]), int(points[3]))
        self.C = Point(int(points[4]), int(points[5]))

def is_same_side(A, B, Z):
    if A.x != B.x:
        a = (A.y - B.y) / (A.x - B.x)
        b = A.y - a * A.x
        y_temp = a * Z.x + b
        return (y_temp - Z.y) * b > 0
    else:
        return A.x * (A.x - Z.x) > 0

def includes_origin(t):
    return is_same_side(t.A, t.B, t.C) and is_same_side(t.A, t.C, t.B) and is_same_side(t.C, t.B, t.A)

triangles = []
origin = Point(0, 0)

with open("p102_triangles.txt") as f:
    for line in f:
        triangles.append(Triangle(line.split(",")))

for i, triangle in enumerate(triangles):
    if includes_origin(triangle):
        result += 1

print("Result =", result)
