import numpy

cores = [
    ["Azul", numpy.array([100, 150, 30]), numpy.array([130, 255, 255])],
    ["Amarelo", numpy.array([15, 100, 80]), numpy.array([30, 255, 255])],
    ["Vermelho", numpy.array([0, 60, 55]), numpy.array([3, 255, 255])],
    ["Verde", numpy.array([50, 90, 30]), numpy.array([80, 255, 255])]
]

color = 20
print  cores[2][2][0]
print range(cores[2][1][0], cores[2][2][0])

for i in range(0, len(cores), 1):
    if color in range(cores[i][1][0], cores[i][2][0]+1):
        print cores[i][0]