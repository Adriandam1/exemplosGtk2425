import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository.Gtk import TreeStore
import sqlite3 as dbapi

# pathlib -> Path(/home/manuel)

# ESTO es treeview modo arbol
class FiestraPrincipal (Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Exemplo con Gtk TreeView en arbore")

        caixaV = Gtk.Box (orientation = Gtk.Orientation.VERTICAL, spacing= 6)

        modelo = TreeStore (str, int)

        # vamos a facer 5 avos que si clicamos neles van aparecer 4 pais, e por ultimo por cada pai vai a a haber 2 fillos
        for avo in range (5):
            punteiroAvo = modelo.append(None, ["Avo %i " %(avo,), avo])
            for pai in range (4):
                punteriroPai = modelo.append(punteiroAvo, ["Pai %i do avo %i" %(pai, avo), pai])
                for fillo in range (2):
                    # como e un elemento final nos necesitamos facer un punteiro para o fillo
                    modelo.append(punteriroPai, ["Neto %i do pai %i do avo %i "%(fillo, pai, avo), fillo])

        # creamos a vista:
        trvVista = Gtk.TreeView (model = modelo)
        tvcColumna = Gtk.TreeViewColumn ("Parentesco")
        trvVista.append_column(tvcColumna)
        celda = Gtk.CellRendererText()
        tvcColumna.pack_start(celda, True)
        tvcColumna.add_attribute(celda, 'text', 0)

        # segunda coumna
        tvcColumna = Gtk.TreeViewColumn("Orde")
        trvVista.append_column(tvcColumna)
        celda = Gtk.CellRendererText()
        tvcColumna.pack_start(celda, True)
        tvcColumna.add_attribute(celda, 'text', 1)

        # iniciamos o tree view
        caixaV.pack_start(trvVista, True, True, 0)

        self.add(caixaV)
        self.connect(("delete-event"), Gtk.main_quit)
        self.show_all()



if __name__ == "__main__":
    FiestraPrincipal()
    Gtk.main()