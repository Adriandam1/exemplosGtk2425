import pathlib

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository.Gtk import TreeStore

#Tenemos que importar Path de pathlib
from pathlib import Path

# pathlib -> Path(/home/dam)

# ESTO es treeview modo arbol
class FiestraPrincipal (Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Exemplo con Gtk TreeView en arbore de debian")

        caixaV = Gtk.Box (orientation = Gtk.Orientation.VERTICAL, spacing= 6)

        modelo = TreeStore (str, str)

        # Creamos el TreeView
        trvVista = Gtk.TreeView(model=modelo)

        # columna 0 ( ICONOS)
        tvcColumna = Gtk.TreeViewColumn()
        trvVista.append_column(tvcColumna) # añadismos la columna a la vista TreeView
        celdaGraficos = Gtk.CellRendererPixbuf()
        tvcColumna.pack_start(celdaGraficos, True)
        tvcColumna.add_attribute(celdaGraficos, "icon_name", 0)

        # columna 1 (nombres)
        tvcColumna = Gtk.TreeViewColumn ()
        trvVista.append_column(tvcColumna) # añadimos la columna a la vista TreeView
        celda = Gtk.CellRendererText()
        tvcColumna.pack_start(celda, True)
        tvcColumna.add_attribute(celda, 'text', 1)


        # ruta_base = Path ('/home/dam')
        self.explorarDirectorio('/home/dam', None, modelo)

        # Añadimos el TreeView al contenedor
        caixaV.pack_start(trvVista, True, True, 0)

        # Configuración de la ventana
        self.add(caixaV)
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()

    """
    # funcion  original de manuel
    def explorarDirectorio (self, ruta, punteiroPai, modelo):
        contidoDir = pathlib.Path(ruta)
        for entrada in contidoDir.iterdir():

            if entrada.is_dir(): # .is_dir() nos permite verificar que sea un directorio
                # icono para las carpetas "folder"
                punteiroFillo = modelo.append(punteiroPai, ("folder", entrada.name))
                self.explorarDirectorio(ruta + '/' + entrada.name, punteiroFillo, modelo)
            else:#en el caso de que no sea un direcotio sino un archivo:
                #print(entrada.name)
                modelo.append(punteiroPai, ("emblem-documents", entrada.name))
                #self.explorarDirectorio(ruta + '/' + entrada.name, punteiroFillo, modelo)
    """
    # función explorarDirectorio Manuel  con gtp
    def explorarDirectorio(self, ruta, punteiroPai, modelo):
        contidoDir = pathlib.Path(ruta)
        for entrada in contidoDir.iterdir():

                # Decodifica el nombre con surrogateescape GPT izo esto por un error uft-8 que dio, "no deberia hacer falta"
                # UnicodeEncodeError: 'utf-8' codec can't encode character '\udcd0' in position 0: surrogates not allowed
                nombre = entrada.name.encode('utf-8', 'surrogateescape').decode('utf-8', 'replace')

                if entrada.is_dir():  # Si es un directorio
                    punteiroFillo = modelo.append(punteiroPai, ("folder", nombre))
                    self.explorarDirectorio(ruta + '/' + entrada.name, punteiroFillo, modelo)
                else:  # Si es un archivo
                    modelo.append(punteiroPai, ("emblem-documents", nombre))



if __name__ == "__main__":
    FiestraPrincipal()
    Gtk.main()