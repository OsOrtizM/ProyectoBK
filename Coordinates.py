import numpy as np
import rasterio
import os
from numpy.lib import math

folder_path = 'img/ASTER-GDEM-BOLIVIA/DataV3'
files = os.listdir(folder_path)


def getTexture(coor):
    coor = coor[11:-4]
    llano = [
        'S10W067', 'S10W066', 'S11W070', 'S11W069', 'S11W068', 'S11W067', 'S11W066', 'S12W070', 'S12W069',
        'S12W068',
        'S12W067', 'S12W066', 'S12W065', 'S13W067', 'S13W066', 'S13W065', 'S13W064', 'S13W063', 'S14W067',
        'S14W066',
        'S14W065', 'S14W064', 'S14W063', 'S14W062', 'S14W061', 'S15W067', 'S15W066', 'S15W065', 'S15W064',
        'S15W063',
        'S15W062', 'S15W061', 'S16W067', 'S16W066', 'S16W065', 'S16W064', 'S16W063', 'S16W062', 'S16W061',
        'S17W065',
        'S17W064', 'S17W063', 'S17W062', 'S17W061', 'S17W060', 'S17W059', 'S18W064', 'S18W063', 'S18W062',
        'S18W061',
        'S18W060', 'S18W059', 'S18W058', 'S19W064', 'S19W063', 'S19W062', 'S19W061', 'S19W060', 'S19W059',
        'S19W058',
        'S20W064', 'S20W063', 'S20W062', 'S20W061', 'S20W060', 'S20W059', 'S20W058', 'S21W062', 'S21W059', 'S21W058'
    ]
    valle = [
        'S17W067', 'S17W066', 'S18W067', 'S18W066', 'S18W065', 'S19W066', 'S19W065', 'S20W065',
        'S21W065', 'S21W064', 'S22W065', 'S22W064', 'S22W063', 'S23W065', 'S23W064', 'S23W063'
    ]
    altiplano = [
        'S13W069', 'S13W068', 'S14W070', 'S14W069', 'S14W068', 'S15W070', 'S15W069', 'S15W068', 'S16W070',
        'S16W069',
        'S16W068', 'S17W070', 'S17W069', 'S17W068', 'S18W070', 'S18W069', 'S18W068', 'S19W070', 'S19W069',
        'S19W068',
        'S19W067', 'S20W069', 'S20W068', 'S20W067', 'S20W066', 'S21W069', 'S21W068', 'S21W067', 'S21W066',
        'S22W069',
        'S22W068', 'S22W067', 'S22W066', 'S23W069', 'S23W068', 'S23W067', 'S23W066'
    ]
    if coor in llano:
        return 'Llano'
    elif coor in altiplano:
        return 'Altiplano'
    elif coor in valle:
        return 'Valle'


def latLon2AltCell(lat, lon):
    for i, f in enumerate(files):
        dataset = rasterio.open(os.path.join(folder_path, f))
        vals = dataset.sample([(lon, lat)])
        for val in vals:
            if val[0] <= 0:
                pass
            else:
                return val[0], files[i]
    return 0


def latLonCell2XY(lat, lon, cell):
    data = rasterio.open(os.path.join(folder_path, cell))
    xy = data.index(lon, lat)
    return xy


def XYtiff2XYrender(x_tiff, y_tiff):
    resTiff = 3601
    resRender = 4096
    x_render = (x_tiff * resRender) / resTiff
    y_render = (y_tiff * resRender) / resTiff
    return x_render, y_render


def altitude2Z(alt):
    # return float(alt * 69.8 / 2580)
    return float(alt * 69.02 / 2580)


# CODIGO DEL MODELO DE CLAROS ADAPTADO
azimutResult = 0
azimutPlataforma = 110.0


