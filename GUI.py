# importing only those functions
# which are needed
import sys
import tkinter as tk
import tkinter.font as font
from tkinter import ttk, messagebox

from PIL import Image, ImageTk

import aplicationV2

# creating tkinter window
root = tk.Tk()
root.title("EMI")
# root.option_add('*font', ('verdana', 12, 'bold'))
root.geometry('500x400')  # 1920x1080
root.resizable(width=0, height=0)

lblTitulo = ttk.Label(root, text="ENTORNOS VIRTUALES DE ESTUDIO DE MISILES", justify='center')
fuenteTitulo = font.Font(family='MS Shell Dlg 2', size=12, weight='bold')
lblTitulo['font'] = fuenteTitulo
lblTitulo.place(x=50, y=10)

fuente = font.Font(family='MS Shell Dlg 2', size=8, weight='normal')

lblFrameMisil = tk.LabelFrame(root, width=300, height=130, text="Coordenadas de la Plataforma")
lblFrameMisil['font'] = fuente
lblFrameMisil.place(x=100, y=50)
lblFrameObj = tk.LabelFrame(root, width=300, height=130, text="Coordendas del Objetivo")
lblFrameObj['font'] = fuente
lblFrameObj.place(x=100, y=200)

canvas = tk.Canvas(lblFrameMisil, width=105, height=95)
canvas.place(x=5, y=10)
image = Image.open('img/Images/misil.png')
my_img = ImageTk.PhotoImage(image.resize((105, 95)))
canvas.create_image(50, 50, image=my_img)

lblLatPlatform = ttk.Label(lblFrameMisil, text="Latitud ↓", justify='center')
lblLatPlatform['font'] = fuente
lblLatPlatform.place(x=120, y=0)
txtLatPlatform = ttk.Entry(lblFrameMisil, width=27)
txtLatPlatform['font'] = fuente
txtLatPlatform.place(x=120, y=16)

lblLonPlatform = ttk.Label(lblFrameMisil, text="Longitud ↓", justify='center')
lblLonPlatform['font'] = fuente
lblLonPlatform.place(x=120, y=36)
txtLonPlatform = ttk.Entry(lblFrameMisil, width=27)
txtLonPlatform['font'] = fuente
txtLonPlatform.place(x=120, y=52)

lblAzPlatform = ttk.Label(lblFrameMisil, text="Azimut ↓", justify='center')
lblAzPlatform['font'] = fuente
lblAzPlatform.place(x=120, y=72)
txtAzPlatform = ttk.Entry(lblFrameMisil, width=10)
txtAzPlatform['font'] = fuente
txtAzPlatform.place(x=120, y=88)

lblNameMisil = ttk.Label(lblFrameMisil, text="Modelo Misil ↓", justify='center')
lblNameMisil['font'] = fuente
lblNameMisil.place(x=210, y=72)
txtNameMisil = ttk.Entry(lblFrameMisil, width=12)
txtNameMisil['font'] = fuente
txtNameMisil.place(x=210, y=88)

canvas2 = tk.Canvas(lblFrameObj, width=105, height=95)
canvas2.place(x=5, y=10)
image2 = Image.open('img/Images/diana.png')
my_img2 = ImageTk.PhotoImage(image2.resize((105, 95)))
canvas2.create_image(50, 50, image=my_img2)

lblLatObj = ttk.Label(lblFrameObj, text="Latitud ↓", justify='center')
lblLatObj['font'] = fuente
lblLatObj.place(x=120, y=15)
txtLatObj = ttk.Entry(lblFrameObj, width=27)
txtLatObj['font'] = fuente
txtLatObj.place(x=120, y=31)

lblLonObj = ttk.Label(lblFrameObj, text="Longitud ↓", justify='center')
lblLonObj['font'] = fuente
lblLonObj.place(x=120, y=60)
txtLonObj = ttk.Entry(lblFrameObj, width=27)
txtLonObj['font'] = fuente
txtLonObj.place(x=120, y=76)


