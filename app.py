from sqlalchemy import create_engine, Column, Integer, String, CheckConstraint
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError, OperationalError

Base = declarative_base()

# ------------------------------------------------------------
# Modelo ORM
# ------------------------------------------------------------
class Libro(Base):
    __tablename__ = "libros"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(100), nullable=False)
    autor = Column(String(100), nullable=False)
    genero = Column(String(50), nullable=False)
    estado = Column(String(20), nullable=False)

    __table_args__ = (
        CheckConstraint("estado IN ('Leído','No leído')", name="check_estado"),
    )

    def __repr__(self):
        return f"<Libro {self.id} - {self.titulo} ({self.estado})>"


# ------------------------------------------------------------
# Conexión a la base de datos (SQLAlchemy + PyMySQL)
# ------------------------------------------------------------
def crear_sesion():
    try:
        # Ajusta tus credenciales aquí
        usuario = "root"
        contrasena = "1234"
        host = "localhost"
        base_datos = "biblioteca_db"

        cadena_conexion = f"mysql+pymysql://{usuario}:{contrasena}@{host}/{base_datos}"
        engine = create_engine(cadena_conexion, echo=False)

        # Crear tablas si no existen
        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        return Session()

    except OperationalError:
        print("❌ Error: No se pudo conectar a la base de datos.")
        print("   Verifica el servidor de MariaDB/MySQL y tus credenciales.")
        exit()

    except Exception as e:
        print(f"❌ Error inesperado al conectar: {e}")
        exit()


# ------------------------------------------------------------
# CRUD
# ------------------------------------------------------------
def agregar_libro(session):
    print("=== Agregar nuevo libro ===")
    titulo = input("Título: ")
    autor = input("Autor: ")
    genero = input("Género: ")
    estado = input("Estado (Leído/No leído): ")

    libro = Libro(titulo=titulo, autor=autor, genero=genero, estado=estado)
    session.add(libro)

    try:
        session.commit()
        print("✔ Libro agregado correctamente.\n")
    except SQLAlchemyError as e:
        session.rollback()
        print("❌ Error al agregar libro:", e)


def actualizar_libro(session):
    ver_libros(session)
    id_libro = input("ID del libro a actualizar: ")

    libro = session.get(Libro, id_libro)
    if not libro:
        print("⚠ No existe un libro con ese ID.\n")
        return

    libro.titulo = input("Nuevo título: ")
    libro.autor = input("Nuevo autor: ")
    libro.genero = input("Nuevo género: ")
    libro.estado = input("Nuevo estado (Leído/No leído): ")

    try:
        session.commit()
        print("✔ Libro actualizado correctamente.\n")
    except SQLAlchemyError as e:
        session.rollback()
        print("❌ Error al actualizar:", e)


def eliminar_libro(session):
    ver_libros(session)
    id_libro = input("ID del libro a eliminar: ")

    libro = session.get(Libro, id_libro)
    if not libro:
        print("⚠ Libro no encontrado.\n")
        return

    try:
        session.delete(libro)
        session.commit()
        print("✔ Libro eliminado.\n")
    except SQLAlchemyError as e:
        session.rollback()
        print("❌ Error al eliminar:", e)


def ver_libros(session):
    libros = session.query(Libro).all()
    print("\n======= LISTA DE LIBROS =======")

    if not libros:
        print("No hay libros registrados.\n")
        return

    for libro in libros:
        print(
            f"ID: {libro.id} | Título: {libro.titulo} | "
            f"Autor: {libro.autor} | Género: {libro.genero} | Estado: {libro.estado}"
        )
    print()


def buscar_libros(session):
    campo = input("Buscar por (titulo/autor/genero): ").lower()

    if campo not in ["titulo", "autor", "genero"]:
        print("⚠ Campo inválido.\n")
        return

    termino = input("Ingrese el término a buscar: ")

    filtro = getattr(Libro, campo).like(f"%{termino}%")
    resultados = session.query(Libro).filter(filtro).all()

    if not resultados:
        print("No se encontraron coincidencias.\n")
        return

    print("\n=== Resultados ===")
    for libro in resultados:
        print(
            f"ID: {libro.id} | Título: {libro.titulo} | "
            f"Autor: {libro.autor} | Género: {libro.genero} | Estado: {libro.estado}"
        )
    print()


# ------------------------------------------------------------
# Menú principal
# ------------------------------------------------------------
def menu():
    session = crear_sesion()

    while True:
        print("========= MENÚ BIBLIOTECA =========")
        print("1. Agregar libro")
        print("2. Actualizar libro")
        print("3. Eliminar libro")
        print("4. Ver libros")
        print("5. Buscar libros")
        print("6. Salir")
        print("===================================")

        opcion = input("Seleccione una opción: ")
        print()

        if opcion == "1":
            agregar_libro(session)
        elif opcion == "2":
            actualizar_libro(session)
        elif opcion == "3":
            eliminar_libro(session)
        elif opcion == "4":
            ver_libros(session)
        elif opcion == "5":
            buscar_libros(session)
        elif opcion == "6":
            print("Saliendo del programa...")
            session.close()
            break
        else:
            print("⚠ Opción inválida.\n")


# ------------------------------------------------------------
# Ejecución principal
# ------------------------------------------------------------
if __name__ == "__main__":
    menu()
