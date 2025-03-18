
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import sqlite3 as dbapi

from conexionBD import ConexionBD

class FiestraPrincipal (Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Exemplo con Gtk TreeView")
        # Resumen de grande a pequeño: Gt.TreeView -> Gtk.TreeViewColumn -> Gtk.CellRenderer
        # Creamos o TreeView o que engadimos columnas nas que engadimos celdas

        #Entrada de datos manual
        """
        columnas = ["Nome", "Apelido", "Numero de teléfono"]
        axendaTelefonica = [["Pepe", "Pérez", "986 543 210"],
                            ["Ana", "Alonso", "986 345 678"],
                            ["Rosa", "Vila", "621 432 567"],
                            ["Jose", "Diaz", "657 890 012"]]
        """


        # preparamos os datos
        # Entrada de datos por conexion sqlLite
        columnas = ["Nome", "Apelido", "Numero de teléfono"]
        axendaTelefonica = Gtk.ListStore (str, str, str)


        try:
            bbdd = dbapi.connect ("bdListinTelefonico.dat")
            print("Conexión a base de datos realizada")
            cursor = bbdd.cursor()
            cursor.execute ("SELECT * FROM listaTelefonos")
            for usuarioListin in cursor:
                axendaTelefonica.append(usuarioListin)
            cursor.close()
            bbdd.close()
        except dbapi.StandardError as e:
            print(e)
        except dbapi.DatabaseError as e:
            print(e)


        caixaV = Gtk.Box (orientation = Gtk.Orientation.VERTICAL, spacing= 6)
        vista = Gtk.TreeView (model = axendaTelefonica) # creamos o treeView e lle asignamos o modelo
        obxectoSeleccion = vista.get_selection()
        obxectoSeleccion.connect("changed", self.on_obxectoSeleccion_changed)

        for i in range (len(columnas)): # le danos a lonxitude da lista columnas e por cada elemento da lista repetimos has seguintes operaciones
            celda = Gtk.CellRendererText() # a celda vai a ir sempre asignada a unha columna, polo que temos que crear a columna
            columna = Gtk.TreeViewColumn(columnas[i], celda, text = i) # columna, celda, indice do modelo que vamos a representar
            vista.append_column(columna)

        # para rematar o que facemos e engadir a packstart
        caixaV.pack_start(vista, False, False, 0)  # False, False, 0 -> non se expande, non se expande, 0 de separacion

        self.add(caixaV)
        self.connect(("delete-event"), Gtk.main_quit)
        self.show_all()

    def on_obxectoSeleccion_changed(self, seleccion):
        (modelo, fila) = seleccion.get_selected()
        print(modelo [fila][0], modelo [fila][1], modelo [fila][2]) #mostramos os datos por pantalla a columna que seleccionamos


if __name__ == "__main__":
    FiestraPrincipal()
    Gtk.main()