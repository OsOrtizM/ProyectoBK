import numpy as np
import rasterio
import os

from numpy.lib import math

folder_path = 'img/ASTER-GDEM-BOLIVIA/DataV3'
files = os.listdir(folder_path)


def getTexture(coor):
    # print(coor)
    coor = coor[11:-4]
    # print(coor)
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


# print(files)
# coord_test = (-67.01875003858024, -18.00013888888889)
# -17.383747, -66.157075 emi
# -17.384667, -66.134642 cristo

# left=-67.00013888888888, bottom=-18.00013888888889,
# right=-65.9998611111111, top=-16.999861111111112)
# izq-sup (-67.00013888888888, -16.999861111111112)
# der-sup (-65.9998611111111, -16.999861111111112)
# izq-inf (-67.00013888888888, -18.00013888888889)
# der-inf (-65.9998611111111, -18.00013888888889)
# 106.3957 km horizontal
# 111.2572 km vertical

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


#
# alt, ind = latLon2AltCell(coord_test)
# print(alt)
# # cell = files[ind][:-4]
# cell = files[ind]
# print(cell)

def latLonCell2XY(lat, lon, cell):
    data = rasterio.open(os.path.join(folder_path, cell))
    xy = data.index(lon, lat)
    return xy


# _x, _y = latLonCell2XY(coord_test[0], coord_test[1], cell)
# print(_x, _y)

def XYtiff2XYrender(x_tiff, y_tiff):
    resTiff = 3601
    resRender = 4096
    x_render = (x_tiff * resRender) / resTiff
    y_render = (y_tiff * resRender) / resTiff
    return x_render, y_render


# _x, _y = XYtiff2XYrender(_x, _y)
# print(_x, _y)

def altitude2Z(alt):
    # return float(alt * 69.8 / 2580)
    return float(alt * 69.02 / 2580)


# def trajectory(x_ini, y_ini, z_ini, x_end, y_end, z_end):
#     return 0


# CODIGO DEL MODELO DE CLAROS ADAPTADO
azimutResult = 0
azimutPlataforma = 110.0;


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


# print(getDistanceFromLatLon(-17.4230747459968, -66.14858610342263, -17.440414712192965, -66.15073899253551))


def calculateAzimut(lat1, lon1, lat2, lon2):
    φ1 = np.deg2rad(lat1)
    φ2 = np.deg2rad(lat2)
    Δλ = np.deg2rad(lon2 - lon1)
    y = math.sin(Δλ) * math.cos(φ2)
    x = math.cos(φ1) * math.sin(φ2) - math.sin(φ1) * math.cos(φ2) * math.cos(Δλ)
    θ = math.atan2(y, x)

    return (np.rad2deg(θ) + 360) % 360


# print(calculateAzimut(-17.4230747459968, -66.14858610342263, -17.440414712192965, -66.15073899253551))


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
        rlon = rlon1;
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
    # return res
    # print(az)
    # print(azimutPlataforma)
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


# print(getPoints(-17.4230747459968, -66.14858610342263, -17.473181809423522, -66.13085125740082))


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
    # print(distances)
    # print(elevations)
    vi = 355
    g = gravityCalculate(elevations[0])
    posObjetive = -1
    xPlattform = distances[0]
    yPlattform = elevations[0]
    xOjetive = distances[posObjetive] - xPlattform
    yObjetive = elevations[posObjetive] - yPlattform
    # print(xPlattform, yPlattform, xOjetive, yObjetive)
    # print('getAngle: ', xOjetive, yObjetive, vi, g)
    angle = getAngle(xOjetive, yObjetive, vi, g)
    while angle[0] is None:
        posObjetive -= 1
        xOjetive = distances[posObjetive] - xPlattform
        yObjetive = elevations[posObjetive] - yPlattform
        angle = getAngle(xOjetive, yObjetive, vi, g)
        # print(angle)
    # time.sleep(random.randint(7, 14))
    return [angle[0], getMaxAltura(vi, angle[0], g) + yPlattform, xOjetive, vi]


