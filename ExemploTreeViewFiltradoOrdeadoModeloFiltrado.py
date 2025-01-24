
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import sqlite3 as dbapi

# https://lazka.github.io/pgi-docs/Gtk-3.0/classes/RadioButton.html
# https://lazka.github.io/pgi-docs/Gtk-3.0/classes/ListStore.html

# ESTO ESUNA CONTINUACION DE TREEVIEWFILTRADOORDEADO pero usamos modelo_filtrado para filtrar campos
class FiestraPrincipal (Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Exemplo con Gtk TreeView e ordeado")


        caixaV = Gtk.Box (orientation = Gtk.Orientation.VERTICAL, spacing= 6)

        self.filtradoXenero = None
        # definicion do modelo
        modelo = Gtk.ListStore (str, str, int, str, bool)

        #indicamos a columna que vai a ser ordenada
        modelo.set_sort_func(2, self.compara_modelo, None)
        # saco un modelo distinto a partir to modelo orixinal y creo esta diferencia
        # creo modelo filtrado, que é parte de modelo
        modelo_filtrado = modelo.filter_new() # traballo con un modelo filtrado(me obriga a cambiar o modelo da vista o fago en filtradoOrdeado2.py)
        modelo_filtrado.set_visible_func(self.filtro_usuarios_xenero)





        try:
            bbdd = dbapi.connect("baseDatos2.dat")
            cursor = bbdd.cursor()
            cursor.execute ("SELECT dni, nome, edade, xenero, falecido FROM usuarios")
            for rexistro in cursor:
                modelo.append (rexistro)
        except dbapi.DatabaseError as e:
            print ("Erro o cargar o ListStore "+ str(e))
        finally:
            cursor.close()
            bbdd.close()

        trvDatosUsuarios = Gtk.TreeView (model = modelo_filtrado) # HEMOS CAMBIADO EL MODELO EN ESTA VERSION
        seleccion = trvDatosUsuarios.get_selection()

        # columnas dni e nome
        for i, tituloColumna in enumerate (["Dni", "Nome"]):
            celda = Gtk.CellRendererText()
            columna = Gtk.TreeViewColumn(tituloColumna, celda, text =i)
            trvDatosUsuarios.append_column(columna)

        # columna edade
        # celda de progreso complecion CellRendererProgress
        celda = Gtk.CellRendererProgress() # barra de progreso
        columna = Gtk.TreeViewColumn("Edade", celda, value = 2)
        columna.set_sort_column_id(2) # co modelo identificamos coa columna 2 permitirianos ordear os filas
        trvDatosUsuarios.append_column(columna)

        # En la tabla abra una columna llamada genero que sera editable y tendra un combo con 3 posiblidades
        modeloCombo = Gtk.ListStore(str)
        modeloCombo.append(("Muller",)) # importante poner una coma al final para que se entienda que es una tupla
        modeloCombo.append(("Home",))
        modeloCombo.append(("Outros",))
        celda = Gtk.CellRendererCombo()
        celda.set_property("editable", True)
        celda.props.model = modeloCombo
        celda.set_property("text-column", 0) # tengo que decirle que columna de texto es del modelo, como es un modelo nuevo, sera la primera 0
        celda.set_property("has-entry", False) # poderiamos permitir o usuario que chegara a editar dentro de ese combo
        celda.connect("changed", self.on_celdaXenero_changed, modelo, 3)
        columna = Gtk.TreeViewColumn ("Xénero", celda, text = 3)
        trvDatosUsuarios.append_column(columna)

        celda = Gtk.CellRendererToggle() # Cuadradito con checkmark
        celda.connect("toggled", self.on_celda_toggled, modelo)
        columna = Gtk.TreeViewColumn("Falecido", celda, activate=4)
        trvDatosUsuarios.append_column(columna)

        # creamos unha caixa horizontal
        caixaH = Gtk.Box (orientation=Gtk.Orientation.HORIZONTAL, spacing= 4)
            # creamos os botones
        rbtHome = Gtk.RadioButton(label= "Home")
            # Como queremos que los radiobutton tengan relacion y solo poder tener uno marcado, hacemos que los siguientes esten en el mismo "widget" que rbthome
        rbtMuller = Gtk.RadioButton.new_with_label_from_widget(rbtHome, label= "Muller")
        rbtOutros = Gtk.RadioButton.new_with_label_from_widget(rbtHome, label= "Outros")
            # engadimos os botones a caixa
        caixaH.pack_start(rbtHome, False, False, 2)
        caixaH.pack_start(rbtMuller, False, False, 2)
        caixaH.pack_start(rbtOutros, False, False, 2)
            # Para que reaccione cuando os manipulemos tratamos o sinal toggled
        rbtHome.connect ("toggled", self.on_xenero_toggled, "Home", modelo_filtrado)
        rbtMuller.connect ("toggled", self.on_xenero_toggled, "Muller", modelo_filtrado)
        rbtOutros.connect ("toggled", self.on_xenero_toggled, "Outros", modelo_filtrado)
        #Metemos esta caixa horizontal dentro da caixa vertical
        caixaV.pack_start(caixaH, True, True, 6)




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

    # funcion para cuando el toggle cambia
    def on_celda_toggled(self, control, fila, modelo):
        #modelo[fila][4] = not modelo[fila][4]
        # otra manera seria
        modelo[fila][4] = False if control.get_active() else True # si esl false, escribo true. si es true escribo false
        # faltaria que actualizase a base de datos
        try:
            bbdd = dbapi.connect("baseDatos2.dat")
            cursor = bbdd.cursor()
            cursor.execute("UPDATE usuarios set falecido=? WHERE dni=?",
                           (modelo[fila][4], modelo[fila][0]) # cogo campos falecido y dni
                           )
            bbdd.commit()
        except dbapi.DatabaseError as e:
            print ("Erro o cargar o xénero: "+ e)
        finally:
            cursor.close()
            bbdd.close()

    # estos 2 metodos siguientes nos permiten filtras a los usuarios por su xenero de modo que cuando se elige una opcion solo salen los usuarios de dicho genero
    def on_xenero_toggled(self, radioButton, xenero, modelo):
        if radioButton.get_active(): # si el radiobutton esta activado
            self.filtradoXenero = xenero # se recoge el valor y se le aplica
            #otra manera de hacerlo seria:
            #self.filtradoXenero = radioButton.props.label
            modelo.refilter() # revisar refilter

    def filtro_usuarios_xenero(self, modelo, fila, datos):
        # a temos preparada por si e un string o e tipo none
        if self.filtradoXenero is None or self.filtradoXenero == "None":
            return True
        else:
            return modelo[fila][3] == self.filtradoXenero

    def compara_modelo(self, modelo, fila1, fila2, datoUsuario):
        columna_ordear, _ = modelo.get_sort_column_id() # con esto temos a referencia da columna (3), ponemos la coma barrabaja por que el column id da una tupla, pero solo necesitamos un dato
        edade1 = modelo.get_value(fila1, columna_ordear) # sacamos o edade1 que seria a fila1
        edade2 = modelo.get_value(fila2, columna_ordear) # sacamos o seguinte valor
        if edade1 < edade2:
            return -1 # retornamos valor negativo
        elif edade1 == edade2:
            return 0 # retornamos 2
        elif edade1 > edade2:
            return 1 # retornamos valor positivo





if __name__ == "__main__":
    FiestraPrincipal()
    Gtk.main()