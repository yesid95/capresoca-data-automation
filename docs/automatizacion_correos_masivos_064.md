# Automatización de Correos Masivos (Decreto 064)

## Descripción General
Este documento describe el proceso automatizado implementado en el notebook `Correos_Maxivos 064.ipynb`. El objetivo principal es notificar masivamente a los afiliados sobre la aplicación de la novedad de **Movilidad al Régimen Subsidiado** en cumplimiento del Decreto 064 de 2020.

El script genera y envía correos electrónicos personalizados a cada afiliado y, adicionalmente, crea archivos PDF de respaldo por municipio que consolidan todas las notificaciones enviadas, sirviendo como evidencia de la gestión.

## Tecnologías Utilizadas
*   **Python 3.x**
*   **Pandas**: Para la manipulación de bases de datos de afiliados y contactos.
*   **Smtplib / Win32com**: Para el envío de correos electrónicos (soporta tanto SMTP directo como automatización de Outlook).
*   **WeasyPrint**: Para la generación de archivos PDF a partir de contenido HTML.
*   **Email.mime**: Para la construcción de correos con formato HTML e imágenes incrustadas.

## Entradas y Salidas

### Entradas (Inputs)
1.  **Archivos de Movilidad (.VAL)**:
    *   Ubicación: `R_Automatico_S1`
    *   Contenido: Archivos planos con la información de los afiliados procesados por movilidad automática.
2.  **Base de Contacto SIE (`R_MS_SIE`)**:
    *   Formato: `.csv`
    *   Contenido: Correos electrónicos y teléfonos de los afiliados.
3.  **Base Sisbén (`R_Sisben`)**:
    *   Formato: `.xlsx`
    *   Contenido: Información de contacto alternativa (email) del Sisbén.
4.  **Red de Servicios (`R_Red_Servicios`)**:
    *   Formato: `.csv`
    *   Contenido: Asignación de IPS de Medicina General y Odontología por afiliado.
5.  **Códigos DANE (`R_Municipios`)**:
    *   Formato: `.txt`
    *   Contenido: Homologación de códigos de municipios.

### Salidas (Outputs)
1.  **Correos Electrónicos**:
    *   Enviados directamente a los afiliados.
    *   Contenido: Carta personalizada informando la movilidad y la red de servicios asignada.
2.  **Archivos PDF por Municipio**:
    *   Ubicación: `SAVE_DIR`
    *   Formato: `Correo_{Municipio}_{NombreArchivo}.pdf`
    *   Contenido: Compendio de todas las cartas enviadas a los afiliados de ese municipio, generadas como evidencia documental.
3.  **Archivo Consolidado de Usuarios (`User_Df.TXT`)**:
    *   Archivo plano con la información final procesada de los usuarios notificados.

## Lógica del Proceso

### 1. Carga y Consolidación de Datos
*   Se leen todos los archivos `.VAL` de la carpeta de movilidad y se concatenan.
*   Se cruza con la tabla de municipios para obtener nombres legibles.
*   Se filtra por la EPS (`EPS025`) y departamento (`85` - Casanare).

### 2. Gestión de Correos Electrónicos
*   **Cruce SIE**: Se busca el correo electrónico en la base de datos SIE.
*   **Limpieza**: Se eliminan correos inválidos (e.g., "notiene", "sincorreo", "actualizar").
*   **Recuperación Sisbén**: Para los registros sin correo en SIE, se busca en la base del Sisbén.
*   **Corrección**: Se aplica una función para corregir errores comunes (e.g., espacios, puntos al final de ".com").

### 3. Asignación de Red de Servicios
*   Se cruza con el archivo de Red de Servicios para obtener la IPS asignada para:
    *   Medicina General.
    *   Odontología General.
*   Se realiza un `pivot` de la tabla de red para tener una fila por afiliado con columnas separadas por servicio.

### 4. Envío de Correos
*   Se utiliza una plantilla HTML (`EMAIL_TEMPLATE`) que incluye:
    *   Logo de Capresoca y firma del funcionario.
    *   Datos variables: Nombre, Documento, Municipio, IPS asignadas.
    *   Texto legal citando el Decreto 064 de 2020.
*   El envío se puede configurar vía **Outlook** (Win32com) o **SMTP** estándar.

### 5. Generación de Evidencia PDF
*   Se agrupan los registros por municipio.
*   Para cada municipio, se genera un único PDF que contiene las cartas de todos los afiliados de ese grupo.
*   Se usa `WeasyPrint` para renderizar el HTML (con imágenes locales) a PDF.

## Variables Clave
*   `Asunto`: Asunto del correo (e.g., "NOTIFICACION MOVILIDAD...").
*   `Fecha_Documento`: Fecha que aparece en el cuerpo de la carta.
*   `USE_WIN32COM`: Booleano para alternar entre envío por Outlook (True) o SMTP (False).
