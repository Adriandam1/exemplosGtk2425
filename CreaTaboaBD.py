from conexionBD import ConexionBD

"""
Esta clase utiliza conexionDB para crear bases de datos, tablas y posibilita inxerir datos nelas,
HAY QUE CAMBIARLA PARA CADA PROGRAMA LOGICAMENTE
"""
class CreaTaboaBD:
    def __init__(self):
        self.ruta_bd = "bdListinTelefonico.dat"
        self.crea_taboa()
        self.insere_datos()

    def crea_taboa(self):
        # Crear la tabla si no existe
        bDatos = ConexionBD(self.ruta_bd)
        bDatos.conectaBD()
        bDatos.creaCursor()
        bDatos.consultaSenParametros("""
        CREATE TABLE IF NOT EXISTS listaTelefonos (
            Nome TEXT,
            Apelido TEXT,
            NumeroDeTelefono TEXT
        )
        """)
        bDatos.pechaBD()

    def insere_datos(self):
        """Insertar datos en la tabla listaTelefonos."""
        bDatos = ConexionBD(self.ruta_bd)
        bDatos.conectaBD()  # Conectamos a la base de datos
        bDatos.creaCursor()

        # Datos a insertar
        axendaTelefonica = [
            ["Pepe", "Pérez", "986 543 210"],
            ["Ana", "Alonso", "986 345 678"],
            ["Rosa", "Vila", "621 432 567"],
            ["Jose", "Diaz", "657 890 012"]
        ]
        # Insertamos los datos en la base de datos
        for usuario in axendaTelefonica:
            bDatos.consultaConParametros("""
            INSERT INTO listaTelefonos (Nome, Apelido, NumeroDeTelefono)
            VALUES (?, ?, ?)
            """, usuario[0], usuario[1], usuario[2])
            bDatos.conexion.commit() #hai que poñer commit para que os datos se carguen
        bDatos.pechaBD()  # Cerramos la conexión



if __name__ == "__main__":
    # Crear la tabla
    creaTaboa = CreaTaboaBD()

