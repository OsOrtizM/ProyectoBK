import aplication
import aplicationV2

# app = aplication.GeoMipTerrainDemo()

coordenada = 'S18W067'
app = aplicationV2.ShaderTerrainDemo(cor=coordenada)
app.run()