def getDistanceFromLatLon(lat1, lon1, lat2, lon2):
    sm_a = 6371009.0
    R = sm_a
    φ1 = np.deg2rad(lat1)
    φ2 = np.deg2rad(lat2)
    Δφ = np.deg2rad(lat2 - lat1)
    Δλ = np.deg2rad(lon2 - lon1)

    a = math.sin(Δφ / 2) * math.sin(Δφ / 2) + math.cos(φ1) * math.cos(φ2) * math.sin(Δλ / 2) * math.sin(Δλ / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c
    return d


def calculateAzimut(lat1, lon1, lat2, lon2):
    φ1 = np.deg2rad(lat1)
    φ2 = np.deg2rad(lat2)
    Δλ = np.deg2rad(lon2 - lon1)
    y = math.sin(Δλ) * math.cos(φ2)
    x = math.cos(φ1) * math.sin(φ2) - math.sin(φ1) * math.cos(φ2) * math.cos(Δλ)
    θ = math.atan2(y, x)
    return (np.rad2deg(θ) + 360) % 360


def mapeo(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def pointRadialDistanceV2(lat1, lon1, distance, azimut):
    sm_a = 6371009.0
    pi = math.pi
    earthRadius = sm_a
    epsilon = 0.000001
    rlat1 = np.deg2rad(lat1)
    rlon1 = np.deg2rad(lon1)
    razimut = np.deg2rad(mapeo(azimut, 0, 360, 360, 0))
    rdistance = distance / earthRadius
    rlat = math.asin(math.sin(rlat1) * math.cos(rdistance) + math.cos(rlat1) * math.sin(rdistance) * math.cos(razimut))
    rlon = 0
    if math.cos(rlat) == 0 or abs(math.cos(rlat)) < epsilon:
        rlon = rlon1
    else:
        rlon = ((rlon1 - math.asin(math.sin(razimut) * math.sin(rdistance) / math.cos(rlat)) + pi) % (2 * pi)) - pi
    res = dict()
    res['lat'] = np.rad2deg(rlat)
    res['lon'] = np.rad2deg(rlon)
    return res


def getPoints(latPlataforma, lonPlataforma, latObjetivo, lonObjetivo, maxPoints, azimutPlat):
    azimutPlataforma = azimutPlat
    distance = getDistanceFromLatLon(latPlataforma, lonPlataforma, latObjetivo, lonObjetivo)
    az = calculateAzimut(latPlataforma, lonPlataforma, latObjetivo, lonObjetivo)
    razon = distance / maxPoints
    res = []
    labelsDistancias = []
    for i in range(0, (maxPoints + 1)):
        point = pointRadialDistanceV2(latPlataforma, lonPlataforma, razon * i, az)
        labelsDistancias.append(str(round(razon * i / 1000 * 100) / 100) + ' Km')
        res.append(point['lon'])
        res.append(point['lat'])
    if 0 < azimutPlataforma <= 110:
        if az >= azimutPlataforma + 110:
            az = az - 360
    if 250 < azimutPlataforma <= 360:
        if az <= azimutPlataforma - 110:
            az = 360 + az
    azimutResult = float(format(az - azimutPlataforma, ".2f"))
    if abs(azimutResult) > 110:
        print('#########ERROR#########')
        print('El objetivo esta fuera de alcance')
        res = False
    return res, labelsDistancias, azimutResult


def getAngle(x, y, vi, gravity):
    comun = gravity * (x ** 2) / (1.0 * (2 * (vi ** 2)))
    a = comun
    b = x
    c = (comun + y)
    internalRaiz = b ** 2 - 4 * a * c
    if internalRaiz < 0:
        return None, None
    x1 = (-b + np.sqrt(internalRaiz)) / (2 * a)
    x2 = (-b - np.sqrt(internalRaiz)) / (2 * a)
    x1 = -np.degrees(np.arctan(x1))
    x2 = -np.degrees(np.arctan(x2))
    return x1, x2


def gravityCalculate(msnm):
    re = 6371009.0
    gravity = 9.80665 * (re / (re + msnm)) ** 2
    return gravity


def getMaxAltura(vi, angle, gravity):
    return 1.0 * (vi ** 2 * np.sin(np.deg2rad(angle)) ** 2) / (2 * gravity)


def getElevations(coords):
    res = []
    for c in coords:
        res.append(int(getElevation(c)))
    return res


def getElevation(coord):
    for f in files:
        dataset = rasterio.open(os.path.join(folder_path, f))
        vals = dataset.sample([coord])
        for val in vals:
            if val[0] <= 0:
                pass
            else:
                return val[0]
    return 0


def launch(distances, elevations):
    print('launch aerodinamic')
    vi = 355
    g = gravityCalculate(elevations[0])
    posObjetive = -1
    xPlattform = distances[0]
    yPlattform = elevations[0]
    xOjetive = distances[posObjetive] - xPlattform
    yObjetive = elevations[posObjetive] - yPlattform
    angle = getAngle(xOjetive, yObjetive, vi, g)
    while angle[0] is None:
        posObjetive -= 1
        xOjetive = distances[posObjetive] - xPlattform
        yObjetive = elevations[posObjetive] - yPlattform
        angle = getAngle(xOjetive, yObjetive, vi, g)
    return [angle[0], getMaxAltura(vi, angle[0], g) + yPlattform, xOjetive, vi]


def getElevationsRoute(coordinates, distances, azimut):
    distances = distances.split(',')
    dists = []
    for i in distances:
        dists.append(float(i[:-3]) * 1000)
    coordsInput = coordinates[1:-1].split(',')
    coords = []
    for i in range(0, len(coordsInput), 2):
        coords.append((float(coordsInput[i]), float(coordsInput[i + 1])))
    res = getElevations(coords)
    launchData = launch(dists, res)
    return dict({
        'coords': coords,
        'elevations': res,
        'distances': dists,
        'elevationPlatform': launchData[0],
        'maxAltitude': launchData[1],
        'maxDistance': launchData[2],
        'azimut': azimut,
        'vInicial': launchData[3]
    })


def pointsInter(dists, theta, grav, vIni, pos, altPlat, coords):
    pointsTrajectory = []  # (latitud, longitud, m.s.n.m)
    pointsTrajectory2 = []  # (distance, altura)
    for i, d in enumerate(dists):
        if d <= dists[pos]:
            y = (d * math.tan(np.deg2rad(theta))) - (grav * (d ** 2)) / \
                (2 * (vIni ** 2) * (math.cos(np.deg2rad(theta)) ** 2))
            pointsTrajectory.append((coords[i][0], coords[i][1], y + altPlat))
            pointsTrajectory2.append((d, y + altPlat))
    return pointsTrajectory, pointsTrajectory2


def calcular(latPlatform, lonPlatform, latObjetive, lonObjetive, maxPoints, azimutPlat):
    direcciones, labelsDistancias, azimut = getPoints(latPlatform, lonPlatform, latObjetive, lonObjetive,
                                                      maxPoints, azimutPlat)
    if direcciones:
        dir = getElevationsRoute(str(direcciones), str(','.join(labelsDistancias)), azimut)
        dir['labelsDistancias'] = labelsDistancias
        posLabel = -1
        for item in dir['distances']:
            if float(item) < dir['maxDistance']:
                posLabel += 1
        posLabel += 1
        if posLabel > len(dir['labelsDistancias']) - 1:
            posLabel = len(dir['labelsDistancias']) - 1
        subidaLenght = math.floor(posLabel * 0.8) + 1
        listPointsLatLonMsnm, listPointsDistAlt = pointsInter(dists=dir['distances'], theta=dir['elevationPlatform'],
                                                              grav=gravityCalculate(dir['elevations'][0]),
                                                              vIni=dir['vInicial'],
                                                              pos=posLabel, altPlat=dir['elevations'][0],
                                                              coords=dir['coords'])
        dir['lonlatmaxAltitude'] = dir['coords'][subidaLenght]
        dir['lonlatImpact'] = dir['coords'][posLabel]
        dir['altitudeImpact'] = dir['elevations'][posLabel]
        dir['lonlatPlatform'] = (lonPlatform, latPlatform)
        dir['altitudePlatform'] = dir['elevations'][0]
        dir['listPointsLatLonMsnm'] = listPointsLatLonMsnm
        dir['listPointsDistAlt'] = listPointsDistAlt
    return dir


def latlonAlt2XYZ(latlonalt):
    _, cell = latLon2AltCell(lon=latlonalt[0], lat=latlonalt[1])
    x_tiff, y_tiff = latLonCell2XY(lat=latlonalt[1], lon=latlonalt[0], cell=cell)
    x, y = XYtiff2XYrender(x_tiff=x_tiff, y_tiff=y_tiff)
    z = altitude2Z(latlonalt[2])
    return x, y, z


def getTrajectory(latPlatform, lonPlatform, latObjetive, lonObjetive, maxPoints, azimutPlat):
    data = calcular(latPlatform, lonPlatform, latObjetive, lonObjetive, maxPoints, azimutPlat)

    # TRAYECTORIA SOLO CON 3 PUNTOS
    # Platform
    # lonPlatform, latPlatform = data['lonlatPlatform']
    # altitudePlatform, cellPlatform = latLon2AltCell(lon=lonPlatform, lat=latPlatform)
    # x_tiff_Plat, y_tiff_Plat = latLonCell2XY(lat=latPlatform, lon=lonPlatform, cell=cellPlatform)
    # x_render_Plat, y_render_Plat = XYtiff2XYrender(x_tiff=x_tiff_Plat, y_tiff=y_tiff_Plat)
    # z_render_Plat = altitude2Z(altitudePlatform)
    #
    # #  Objetive
    # lonObjetive, latObjetive = data['lonlatImpact']
    #
    # altitudeObj, cellObj = latLon2AltCell(lon=lonObjetive, lat=latObjetive)
    # x_tiff_Obj, y_tiff_Obj = latLonCell2XY(lat=latObjetive, lon=lonObjetive, cell=cellObj)
    # x_render_Obj, y_render_Obj = XYtiff2XYrender(x_tiff=x_tiff_Obj, y_tiff=y_tiff_Obj)
    # z_render_Obj = altitude2Z(data['altitudeImpact'])
    #
    # #  ptAltitudeMaximum
    # lonMaxAltitude, latMaxAltitude = data['lonlatmaxAltitude']
    # altitudeMaxAltitude, cellMaxAltitude = latLon2AltCell(lon=lonMaxAltitude, lat=latMaxAltitude)
    # x_tiff_MaxAltitude, y_tiff_MaxAltitude = latLonCell2XY(lat=latMaxAltitude,
    #                                                          lon=lonMaxAltitude, cell=cellMaxAltitude)
    # x_render_MaxAltitude, y_render_MaxAltitude = XYtiff2XYrender(x_tiff=x_tiff_MaxAltitude, y_tiff=y_tiff_MaxAltitude)
    # z_render_MaxAltitude = altitude2Z(data['maxAltitude'])
    # points = [
    #     (x_render_Plat, y_render_Plat, z_render_Plat),
    #     (x_render_MaxAltitude, y_render_MaxAltitude, z_render_MaxAltitude),
    #     (x_render_Obj, y_render_Obj, z_render_Obj)
    # ]

    points = []
    for pt in data['listPointsLatLonMsnm']:
        points.append(latlonAlt2XYZ(pt))

    return points, data['listPointsLatLonMsnm'], data['listPointsDistAlt'], data['distances'], data['elevations']
