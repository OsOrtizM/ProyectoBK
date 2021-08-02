# importing only those functions
# which are needed
import tkinter as tk
from tkinter import ttk
import tkinter.font as font
import aplicationV2


# creating tkinter window
root = tk.Tk()
root.title("ENTORNOS VIRTUALES DE ESTUDIO DE MISILES")
root.option_add('*font', ('verdana', 12, 'bold'))
root.geometry('1220x900')  # 1920x1080
fuente = font.Font(family='verdana', size=20, weight='bold')
root.resizable(width=0, height=0)
# photo = tk.PhotoImage(file=r"img/Mapas/MapaBolivia_Coordenadas.PNG")
#
# imgMapa = ttk.Label(root, image=photo)
# imgMapa.pack(side="left", fill="both", expand="yes")

lblCoorPlatform = ttk.Label(root, text="Coordenadas Origen", justify='center')
lblCoorPlatform['font'] = fuente
lblCoorPlatform.place(x=850, y=100)

lblLatPlatform = ttk.Label(root, text="Ingrese Latitud", justify='center')
lblLatPlatform['font'] = fuente
lblLatPlatform.place(x=850, y=150)

txtLatPlataform = ttk.Entry(root, width=19)
txtLatPlataform['font'] = fuente
txtLatPlataform.place(x=850, y=200)

lblLonPlataform = ttk.Label(root, text="Ingrese Longitud", justify='center')
lblLonPlataform['font'] = fuente
lblLonPlataform.place(x=850, y=250)

txtLonPlataform = ttk.Entry(root, width=19)
txtLonPlataform['font'] = fuente
txtLonPlataform.place(x=850, y=300)

lblCoorObj = ttk.Label(root, text="Coordenadas Destino", justify='center')
lblCoorObj['font'] = fuente
lblCoorObj.place(x=850, y=400)

lblLatObj = ttk.Label(root, text="Ingrese Latitud", justify='center')
lblLatObj['font'] = fuente
lblLatObj.place(x=850, y=450)

txtLatObj = ttk.Entry(root, width=19)
txtLatObj['font'] = fuente
txtLatObj.place(x=850, y=500)

lblLonObj = ttk.Label(root, text="Ingrese Longitud", justify='center')
lblLonObj['font'] = fuente
lblLonObj.place(x=850, y=550)

txtLonObj = ttk.Entry(root, width=19)
txtLonObj['font'] = fuente
txtLonObj.place(x=850, y=600)


def ejecutar():
    latitudePlataform = txtLatPlataform.get()
    longitudePlataform = txtLonPlataform.get()
    latitudeObj = txtLatObj.get()
    longitudeObj = txtLonObj.get()
    name = txtLatPlataform.get()
    longitudePlataform, latitudePlataform = -66.15700687603821, -17.383694116678157         # emi
    # longitudePlataform, latitudePlataform = -66.13486064219316, -17.38395447862384        # cristo
    # longitudePlataform, latitudePlataform = -66.31072900706361, -17.422539946086463       # calvario
    # longitudePlataform, latitudePlataform = -66.3917877770738, -17.285657545649716        # tunari
    # -17.383694116678157 - 66.15700687603821 - 17.469241909052002 - 65.9034988394223

    longitudeObj, latitudeObj = -66.13486064219316, -17.38395447862384
    azimutPlataform = 180
    root.withdraw()
    app = aplicationV2.ShaderTerrainDemo(latPlat=latitudePlataform, lonPlat=longitudePlataform, name=name,
                                         latObj=latitudeObj, lonObj=longitudeObj, azPlat=azimutPlataform)
    app.run()


style = ttk.Style()
style.configure("TButton", font=('verdana', 20, 'bold'))
btnComenzar = ttk.Button(root, text="COMENZAR!", command=ejecutar, width=19, style="TButton")
btnComenzar.place(x=850, y=700)

root.mainloop()