def ejecutar():
    if txtLatPlatform.get() and txtLonPlatform.get() and txtLatObj.get() \
            and txtLonObj.get() and txtAzPlatform.get():
        print('valido')
        latitudePlataform = float(txtLatPlatform.get())
        longitudePlataform = float(txtLonPlatform.get())
        latitudeObj = float(txtLatObj.get())
        longitudeObj = float(txtLonObj.get())
        azimutPlataform = float(txtAzPlatform.get())
        name = txtNameMisil.get()
        # # longitudePlataform, latitudePlataform = -66.15700687603821, -17.383694116678157         # emi
        # longitudePlataform, latitudePlataform = -66.13486064219316, -17.38395447862384        # cristo
        # # longitudePlataform, latitudePlataform = -66.31072900706361, -17.422539946086463       # calvario
        # # longitudePlataform, latitudePlataform = -66.3917877770738, -17.285657545649716        # tunari
        # longitudeObj, latitudeObj = -66.15700687603821, -17.383694116678157
        # azimutPlataform = 180
        # name = 'Prueba10'

        root.withdraw()
        app = aplicationV2.ShaderTerrainDemo(latPlat=latitudePlataform, lonPlat=longitudePlataform, name=name,
                                             latObj=latitudeObj, lonObj=longitudeObj, azPlat=azimutPlataform)
        app.run()
        # pic = QPixmap("mapaQt.png")
        # self.lblMapa.setPixmap(pic)
        # self.lblMapa.show()
        # self.close()
        # self.txtLatMisil.setText("-17.383694116678157")
        # self.txtLonMisil.setText("-66.15700687603821")
        # self.txtLatObj.setText("-17.38395447862384")
        # self.txtLonObj.setText("-66.13486064219316")

        # appP = aplicationV2.ShaderTerrainDemo(latPlat=self.txtLatMisil.text(), lonPlat=self.txtLonMisil.text(),
        #                                      latObj=self.txtLatObj.text(), lonObj=self.txtLonObj.text(),
        #                                      azPlat=self.txtAzimut.text(), Qtapp=QApplication.processEvents())
        # self.mutex.locked()
        # appP.run()
        # self.mutex.release()
    else:
        print('invalido')
        messagebox.showerror(message="Llene los datos correctamente", title="Error")
        # self.lblAviso.show()
        # self.btnAviso.show()
    # latitudePlataform = txtLatPlatform.get()
    # longitudePlataform = txtLonPlatform.get()
    # latitudeObj = txtLatObj.get()
    # longitudeObj = txtLonObj.get()
    # name = txtNameMisil.get()
    # longitudePlataform, latitudePlataform = -66.15700687603821, -17.383694116678157         # emi
    # longitudePlataform, latitudePlataform = -66.13486064219316, -17.38395447862384        # cristo
    # longitudePlataform, latitudePlataform = -66.31072900706361, -17.422539946086463       # calvario
    # longitudePlataform, latitudePlataform = -66.3917877770738, -17.285657545649716        # tunari
    # -17.383694116678157 - 66.15700687603821 - 17.469241909052002 - 65.9034988394223
    # longitudeObj, latitudeObj = -66.13486064219316, -17.38395447862384
    # azimutPlataform = 180
    # root.withdraw()
    # app = aplicationV2.ShaderTerrainDemo(latPlat=latitudePlataform, lonPlat=longitudePlataform, name=name,
    #                                      latObj=latitudeObj, lonObj=longitudeObj, azPlat=azimutPlataform)
    # app.run()


def cerrar():
    print('cerrado')
    if messagebox.askyesno(message="¿Desea cerra el programa?", title="Título"):
        sys.exit()


style = ttk.Style()
style.configure("TButton", font=('verdana', 15, 'bold'))
btnComenzar = ttk.Button(root, text="Comenzar!", command=ejecutar, width=10, style="TButton")
btnComenzar.place(x=250, y=350)

style = ttk.Style()
style.configure("TButton", font=('verdana', 15, 'bold'))
btnComenzar = ttk.Button(root, text="Salir", command=cerrar, width=5, style="TButton")
btnComenzar.place(x=100, y=350)




root.mainloop()
