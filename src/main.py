from src.file_loader import cargar_maestro_ADRES


def main():
    print("Bienvenido a Capresoca Data Automation")
    # Aquí puedes agregar lógica para interactuar con los módulos
    # Por ejemplo, cargar un maestro y mostrar los primeros registros
    ruta_maestro = input("Ingrese la ruta del archivo maestro: ")
    maestro = cargar_maestro_ADRES(ruta_maestro)
    if maestro is not None:
        print("Primeros registros del maestro cargado:")
        print(maestro.head())
    else:
        print("No se pudo cargar el archivo maestro.")


if __name__ == "__main__":
    main()
