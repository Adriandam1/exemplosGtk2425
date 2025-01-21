
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import sqlite3 as dbapi

class FiestraPrincipal (Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Exemplo con Gtk TreeView e ordeado")


        caixaV = Gtk.Box (orientation = Gtk.Orientation.VERTICAL, spacing= 6)

        self.filtradoXenero = None
        modelo = Gtk.ListStore (str, str, int, str, bool)

        try:
            bbdd = dbapi.connect("baseDatos2.dat")
            cursor = bbdd.cursor()
            cursor.execute ("SELECT dni, nome, edade, xenero, falecido FROM usuarios")
            for rexistro in cursor:
                modelo.append (rexistro)
        except dbapi.DatabaseError as e:
            print ("Erro o cargar o ListStore "+ e)
        finally:
            cursor.close()
            bbdd.close()

        trvDatosUsuarios = Gtk.TreeView (model = modelo)
        seleccion = trvDatosUsuarios.get_selection()

        # columnas dni e nome
        for i, tituloColumna in enumerate (["Dni", "Nome"]):
            celda = Gtk.CellRendererText()
            columna = Gtk.TreeViewColumn(tituloColumna, celda, text =i)
            trvDatosUsuarios.append_column(columna)

        # columna edade
        # celda de progreso complecion CellRendererProgress
        celda = Gtk.CellRendererProgress()
        columna = Gtk.TreeViewColumn("Edade", celda, value = 2)
        trvDatosUsuarios.append_column(columna)

        # En la tabla abra una columna llamada genero que sera editable y tendra un combo con 3 posiblidades
        modeloCombo = Gtk.ListStore(str)
        modeloCombo.append("Muller",) # importante poner una coma al final para que se entienda que es una tupla
        modeloCombo.append("Home",)
        modeloCombo.append("Outros",)
        celda = Gtk.CellRendererCombo()
        celda.set_property("editable", True)
        celda.props.model = modeloCombo
        celda.set_property("text-column", 0) # tengo que decirle que columna de texto es del modelo, como es un modelo nuevo, sera la primera 0
        celda.set_property("has-entry", False) # poderiamos permitir o usuario que chegara a editar dentro de ese combo
        celda.connect("changed", self.on_celdaXenero_changed, modelo, 3)
        columna = Gtk.TreeViewColumn ("Xénero", celda, text = 3)
        trvDatosUsuarios.append_column(columna)

        celda = Gtk.CellRendererToggle()
        celda.connect("toggled", self.on_celda_toggled, modelo)
        columna = Gtk.TreeViewColumn("Falecido", celda, activate=4)
        trvDatosUsuarios.append_column(columna)


        caixaV.pack_start (trvDatosUsuarios, True, True, 0)
        self.add(caixaV)
        self.connect(("delete-event"), Gtk.main_quit)
        self.show_all()

    # funcion que se activa cuando se cambia o xenero no combo
    def on_celdaXenero_changed(self, celda, fila, filaXenero, modelo, columna):
        print(celda.props.model[filaXenero][0]) #mostra o valor que foi seleccionado(o novo valor)
        print(modelo [fila][columna]) # mostra o valor da columna
        modelo [fila][columna] = celda.props.model[filaXenero][0] #hacemos que los cambios realizados aparezcan en la vista
        #aplicamos os cambios a base de datos para que persistan
        try:
            bbdd = dbapi.connect("baseDatos2.dat")
            cursor = bbdd.cursor()
            cursor.execute("UPDATE usuarios set xenero=? WHERE dni=?",
                           (celda.props.model[filaXenero][0], modelo[fila][0])
                           )
            bbdd.commit()
        except dbapi.DatabaseError as e:
            print ("Erro o cargar o xénero: "+ e)
        finally:
            cursor.close()
            bbdd.close()

    def on_celda_toggled(self, control, fila, modelo):
        modelo[fila][4] = not modelo[fila][4]
        # faltaria que actualizase a base de datos


if __name__ == "__main__":
    FiestraPrincipal()
    Gtk.main()