def getElevationsRoute(coordinates, distances, azimut):
    distances = distances.split(',')
    # print(distances)
    dists = []
    for i in distances:
        dists.append(float(i[:-3]) * 1000)
    # print(dists)
    # print('coordinates',coordinates[1:-1])
    coordsInput = coordinates[1:-1].split(',')
    # print('coordinatesinput',coordsInput)
    coords = []
    for i in range(0, len(coordsInput), 2):
        coords.append((float(coordsInput[i]), float(coordsInput[i + 1])))
    # print(coords)
    res = getElevations(coords)
    # print(res)
    launchData = launch(dists, res)
    # print(launchData)
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
    pointsTrajectory = []   # (latitud, longitud, m.s.n.m)
    pointsTrajectory2 = []  # (distance, altura)
    for i, d in enumerate(dists):
        if d <= dists[pos]:
            y = (d * math.tan(np.deg2rad(theta))) - (grav * (d ** 2)) / (
                    2 * (vIni ** 2) * (math.cos(np.deg2rad(theta)) ** 2))

            pointsTrajectory.append((coords[i][0], coords[i][1], y + altPlat))
            pointsTrajectory2.append((d, y+ altPlat))
    return pointsTrajectory, pointsTrajectory2


# dis=[0.0, 770.0, 1530.0, 2300.0, 3060.0, 3830.0, 4590.0, 5360.0, 6120.0, 6890.0, 7650.0, 8420.0, 9180.0, 9950.0, 10710.0, 11480.0, 12240.0, 13010.0, 13780.0, 14540.0, 15310.0, 16070.0, 16840.0, 17600.0, 18370.0, 19130.0, 19900.0, 20660.0, 21430.0, 22190.0, 22960.0]
# cor = [(-66.15700687603821, -17.383694116678157), (-66.15334777184026, -17.389624810058258), (-66.14968843039776, -17.395555436785795), (-66.14602885161186, -17.401485996832243), (-66.14236903538374, -17.40741649016909), (-66.13870898161453, -17.413346916767814), (-66.13504869020534, -17.419277276599864), (-66.13138816105727, -17.425207569636715), (-66.12772739407141, -17.431137795849818), (-66.12406638914881, -17.437067955210615), (-66.1204051461905, -17.44299804769056), (-66.11674366509754, -17.44892807326108), (-66.11308194577089, -17.454858031893604), (-66.10941998811155, -17.460787923559554), (-66.10575779202051, -17.466717748230355), (-66.10209535739867, -17.47264750587741), (-66.098432684147, -17.478577196472123), (-66.0947697721664, -17.4845068199859), (-66.09110662135774, -17.49043637639012), (-66.08744323162192, -17.496365865656177), (-66.08377960285976, -17.502295287755448), (-66.08011573497214, -17.508224642659307), (-66.07645162785983, -17.51415393033912), (-66.07278728142364, -17.520083150766244), (-66.06912269556436, -17.526012303912033), (-66.06545787018274, -17.531941389747843), (-66.06179280517951, -17.537870408245006), (-66.0581275004554, -17.543799359374862), (-66.0544619559111, -17.54972824310874), (-66.05079617144732, -17.555657059417957), (-66.04713014696468, -17.561585808273836)]
# print('p: ',pointsInter(dis, 38.04074191677854, 9.798712231780858, 355, 16, 2580, cor))

def calcular(latPlatform, lonPlatform, latObjetive, lonObjetive, maxPoints, azimutPlat):
    direcciones, labelsDistancias, azimut = getPoints(latPlatform, lonPlatform, latObjetive, lonObjetive, maxPoints,
                                                      azimutPlat)
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
                                 grav=gravityCalculate(dir['elevations'][0]), vIni=dir['vInicial'],
                                 pos=posLabel, altPlat=dir['elevations'][0], coords=dir['coords'])
        # print(subidaLenght)
        dir['lonlatmaxAltitude'] = dir['coords'][subidaLenght]
        dir['lonlatImpact'] = dir['coords'][posLabel]
        dir['altitudeImpact'] = dir['elevations'][posLabel]
        dir['lonlatPlatform'] = (lonPlatform, latPlatform)
        dir['altitudePlatform'] = dir['elevations'][0]
        dir['listPointsLatLonMsnm'] = listPointsLatLonMsnm
        dir['listPointsDistAlt'] = listPointsDistAlt
        # dir['elevations'] = dir['elevations'][:posLabel+1]

        # print(listPoints[subidaLenght])
        # print(dir['lonlatmaxAltitude'], dir['maxAltitude'])

    return dir
    #         graphicDates(data);
    #         var elevationResult=data['launch'][0].toFixed(2);


# trajectory = calcular(lonPlatform=-66.15700687603821, latPlatform=-17.383694116678157,
#                       #                       # lonObjetive=-66.13486064219316, latObjetive=-17.38395447862384)
#                       lonObjetive=-66.04713014696468, latObjetive=-17.561585808273836)


#
# print(trajectory['listPoints'])
# print(trajectory['coords'])

