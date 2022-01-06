# Patenteinador
Patenteinador es un script en Python3 que permite la busqueda de datos de patentes chilenas por medio de la pagina https://www.patentechile.com

# Instalacion
```bash
git clone https://github.com/MikuWRS/Patenteinador
cd Patenteinador
pip install -r requirements.txt
```

# Modo de Uso:
```bash
python3 patenteinador.py -comandos "patente"
```
Comandos:
- -p "patente"
- -e Exportar a csv
- -l Lista de patentes
- -h Help

Ejemplos
```bash
python3 patenteinador.py -p "aabb00"
python3 patenteinador.py -p "aabb00" -e
python3 patenteinador.py -l lista.txt
python3 patenteinador.py -l lista.txt -e
```
# Notas/Issues
- Por algun motivo si se utiliza el parametro "-p" junto con una patente en mayusculas, sys.argv no reconoce el string de la patente.
Ejemplo
```bash
python3 patenteinador.py -p "AABB00" -e

[◐] Recopilando informacion
El formato de -e no coincide
```
Sin embargo si la lista posee las patentes en mayusculas no ocurre este error.

- Dado el modo de lectura de los argumentos, es recomendable NO ejecutar el programa de esta forma
```bash
python3 patenteinador.py -p -e "AABB00" 
```
El programa fallara.
