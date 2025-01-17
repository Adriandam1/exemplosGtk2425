import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GLib

#enlaces: https://docs.gtk.org/gtk3/class.ComboBox.html
# https://docs.gtk.org/gtk3/class.Entry.html
# https://lazka.github.io/pgi-docs/Gtk-3.0/classes/Entry.html

class FiestraPrincipal (Gtk.Window):
    def __init__(self):
        super().__init__()

        self.set_title("Exemplo con Gtk ComboBox")

        modelo = Gtk.ListStore(int, str)
        # le damos una coleccion, una TUPLA unha LISTA ou o que queiramos
        # a append temos que pasarlle un elemento de coleccion, que se poda recorrer
        modelo.append((1, "Ana Pérez"))
        modelo.append((12, "Rosa Gómez"))
        modelo.append((13, "Roque Ros"))
        modelo.append((3, "Jose Diz"))

        caixaV = Gtk.Box(orientation= Gtk.Orientation.VERTICAL, spacing = 6)

        cmbNomes = Gtk.ComboBox.new_with_model_and_entry(model = modelo)
        cmbNomes.set_entry_text_column(1)
        cmbNomes.connect("changed", self.on_cmbNomes_changed)
        txtCadroTexto = cmbNomes.get_child()
        txtCadroTexto.connect("activate", self.on_txtCadroTexto_activate, modelo)
        caixaV.pack_start(cmbNomes, False, False, 0)

        modelo_paises = Gtk.ListStore(str)
        paises = ["Portugal", "Irlanda", "Marrocos", "Cabo Verde", "Nepal", "Arabia Saudí"]
        for pais in paises:
            modelo_paises.append((pais,))
        cmbPaises = Gtk.ComboBox.new_with_model(modelo_paises)
            # o equivalente a liña anterior seria:
            # cmbPaises = Gtk.ComboBox()
            # cmbPaises.set_model(modelo_paises)
        celdaTexto = Gtk.CellRendererText()
        cmbPaises.pack_start(celdaTexto, True)
        cmbPaises.add_attribute(celdaTexto, "text", 0)
        cmbPaises.set_active(3) #poñemos un pais por defecto, neste caso o que este no indice 3(Vabo Verde)
        caixaV.pack_start (cmbPaises, False, False, 0)

        #BoxText
        cmbColores = Gtk.ComboBoxText()
        cmbColores.set_entry_text_column(0)
        cmbColores.append_text("Vermello")
        cmbColores.append_text("Azul")
        cmbColores.append_text("Amarelo")
        caixaV.pack_start (cmbColores, False, False, 0)

        #
        modeloIconas = Gtk.ListStore(str, str)
        modeloIconas.append (("Novo", "document-new"))
        modeloIconas.append (("Abrir", "document-open"))
        modeloIconas.append (("Gardar", "document-save"))
        cmbIconas = Gtk.ComboBox()
        cmbIconas.set_model(modeloIconas)
        # Preparamos a celda:
        celdaGraficos = Gtk.CellRendererPixbuf()
        cmbIconas.pack_start(celdaGraficos, True)
        cmbPaises.add_attribute(celdaGraficos, "icon_name", 1)
        caixaV.pack_start(cmbIconas, False, False, 0)







        self.add(caixaV)
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()

    def on_cmbNomes_changed(self, combo):
        fila = combo.get_active_iter()
        if fila is not None:
            modelo = combo.get_model()
            # numero se mete en elemento 0 y nome en elemento 1
            num, nome = modelo [fila][:2]
            # O equivalente seria:
            #num = modelo [fila][0]
            #nome = modelo [fila][1]
            # facemos un preformateo para mostralo e metemods unha tupla coas variables
            print("Seleccionado: Num= %d, nome = %s" % (num, nome))
            # exemplo de execucion: Seleccionado Num= 13, nome = Roque Ros

    # funcion para que nos muestre el nombre cuando lo tecleamos nosotros y lo introduzca la lista
    def on_txtCadroTexto_activate(self, cadroTexto, mod):
        print("Tecleado: %s" % cadroTexto.get_text())
        mod.append ((999, cadroTexto.get_text()))


if __name__ == "__main__":
    FiestraPrincipal()
    Gtk.main()
