# print(trajectory['maxAltitude'])
# print(trajectory['maxDistance'])
# print(trajectory['labelsDistancias'])
# print(trajectory['distances'])
# print(trajectory['distances'][subidaLenght])
# print(trajectory['coords'][subidaLenght])
# print(trajectory['distances'][posLabel])
# print(trajectory['coords'][posLabel])
# print(getDistanceFromLatLon(-17.478577196472123, -66.098432684147, -17.383694116678157, -66.15700687603821))

# aousfghbpaeuievnñaowuiefpuasnbcvñoaushnfaosncoasinfñ

def latlonAlt2XYZ(latlonalt):
    _, cell = latLon2AltCell(lon=latlonalt[0], lat=latlonalt[1])
    x_tiff, y_tiff = latLonCell2XY(lat=latlonalt[1], lon=latlonalt[0], cell=cell)
    x, y = XYtiff2XYrender(x_tiff=x_tiff, y_tiff=y_tiff)
    z = altitude2Z(latlonalt[2])
    return x, y, z


def getTrajectory(latPlatform, lonPlatform, latObjetive, lonObjetive, maxPoints, azimutPlat):
    data = calcular(latPlatform, lonPlatform, latObjetive, lonObjetive, maxPoints, azimutPlat)
    # Platform
    # lonPlatform, latPlatform = data['lonlatPlatform']
    # altitudePlatform, cellPlatform = latLon2AltCell(lon=lonPlatform, lat=latPlatform)
    # x_tiff_Plat, y_tiff_Plat = latLonCell2XY(lat=latPlatform, lon=lonPlatform, cell=cellPlatform)
    # x_render_Plat, y_render_Plat = XYtiff2XYrender(x_tiff=x_tiff_Plat, y_tiff=y_tiff_Plat)
    # z_render_Plat = altitude2Z(altitudePlatform)
    #
    # #  Objetive     Revisar lat y lon, alcance maximo
    # lonObjetive, latObjetive = data['lonlatImpact']
    #
    # altitudeObj, cellObj = latLon2AltCell(lon=lonObjetive, lat=latObjetive)
    # x_tiff_Obj, y_tiff_Obj = latLonCell2XY(lat=latObjetive, lon=lonObjetive, cell=cellObj)
    # x_render_Obj, y_render_Obj = XYtiff2XYrender(x_tiff=x_tiff_Obj, y_tiff=y_tiff_Obj)
    # z_render_Obj = altitude2Z(data['altitudeImpact'])
    #
    # #  ptAltitudeMaximum     Revisar lat y lon, alcance maximo
    # lonMaxAltitude, latMaxAltitude = data['lonlatmaxAltitude']
    # altitudeMaxAltitude, cellMaxAltitude = latLon2AltCell(lon=lonMaxAltitude, lat=latMaxAltitude)
    # x_tiff_MaxAltitude, y_tiff_MaxAltitude = latLonCell2XY(lat=latMaxAltitude, lon=lonMaxAltitude, cell=cellMaxAltitude)
    # x_render_MaxAltitude, y_render_MaxAltitude = XYtiff2XYrender(x_tiff=x_tiff_MaxAltitude, y_tiff=y_tiff_MaxAltitude)
    # z_render_MaxAltitude = altitude2Z(data['maxAltitude'])

    # points = [
    #     (x_render_Plat, y_render_Plat, z_render_Plat),
    #     (x_render_MaxAltitude, y_render_MaxAltitude, z_render_MaxAltitude),
    #     (x_render_Obj, y_render_Obj, z_render_Obj)
    # ]
    points = []
    for pt in data['listPointsLatLonMsnm']:
        # print(pt)
        points.append(latlonAlt2XYZ(pt))
    # print(points)
    # print(x_render_MaxAltitude, y_render_MaxAltitude, z_render_MaxAltitude)
    # print(data['lonlatmaxAltitude'])
    # print(data['lonlatImpact'])
    # print(len(data['points']))
    # print(len(data['distances']))
    # print(len(data['elevations']))
    # print(data['lonlatImpact'])
    # print(data['lonlatPlatform'], data['altitudePlatform'])
    # print(len(data['listPointsLatLonMsnm']))
    # print(len(data['listPointsDistAlt']))

    return points, data['listPointsLatLonMsnm'], data['listPointsDistAlt'], data['distances'], data['elevations']

# print(getTrajectory(lonPlatform=-66.15700687603821, latPlatform=-17.383694116678157,
#                     lonObjetive=-66.04713014696468, latObjetive=-17.561585808273836))
