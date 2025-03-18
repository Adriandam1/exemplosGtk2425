import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import sqlite3 as dbapi

from conexionBD import ConexionBD

class FiestraPrincipal (Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Exemplo previo")

        caixaV = Gtk.Box (orientation = Gtk.Orientation.VERTICAL, spacing= 6)
        grid = Gtk.Grid()

        lblNumeroAlbara = Gtk.Label(label ="Número de albará")
        lblData = Gtk.Label(label = "Data")
        lblDataEntrega = Gtk.Label(label = "Data de entrega")
        lblNumeroCliente = Gtk.Label(label = "Número de cliente")
        lblNomeCliente = Gtk.Label(label = "Nome de cliente")
        lblApelidosCliente = Gtk.Label(label = "Apelidos de cliente")

        self.cmbNumeroAlbara = Gtk.ComboBoxText()
        self.txtDataAlbara = Gtk.Entry()
        self.txtDataEntrega = Gtk.Entry()
        self.txtNumeroCliente = Gtk.Entry()
        self.txtNomeCliente = Gtk.Entry()
        self.txtApelidosCliente = Gtk.Entry()

        # todos os elementos que engadimos ao grid
        grid.add(lblNumeroAlbara)
        grid.attach_next_to(self.cmbNumeroAlbara, lblNumeroAlbara, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(lblData, self.cmbNumeroAlbara, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(self.txtDataAlbara, lblData, Gtk.PositionType.RIGHT, 1, 1)
        # engadimos a segunda fila
        grid.attach_next_to(lblNumeroCliente, lblNumeroAlbara, Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(self.txtNumeroCliente, lblNumeroCliente, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(lblDataEntrega, self.txtNumeroCliente, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(self.txtDataEntrega, lblDataEntrega, Gtk.PositionType.RIGHT, 1, 1)
        #Tecerda fila
        grid.attach_next_to(lblNomeCliente, lblNumeroCliente, Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(self.txtNomeCliente, lblNomeCliente, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(lblApelidosCliente, self.txtNomeCliente, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(self.txtApelidosCliente, lblApelidosCliente, Gtk.PositionType.RIGHT, 1, 1)



        caixaV.pack_start(grid, True, True, 0)


        #Creamos a conexion a base de datos, para eso utilizamos a clase ConexionBD
        conBD = ConexionBD("modelosClasicos.dat")
        # facemos os pasos que teriamos que facer unha conexion a base de datos
        conBD.conectaBD()
        conBD.creaCursor()
        #-------------------

        numerosAlbaras = conBD.consultaSenParametros("Select numeroAlbara from ventas")# esta libreria voltaba unha lista e llepasabamos o sql
        # teño que pasarllos o combo, para ello teño que facer un listStore, poderiamos facer un combo text pero vamos a facer un modelo e asi nos lembramos como se usaba
        modeloCmbAlbaran = Gtk.ListStore(int)
        # consulta unha lista, temos que recorrer a lista e usar os datos que os dan
        for numero in numerosAlbaras:
            print (numero)
            modeloCmbAlbaran.append(numero)
            #modeloCmbAlbaran.append((str(numero[0]),)) # int convertido a string e o meto a unha tupla para que o poida engadir
        self.cmbNumeroAlbara.set_model(modeloCmbAlbaran)
        celda = Gtk.CellRendererText() # celda que vai a ter o combo
        self.cmbNumeroAlbara.pack_start(celda, True)
        self.cmbNumeroAlbara.set_active(0) # seleccionamos o primeiro elemento
        #self.cmbNumeroAlbara.connect("changed", self.on_cmbNumeroAlbara_changed)


        # engadimos botons
        caixaBotons = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing =2)
        self.btnEngadir = Gtk.Button(label = "Engadir")
        self.btnEditar = Gtk.Button(label = "Editar")
        self.btnBorrar = Gtk.Button(label = "Borrar")
        self.btnEngadir.connect("clicked", self.on_btnEngadir_clicked)
        #self.btnEditar.connect("clicked", self.on_btnEditar_clicked)
        #self.btnBorrar.connect("clicked", self.on_btnBorrar_clicked)
        caixaBotons.pack_start(self.btnEngadir, False, False, 2)
        caixaBotons.pack_start(self.btnEditar, False, False, 2)
        caixaBotons.pack_start(self.btnBorrar, False, False, 2)
        caixaV.pack_start(caixaBotons, False, False, 0)

        # --------------------
        # engadimos a lista de albarans
        self.txtCodigoProduto = Gtk.Entry()
        self.txtCantidade = Gtk.Entry()
        self.txtPrezoUnitario = Gtk.Entry()
        caixaCamposAlbaran = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing = 2)
        caixaCamposAlbaran.pack_start(self.txtCodigoProduto, True, False, 2)
        caixaCamposAlbaran.pack_start(self.txtCantidade, True, False, 2)
        caixaCamposAlbaran.pack_start(self.txtPrezoUnitario, True, False, 2)

        caixaV.pack_start(caixaCamposAlbaran, False, False, 0)

        # engadimos a lista de albarans a un TreeView
        self.trvDetalleAlbara = Gtk.TreeView()
        self.modeloDetalleAlbara = Gtk.ListStore(str, str, int, float)
        # hicimos un set active arribe para seleccionar el primer elemento de la lista de albaranes

        # elemento que nos apunte o elemento que esta seleccionado
        punteiro = self.cmbNumeroAlbara.get_active()
        numAlbara = modeloCmbAlbaran [punteiro][0]
        detalleVentas = conBD.consultaConParametros(
            "Select codigoProduto, cantidade, prezoUnitario from detalleVentas where numeroAlbaran = ?",
            numAlbara
        )
        # para preparar o que vamos a mostrar temos que facer un bucle para recorrer a lista de detalleVentas
        #detVentas = []
        for detalle in detalleVentas:
            #lanzo unha consulta para recuperar o nome do produto
            nomeProduto = conBD.consultaConParametros("Select nomeProduto from Produtos where codigoProduto = ?",
                                                      detalle[0].strip()) # empregamos strip para asegurarnos que non hai espazos
            # creo lista cos 3 elementos de detalle e logo lle meto o nome do produto en medio para elaborar a liña
            listaDetalle = list(detalle)
            #introduzo os elementos
            listaDetalle.insert(1, nomeProduto[0][0])
            self.modeloDetalleAlbara.append(listaDetalle)

        self.trvDetalleAlbara.set_model(self.modeloDetalleAlbara)
        #self.seleccion = self.trvDetalleAlbara.SelectionModel()
        caixaV.pack_start(self.trvDetalleAlbara, False, False, 2)

        # engadimos as columnas
        # engadimos a columna de codigo de produto
        celda = Gtk.CellRendererText()
        columna = Gtk.TreeViewColumn("Cod produto", celda, text = 0) # 0 e a columna do modelo que vai a representar
        self.trvDetalleAlbara.append_column(columna)
        # engadimos a columna de nome de produto
        celda = Gtk.CellRendererText()
        columna = Gtk.TreeViewColumn("Produto", celda, text = 1)
        self.trvDetalleAlbara.append_column(columna)
        # engadimos a columna de cantidade
        celda = Gtk.CellRendererText()
        columna = Gtk.TreeViewColumn("Cantidade", celda, text = 2)
        self.trvDetalleAlbara.append_column(columna)
        # engadimos a columna de prezo unitario
        celda = Gtk.CellRendererText()
        columna = Gtk.TreeViewColumn("Prezo Unitario", celda, text = 3)
        self.trvDetalleAlbara.append_column(columna)

        # por ultimo creamos un boton aceptar que iria abaixo e un cancelar
        caixaBtnAceptar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
        self.btnAceptar = Gtk.Button(label = "Aceptar")
        self.btnAceptar.connect ("clicked", self.on_btnAceptar_clicked)
        caixaBtnAceptar.pack_start(self.btnAceptar, False, False, 2)
        caixaBtnCancelar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
        self.btnCancelar = Gtk.Button(label = "Cancelar")
        #self.btnCancelar.connect ("clicked", self.on_btnCancelar_clicked)
        caixaBtnCancelar.pack_start(self.btnCancelar, False, False, 2)
        # esta caixa a engadimos a caixaV
        caixaV.pack_start(caixaBtnAceptar, False, False, 2)
        caixaV.pack_start(caixaBtnCancelar, False, False, 2)




        # -----------------------
        # Configuración de la ventana
        self.add(caixaV)
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()
        # ocultamos os campos de codigo de produto, cantidade e prezo unitario
        self.txtCodigoProduto.set_visible(False)
        self.txtCantidade.set_visible(False)
        self.txtPrezoUnitario.set_visible(False)
        #
        self.operacion = None


    def on_btnEngadir_clicked(self, boton):
        self.operacion = "Engadir"
        self.mostrarControis (True)
        self.bloquearBotons (True)
        self.bloquearBotonsEdicion(False)
        self.limparControis()

    def mostrarControis(self, opcion):
        self.txtCodigoProduto.set_visible(opcion)
        self.txtCantidade.set_visible(opcion)
        self.txtPrezoUnitario.set_visible(opcion)

    def bloquearBotons(self, opcion):
        self.btnAceptar.set_sensitive(opcion)
        self.btnCancelar.set_sensitive (opcion)

    def bloquearBotonsEdicion(self, opcion):
        self.btnEditar.set_sensitive (opcion)
        self.btnEngadir.set_sensitive (opcion)
        self.btnBorrar.set_sensitive (opcion)

    def limparControis(self):
        self.txtCodigoProduto.set_text('')
        self.txtCantidade.set_text('')
        self.txtPrezoUnitario.set_text('')

    def on_btnAceptar_clicked(self, boton):
        if self.operacion == 'Engadir':
            conBD = ConexionBD ('modelosClasicos.dat')
            conBD.conectaBD()
            conBD.creaCursor()
            linhas = conBD.consultaConParametros("""Select numeroLinhaAlbaran from detalleVentas where numeroAlbaran = ?""",
                                                 self.cmbNumeroAlbara.get_model() [self.cmbNumeroAlbara.get_active()][0]) # esto seria file e columna
            numLinha = 0
            # recorremos as linhas para atopar a mais alta
            for linha in linhas:
                if linha[0] > numLinha:
                    numLinha = linha[0]
            numLinha =+ numLinha # incrementamos en 1 o numero de linea

            # ATENCION ESTA PARTE FUNCIONA PERO DA ERROR, HAY QUE REVISAR
            conBD.engadeRexistro("""Insert Into detalleVentas (numeroAlbaran, codigoProduto, cantidade, prezoUnitario, numeroLinhaAlbaran)
                                                Values (?,?,?,?,?)""",
                                 self.cmbNumeroAlbara.get_model()[self.cmbNumeroAlbara.get_active()][0],
                                 self.txtCodigoProduto.get_text(),
                                 int(self.txtCantidade.get_text()),
                                 float(self.txtPrezoUnitario.get_text()),
                                 numLinha)
            nomeProduto = conBD.consultaConParametros("Select nomeProduto from Produtos where codigoProduto = ?",
                                                      self.txtCodigoProduto.get_text())
            conBD.pechaBD() # pecho a base de datos
            # agora temos que engadir os elementos unha nova liña
            self.modeloDetalleAlbara.append(
                self.txtCodigoProduto.get_text(),
                nomeProduto[0][0],
                int(self.txtCantidade.get_text()),
                float(self.txtPrezoUnitario.get_text())
            )














if __name__ == "__main__":
    FiestraPrincipal()
    Gtk.main()













"""
        try:
            bbdd = dbapi.connect ("modelosClasicos.dat")
            print("Conexión a base de datos realizada")
            cursor = bbdd.cursor()
            cursor.execute ("SELECT * FROM listaTelefonos")
            for rexistro in cursor:
                modelo.append(rexistro)
            cursor.close()
            bbdd.close()
        except dbapi.StandardError as e:
            print("Erro o cargar o listStore "+e)
        except dbapi.DatabaseError as e:
            print(e)
"""


























