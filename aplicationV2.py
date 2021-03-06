from direct.gui.DirectDialog import DirectDialog
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.ShowBase import ShowBase
from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import ShaderTerrainMesh, Shader, load_prc_file_data, LineSegs
from panda3d.core import SamplerState
import sys
import Coordinates as sig

from reportGenerator import reporte


class ShaderTerrainDemo(ShowBase):

    def __init__(self, latPlat, lonPlat, latObj, lonObj, azPlat, name):
        load_prc_file_data("", """
            # archivo de configuracion 
            
            # no redimensiona la entrada
            textures-power-2 none
            
            # sistema de coordenadas
            gl-coordinate-system default
            # filled-wireframe-apply-shader true
            # configurar titulo de la ventana
            window-title ENTORNOS VIRTUALES DE ESTUDIO DE MISILES
            
            # cantidad de vistas/optimizacion
            # stm-max-views 1

            # cantidad de fragmetos a mostrar, depende del nivel de detalle/optimizacion
            # stm-max-chunk-count 2048

            # poner en pantalla completa
            # fullscreen true     
            
            # want-directtools true
            # want-tk true
            # tamaño ventana
            win-size 1024 768
            win-fixed-size 1
            show-frame-rate-meter t
            # show-scene-graph-analyzer-meter 1
            # show-tex-mem 1

        """)

        ShowBase.__init__(self)  # inicializacion
        self.latitudePlataform = float(latPlat)
        self.longitudePlataform = float(lonPlat)
        self.latitudeObj = float(latObj)
        self.longitudeObj = float(lonObj)
        self.azimutPlat = float(azPlat)
        self.name = name

        self.terrain_node = ShaderTerrainMesh()  # crear el terreno
        self.altitudePlataform, self.cell = sig.latLon2AltCell(lon=self.longitudePlataform, lat=self.latitudePlataform)
        self.altitudeObj, _ = sig.latLon2AltCell(lon=self.longitudeObj, lat=self.latitudeObj)
        print('Plataforma: ', self.latitudePlataform, self.longitudePlataform, self.altitudePlataform)
        print('Objetivo: ', self.latitudeObj, self.longitudeObj, self.altitudeObj)
        print('Celda: ', self.cell)
        nameFile = self.cell[:-4]
        self.mde_path = 'img/ASTER-GDEM-BOLIVIA/Hm/' + nameFile + '.bmp'

        heightfield = self.loader.loadTexture(self.mde_path)  # cargar MDE
        heightfield.wrap_u = SamplerState.WM_clamp
        heightfield.wrap_v = SamplerState.WM_clamp
        self.terrain_node.heightfield = heightfield  # setear MDE

        self.terrain_node.target_triangle_width = 10.0  # ancho del triangulo/detalle
        self.terrain_node.setChunkSize(8)
        self.terrain_node.generate()  # genera el terreno
        self.terrain = self.render.attach_new_node(self.terrain_node)  # vincula al nodo render
        self.scaleXY = 4096
        self.scaleZ = 1760
        self.terrain.set_scale(self.scaleXY, self.scaleXY, self.scaleZ)  # escala
        self.terrain.set_pos(0, 0, 0)

        # setear shaders
        terrain_shader = Shader.load(Shader.SL_GLSL, "extras/shaders/terrain.vert.glsl",
                                     "extras/shaders/terrain.frag.glsl")
        self.terrain.set_shader(terrain_shader)
        self.terrain.set_shader_input("camera", base.cam)

        # setear textura
        self.texture_path = "img/Texturas/jpg/" + sig.getTexture(nameFile) + ".jpg"
        grass_tex = self.loader.loadTexture(self.texture_path)
        grass_tex.set_minfilter(SamplerState.FT_linear_mipmap_linear)
        grass_tex.set_anisotropic_degree(16)
        self.terrain.set_texture(grass_tex)

        self.maxdistance = 300
        self.camLens.setFar(self.maxdistance)  # setear distancia lejana
        self.camLens.setNear(0.1)
        self.camLens.set_fov(90)  # setear campo de vision

        x_tiff, y_tiff = sig.latLonCell2XY(lon=self.longitudePlataform, lat=self.latitudePlataform, cell=self.cell)
        x_render, y_render = sig.XYtiff2XYrender(x_tiff=x_tiff, y_tiff=y_tiff)
        self.missile = self.loader.loadModel("img/Modelos/misilModelo.egg")
        x_missile = y_render
        y_missile = self.scaleXY - x_render
        z_missile = sig.altitude2Z(self.altitudePlataform) + 0.6

        x_tiff_obj, y_tiff_obj = sig.latLonCell2XY(lat=self.latitudeObj, lon=self.longitudeObj, cell=self.cell)
        x_render_obj, y_render_obj = sig.XYtiff2XYrender(x_tiff=x_tiff_obj, y_tiff=y_tiff_obj)
        self.objetive = self.loader.loadModel("img/Modelos/misilModelo.egg")
        x_objetive = y_render_obj
        y_objetive = self.scaleXY - x_render_obj
        z_objetive = sig.altitude2Z(self.altitudeObj)

        self.missile.setPos(x_missile, y_missile, z_missile)  # invertido
        self.missile.reparentTo(self.render)
        self.missile.setScale(1, 1, 1)
        print('posMisil:', x_missile, y_missile, z_missile)
        self.objetive.setPos(x_objetive, y_objetive, z_objetive)  # invertido
        self.objetive.reparentTo(self.render)
        self.objetive.setScale(10, 10, 100)
        print('posObjetivo: ', x_objetive, y_objetive, z_objetive)

        pointsXYZ, pointslatlonalt, pointsXY, distancesTerrain, elevationsTerrain = sig.getTrajectory(
            latPlatform=self.latitudePlataform, lonPlatform=self.longitudePlataform,
            latObjetive=self.latitudeObj, lonObjetive=self.longitudeObj,
            maxPoints=30, azimutPlat=azPlat)

        # self.drawTrajectory(pointsXYZ)
        # self.trajectory = self.drawTrajectory(pointsXYZ)
        # self.trajectoryNode = self.render.attachNewNode(self.trajectory)
        base.cam.setPos(x_missile, y_missile - 5, z_missile + 5)
        base.cam.setP(-45)
        # print(base.cam.getHpr())
        OnscreenText(text='Presione Esc para finalizar', pos=(-1, 0.95), scale=0.06)
        OnscreenText(text='Presione D para la trayectoria', pos=(-0.95, 0.90), scale=0.06)
        # base.cam.setHpr(94.8996, -16.6549, 1.55508)
        # render.clearFog()

        # teclas
        self.accept("f3", self.toggleWireframe)
        self.accept("escape", self.confirmExit, [pointslatlonalt, pointsXY, distancesTerrain, elevationsTerrain])
        self.accept("d", self.drawTrajectory, [pointsXYZ])

    def itemSel(self, arg, XYZ, XY, dis, ele):
        if arg is 'report':
            self.callReport(XYZ, XY, dis, ele)
        else:
            sys.exit()

    def confirmExit(self, XYZ, XY, dis, ele):
        dialog = DirectDialog(dialogName="test",
                              text="¿QUE DESEA HACER?",
                              buttonTextList=['GENERAR REPORTE', 'SALIR'],
                              buttonValueList=['report', 'exit'],
                              # buttonSize=(0.1, 0.1, 0.5, 0.5),
                              topPad=0.1,
                              midPad=0.1,
                              sidePad=0.1,
                              buttonPadSF=1.1,
                              command=self.itemSel,
                              extraArgs=[XYZ, XY, dis, ele],
                              fadeScreen=1
                              )

    def callReport(self, XYZ, XY, dis, ele):
        reporte(ptXYZ=XYZ, ptXY=XY, dis=dis, elev=ele, azimut=self.azimutPlat,
                latPlat=self.latitudePlataform, lonPlat=self.longitudePlataform,
                latObj=self.latitudeObj, lonObj=self.longitudeObj, name=self.name)
        sys.exit()

    def drawTrajectory(self, points, color=(255, 255, 255, 1)):
        # print(points)
        # line = LineSegs()
        # line.setColor(color)
        # line.setThickness(50)

        # for i, pt in enumerate(points[:-1]):
        taskMgr.doMethodLater(0.5,
                              self.drawLine, name='Pintar',
                              extraArgs=(points, 0)
                              )
        #     print(i)
        # line.moveTo(points[i][1], self.scaleXY - points[i][0], points[i][2])
        # line.drawTo(points[i + 1][1], self.scaleXY - points[i + 1][0], points[i + 1][2])
        #
        # param = line.create()
        # self.render.attachNewNode(param)

        # time.sleep()

        # return param

    def drawLine(self, points, ind, color=(255, 255, 255, 1)):
        if len(points) - 1 == ind:
            return 0
        line = LineSegs()
        line.setColor(color)
        line.setThickness(50)
        line.moveTo(points[ind][1], self.scaleXY - points[ind][0], points[ind][2])
        line.drawTo(points[ind + 1][1], self.scaleXY - points[ind + 1][0], points[ind + 1][2])
        param = line.create()
        self.render.attachNewNode(param)
        taskMgr.doMethodLater(0.5,
                              self.drawLine, name='Pintar',
                              extraArgs=(points, ind + 1)
                              )
