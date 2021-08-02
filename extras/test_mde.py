import numpy
import rasterio
import os

folder_path = '../img/ASTER-GDEM-BOLIVIA/DataV3'
files = os.listdir(folder_path)

data = rasterio.open(os.path.join(folder_path, files[0]))
# data = rasterio.open(os.path.join(folder_path, files[124]))

print(data.name)
print(data.mode)
print(data.closed)
print("##########Atributos")
print(data.count)
print(data.width)
print(data.height)
print({i: dtype for i, dtype in zip(data.indexes, data.dtypes)})
print("##########Georeferencia")
print(data.bounds)
print(data.transform)
print(data.transform * (0, 0))
print(data.transform * (data.width, data.height))
print(data.transform * (-67.00013888888888, -16.999861111111112))
print(data.crs)
print("##########Leyendo")
print(data.indexes)
band1 = data.read(1)
print(band1)
print(band1[data.height // 2, data.width // 2])
print("##########Indice espacial")
# x, y = (data.bounds.left + 1, data.bounds.top - 1)
# x, y = (-66.13488484712903, -17.3840218806585) # cristo
# x, y = (-66.31072900706361, -17.422539946086463) # calvario
x, y = (86.9249906082514, 27.988189989080908) # everest
print('Latitud: ', y, ' Longitud: ', x)
row, col = data.index(x, y)
print('Fila: ', row, ' Columna: ', col)
print('ALtura: ', band1[row, col])
# print('##########')
# print('Altura maxima: ', numpy.max(band1))
# print('Fila y columna maxima: ', (numpy.argmax(band1, axis=-1)))
# print('##########')
# print('Altura minima: ', numpy.min(band1))
# print('Fila y columna minima: ', numpy.argmin(band1))




