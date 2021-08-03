import datetime
import os
import time
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import staticmaps
from staticmaps import Line, Area
import matplotlib.pyplot as plt
import Coordinates


def generateMap(latPlat, lonPlat, latObj, lonObj, azimut, name):
    context = staticmaps.Context()
    context.set_tile_provider(staticmaps.tile_provider_OSM)
    center1 = staticmaps.create_latlng(latPlat, lonPlat)
    center2 = staticmaps.create_latlng(latObj, lonObj)

    geoLineaDirection = Coordinates.pointRadialDistanceV2(latPlat, lonPlat, 20000, azimut)
    coor = [(latPlat, lonPlat), (geoLineaDirection['lat'], geoLineaDirection['lon'])]
    coordinates = [staticmaps.create_latlng(lat, lng) for lat, lng in coor]
    lineAzimut = Line(coordinates, staticmaps.BLACK, 5)

    geoLineaDirectionLeft = Coordinates.pointRadialDistanceV2(latPlat, lonPlat, 20000, azimut - 110)
    coorLeft = [(latPlat, lonPlat), (geoLineaDirectionLeft['lat'], geoLineaDirectionLeft['lon'])]
    coordinatesLeft = [staticmaps.create_latlng(lat, lng) for lat, lng in coorLeft]
    lineAzimutLeft = Line(coordinatesLeft, staticmaps.BLACK, 5)

    geoLineaDirectionRight = Coordinates.pointRadialDistanceV2(latPlat, lonPlat, 20000, azimut + 110)
    coorRight = [(latPlat, lonPlat), (geoLineaDirectionRight['lat'], geoLineaDirectionRight['lon'])]
    coordinatesRight = [staticmaps.create_latlng(lat, lng) for lat, lng in coorRight]
    lineAzimutRight = Line(coordinatesRight, staticmaps.BLACK, 5)

    areaAlcanzable = [Coordinates.pointRadialDistanceV2(latPlat, lonPlat, 15000, azimut - i) for i in range(-110, 111)]
    alcanzable = [(i['lat'], i['lon']) for i in areaAlcanzable]
    alcanzable.insert(0, (float(latPlat), float(lonPlat)))
    alcanzable.append((float(latPlat), float(lonPlat)))
    coordinatesArea = [staticmaps.create_latlng(lat, lng) for lat, lng in alcanzable]
    area = Area(coordinatesArea, fill_color=staticmaps.parse_color("#b1cbb14d"),
                color=staticmaps.parse_color("#008000"), width=6)

    context.add_object(
        staticmaps.Circle(center1, 15, fill_color=staticmaps.parse_color("#e4b1b14d"), color=staticmaps.RED, width=6))
    context.add_object(
        staticmaps.Circle(center1, 10, fill_color=staticmaps.parse_color("#b1b1e44d"), color=staticmaps.BLUE, width=6))
    context.add_object(lineAzimut)
    context.add_object(lineAzimutLeft)
    context.add_object(lineAzimutRight)
    context.add_object(area)

    context.add_object(staticmaps.ImageMarker(center2, 'img/Images/dianatiny.png', 20, 20))
    context.add_object(staticmaps.Marker(center1, color=staticmaps.parse_color("#3f92cf"), size=20))

    # image = context.render_pillow(40000, 60000)
    image = context.render_pillow(1500, 850)
    os.makedirs('reports/' + name, exist_ok=True)
    image.save("reports/" + name + '/' + name + "_map.png")


def generateGraphXY(XY, dist, elev, name):
    x = [i[0] for i in XY]
    y = [i[1] for i in XY]
    plt.plot(x, y)
    plt.plot(dist, elev)
    plt.fill_between(dist, elev, color="#ffd8b6")
    ejeXini, ejeXend = min(dist), max(dist)
    ejeYini, ejeYend = min(y), max(y)
    plt.ylabel('Altura (m.s.n.m)')
    plt.xlabel('Distancia (m.)')
    plt.annotate('Altura Maxima Aproximada\n' + "Distancia: " + str(round(x[y.index(max(y))])) +
                 " mts.\nAltura: " + str(round(max(y))) + " mts.",
                 xy=(x[y.index(max(y))], max(y)), xytext=(x[y.index(max(y))] - 500, max(y) + 500),
                 arrowprops=dict(facecolor='black', shrink=0.01))
    plt.annotate('Impacto Aproximado\n' + "Distancia: " + str(round(x[-1])) +
                 " mts.\nAltura: " + str(round(y[-1])) + " mts.",
                 xy=(x[-1], y[-1]), xytext=(x[-1] - 500, y[-1] - 500),
                 arrowprops=dict(facecolor='black'))
    plt.axis([ejeXini - 100, ejeXend + 100, ejeYini - 500, ejeYend + 500])
    os.makedirs('reports/' + name, exist_ok=True)
    plt.savefig("reports/" + name + '/' + name +"_xy.png")


# def generateGraphXYZ(XYZ):
# x = [i[0] for i in XYZ]
# y = [i[1] for i in XYZ]
# z = [i[2] for i in XYZ]
#     fig = plt.figure()
#     ax = fig.add_subplot(111, projection='3d')
#     ax.plot_trisurf(x, y, z, color='white', edgecolors='grey', alpha=1)
#     # ax.scatter(x, y, z, c='red')
#     plt.show()
#
# generateGraphXYZ(cord)

