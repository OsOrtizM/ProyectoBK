from direct.showbase.ShowBase import ShowBase
from panda3d.core import GeoMipTerrain, load_prc_file_data
import sys


class GeoMipTerrainDemo(ShowBase):
    def __init__(self):
        load_prc_file_data("", """    
                    # archivo de configuracion  
                                        
                    # configurar titulo de la ventana
                    window-title Panda3D - Mapeo a terreno 3D
                    
                    # poner en pantalla completa
                    # fullscreen true                     
                """)

        ShowBase.__init__(self)                         # inicializacion
        terrain = GeoMipTerrain("world")                # crear el terreno
        self.mde_path = '../img/ASTER-GDEM-BOLIVIA/ASTGTM2_S18W067_dem.bmp'
        terrain.setHeightfield(self.mde_path)           # setear MDE
        self.texture_path = '../img/textures/mountain.jpg'
        terrain.setColorMap(self.texture_path)          # setear textura
        root = terrain.getRoot()                        # obtener nodo del terreno
        root.reparentTo(self.render)                    # vincular al nodo render
        root.setSz(5000)                                # escala

        self.maxDistance = 1000
        self.camLens.setFar(self.maxDistance)           # setear distancia lejana
        self.camLens.setFov(60)                         # setear campo de vision
        terrain.generate()                              # generar el terreno
        self.render.setShaderAuto()                     # sombreador automatico
        self.accept("f3", self.toggleWireframe)         # para ver la malla
        self.accept("escape", sys.exit)                 # para cerrar el programa