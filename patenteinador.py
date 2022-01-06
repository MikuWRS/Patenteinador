#!/usr/bin/python3

from bs4 import BeautifulSoup
from texttable import Texttable
from pwn import *
import sys,signal,requests,time,re,csv,pdb


def def_handler(sig,frame):
	print("\n[!] Saliendo...\n")
	sys.exit(1)

#ctrl+c
signal.signal(signal.SIGINT, def_handler)

# variables globales
url = "https://www.patentechile.com/resultados"
headers ={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 OPR/82.0.4227.50'}

def imprimir(datos):
	t = Texttable()
	t.add_rows([['RUT','Nombre'],[datos["rut"],datos["nombre"]]])
	print(t.draw())
	t2 = Texttable()
	t2.add_rows([['Patente','Tipo','Marca','Modelo','Año','Color'],[datos["patente"],datos["tipo"],datos["marca"],datos["modelo"],datos["ano"],datos["color"]]])
	print(t2.draw())

def exportar_datos(datos):
	multiples = True if "-l" in sys.argv else False
	
	if(multiples):
		data = [datos["rut"],datos["nombre"],datos["patente"],datos["tipo"],datos["marca"],datos["modelo"],datos["ano"],datos["color"]]
		with open('resultados.csv','a',encoding='UTF-8') as r:
			writer = csv.writer(r)
			writer.writerow(data)
	else:
		header = ['RUT', 'Nombre', 'Patente','Tipo','Marca','Modelo','Año','Color']
		data = [datos["rut"],datos["nombre"],datos["patente"],datos["tipo"],datos["marca"],datos["modelo"],datos["ano"],datos["color"]]
		with open('resultados.csv','w',encoding='UTF-8') as r:
			writer = csv.writer(r)
			writer.writerow(header)
			writer.writerow(data)


def resultados(res):
	exportar = True if "-e" in sys.argv else False
	
	tr = res.find_all('tr')
	if(tr):
		rut = tr[1].find_all('td');nombre = tr[2].find_all('td')
		patente = tr[5].find_all('td');tipo = tr[6].find_all('td');marca = tr[7].find_all('td')
		modelo = tr[8].find_all('td');ano = tr[9].find_all('td');color = tr[10].find_all('td')
		datos = {
			"rut":rut[1].get_text(),"nombre":nombre[1].get_text(),
			"patente":patente[1].get_text(),"tipo":tipo[1].get_text(),"marca":marca[1].get_text(),
			"modelo":modelo[1].get_text(),"ano":ano[1].get_text(),"color":color[1].get_text()
		}

		if(exportar):
			exportar_datos(datos)
		else:
			imprimir(datos)
		return(1)
	else:
		return(0)

def consulta(payload):
	s = requests.Session()
	res = s.post(url,data=payload,headers=headers)
	#time.sleep(1)
	return(resultados(BeautifulSoup(res.text,'lxml')))

def main():
	p1 = log.progress("Recopilando informacion")

	if("-p" in sys.argv):
		i = sys.argv.index("-p")
		patente = sys.argv[i+1]
		if(re.search('^[A-Z,a-z]{4}[0-9]{2}$',patente) or re.search('^[A-Z,a-z]{2}[0-9]{4}$',patente)):
			payload = {'frmTerm':patente,'frmOpcion':'vehiculo'}
			consulta(payload)
		elif(re.search('^[A-Z,a-z]{2}[0-9]{3}$',patente) or re.search('^[A-Z,a-z]{3}[0-9]{2}$',patente)):
			payload = {'frmTerm':patente.rstrip("\n"),'frmOpcion':'moto'}
			consulta(payload)
		else:
			print(f"El formato de {patente} no coincide\n")
	elif("-l" in sys.argv):
		p1.status("Probando patentes multiples")
		i = sys.argv.index("-l")
		patentes = open(sys.argv[i+1],"r")
		header = ['RUT', 'Nombre', 'Patente','Tipo','Marca','Modelo','Año','Color']
		with open('resultados.csv','w',encoding='UTF-8') as r:
			writer = csv.writer(r)
			writer.writerow(header)
		for patente in patentes:
			if(re.search('^[A-Z,a-z]{4}[0-9]{2}$',patente) or re.search('^[A-Z,a-z]{2}[0-9]{4}$',patente)): #AABB00
				payload = {'frmTerm':patente.rstrip("\n"),'frmOpcion':'vehiculo'}
				if(consulta(payload) == 1):
					print(f" Lista {patente}")
				else:
					print(f" Error {patente}")
			elif(re.search('^[A-Z,a-z]{2}[0-9]{3}$',patente) or re.search('^[A-Z,a-z]{3}[0-9]{2}$',patente)): #AA000
				payload = {'frmTerm':patente.rstrip("\n"),'frmOpcion':'moto'}
				if(consulta(payload) == 1):
					print(f" lista {patente}")
				else:
					print(f" Error {patente}")
			else:
				print(f"El formato de {patente} no coincide\n")
	elif("-h" in sys.argv):
		print("Modo de uso:\n python3 "+sys.argv[0]+" -command patente/lista")
		print("Command:\n\t-p Patente\n\t-l Lista\n\t-e Exportar en csv\n\t-h Help")
		print("Example: python3 "+sys.argv[0]+" -p 'aabb00' \n")
		print("Example: python3 "+sys.argv[0]+" -l list.txt -e\n")
		sys.exit(1)
	else:
		print("Modo de uso:\n python3 "+sys.argv[0]+" -command patente/lista")
		print("Command:\n\t-p Patente\n\t-l Lista\n\t-e Exportar en csv\n\t-h Help")
		print("Example: python3 "+sys.argv[0]+" -p 'aabb00' \n")
		print("Example: python3 "+sys.argv[0]+" -l list.txt -e\n")
		sys.exit(1)
if __name__ == '__main__':
	main()