def reporte(ptXYZ, ptXY, dis, elev, name, latPlat, lonPlat, latObj, lonObj, azimut):
    margen = 50
    w, h = letter
    generateGraphXY(ptXY, dis, elev, name)
    generateMap(latPlat, lonPlat, latObj, lonObj, azimut, name)
    os.makedirs('reports/' + name, exist_ok=True)
    c = canvas.Canvas("reports/" + name + '/' + name + ".pdf", pagesize=letter)
    c.setFont("Times-Bold", 18)
    # print(c.getAvailableFonts())
    c.drawString(margen + 200, h - margen, "REPORTE")
    c.setFont("Times-Bold", 12)

    c.drawString(margen + 160, h - margen - 20,
                 "Fecha y Hora: " + str(datetime.datetime.now().strftime('%d/%m/%Y')) + '  ' + str(time.strftime("%X")))
    c.drawImage("img/Images/EMI.PNG", 431, h - 90, width=100, height=50)
    c.setFont("Times-Roman", 12)
    c.drawString(margen + 230 + 31, h - margen - 40, "Misil: " + name)
    c.drawString(margen + 31, h - margen - 40, "Azimut Plataforma: " + str(azimut))
    c.drawString(margen + 31, h - margen - 60, "Latitud Plataforma: " + str(latPlat))
    c.drawString(margen + 31, h - margen - 80, "Longitud Plataforma: " + str(lonPlat))
    c.drawString(margen + 230 + 31, h - margen - 60, "Latitud Objetivo: " + str(latObj))
    c.drawString(margen + 230 + 31, h - margen - 80, "Longitud Objetivo: " + str(lonObj))
    c.drawImage("reports/" + name + '/' + name + "_map.png", margen + 31, h - margen - 340, width=450, height=250)
    espacePreTable = 91
    x_table1 = [
        espacePreTable + margen,
        espacePreTable + margen + 130,
        espacePreTable + margen + 260,
        espacePreTable + margen + 330
    ]
    y_table1 = [(i * 11) + margen for i in range(0, 33)]
    c.grid(x_table1, y_table1)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(espacePreTable + margen + 40, margen + 343, "LATITUD")
    c.drawString(espacePreTable + margen + 170, margen + 343, "LONGITUD")
    c.drawString(espacePreTable + margen + 275, margen + 343, "ALTURA")
    c.setFont("Helvetica", 10)
    for i, cor in enumerate(ptXYZ):
        c.drawString(espacePreTable + margen + 10, margen + 332 - (11 * i), str(cor[1]))
        c.drawString(espacePreTable + margen + 140, margen + 332 - (11 * i), str(cor[0]))
        c.drawString(espacePreTable + margen + 270, margen + 332 - (11 * i), str(round(cor[2], 4)))
    c.showPage()
    # /////////////////////////////nueva hoja//////////////////////////////////////
    c.setFont("Times-Bold", 18)
    c.drawString(margen + 200, h - margen, "REPORTE")
    c.setFont("Times-Bold", 12)

    c.drawString(margen + 160, h - margen - 20,
                 "Fecha y Hora: " + str(time.strftime("%x")) + '  ' + str(time.strftime("%X")))
    c.drawImage("img/Images/EMI.PNG", 431, h - 90, width=100, height=50)
    c.setFont("Times-Roman", 12)
    c.drawString(margen + 230 + 31, h - margen - 40, "Misil: " + name)
    c.drawString(margen + 31, h - margen - 40, "Azimut Plataforma: " + str(azimut))
    c.drawString(margen + 31, h - margen - 60, "Latitud Plataforma: " + str(latPlat))
    c.drawString(margen + 31, h - margen - 80, "Longitud Plataforma: " + str(lonPlat))
    c.drawString(margen + 230 + 31, h - margen - 60, "Latitud Objetivo: " + str(latObj))
    c.drawString(margen + 230 + 31, h - margen - 80, "Longitud Objetivo: " + str(lonObj))
    c.drawImage("reports/" + name + '/' + name + "_xy.png", margen + 31, h - margen - 340, width=450, height=250)
    espacePreTable = 126
    x_table2 = [
        espacePreTable + margen,
        espacePreTable + margen + 130,
        espacePreTable + margen + 260
    ]
    y_table2 = [(i * 11) + margen for i in range(0, 33)]
    c.grid(x_table2, y_table2)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(espacePreTable + margen + 40, margen + 343, "RECORRIDO")
    c.drawString(espacePreTable + margen + 170, margen + 343, "ALTURA")
    c.setFont("Helvetica", 10)
    for i, cor in enumerate(ptXY):
        c.drawString(espacePreTable + margen + 40, margen + 332 - (11 * i), str(cor[0]))
        c.drawString(espacePreTable + margen + 170, margen + 332 - (11 * i), str(round(cor[1], 4)))

    c.showPage()
    c.save()
    print('reporte generado')
    path = "reports/" + name
    path = os.path.realpath(path)
    os.startfile(path)
