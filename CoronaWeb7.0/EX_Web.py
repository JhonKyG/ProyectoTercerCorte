from datetime import datetime
from os import path
from bs4 import BeautifulSoup
from flask import Flask
from flask import render_template
from xml.dom import minidom
from os import remove
import wget
import requests

def coordenadasCiudades():
    url = "https://www.geodatos.net/coordenadas/colombia"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    eq = soup.find_all('td')
    cordenates = []
    for i in eq:
        cordenates.append(i.text)
    coordenadas = [[], []]
    coordenadas[0] = cordenates[12::2]
    coordenadas[1] = cordenates[13::2]
    array = [[], [], []]
    for i in range(len(coordenadas[1])):
        cadena = coordenadas[1][i]
        separador = ","
        separado = cadena.split()
        separado[0] = separado[0][:-1]
        array[0].append(coordenadas[0][i])
        array[1].append(float(separado[0]))
        array[2].append(float(separado[1]))
    return array

def refresh_path():
    if path.exists('rows.xml'):
        remove('rows.xml')

def download_source():
    url = 'https://www.datos.gov.co/api/views/gt2j-8ykr/rows.xml?accessType=DOWNLOAD'
    filename = wget.download(url)

def xml_parsing():
    docXML = minidom.parse("rows.xml")
    datos = docXML.getElementsByTagName("row")
    lista = [[], [], [], [],[], [], [], [],[], [], [], [],[], [], [], [], []]
    for row in datos:
        try:
            lista[0].append((((row.getElementsByTagName("id_de_caso"))[0]).firstChild.data))
        except:
            lista[0].append('- -')
        try:
            lista[1].append((((row.getElementsByTagName("fecha_de_notificaci_n"))[0]).firstChild.data))
        except:
            lista[1].append('- -')
        try:
            lista[2].append((((row.getElementsByTagName("codigo_divipola"))[0]).firstChild.data))
        except:
            lista[2].append('- -')
        try:
            lista[3].append((((row.getElementsByTagName("ciudad_de_ubicaci_n"))[0]).firstChild.data))
        except:
            lista[3].append('- -')
        try:
            lista[4].append((((row.getElementsByTagName("departamento"))[0]).firstChild.data))
        except:
            lista[4].append('- -')
        try:
            lista[5].append((((row.getElementsByTagName("atenci_n"))[0]).firstChild.data))
        except:
            lista[5].append('- -')
        try:
            lista[6].append((((row.getElementsByTagName("edad"))[0]).firstChild.data))
        except:
            lista[6].append('- -')
        try:
            lista[7].append((((row.getElementsByTagName("sexo"))[0]).firstChild.data))
        except:
            lista[7].append('- -')
        try:
            lista[8].append((((row.getElementsByTagName("tipo"))[0]).firstChild.data))
        except:
            lista[8].append('- -')
        try:
            lista[9].append((((row.getElementsByTagName("estado"))[0]).firstChild.data))
        except:
            lista[9].append('- -')
        try:
            lista[10].append((((row.getElementsByTagName("pa_s_de_procedencia"))[0]).firstChild.data))
        except:
            lista[10].append('- -')
        try:
            lista[11].append((((row.getElementsByTagName("fis"))[0]).firstChild.data))
        except:
            lista[11].append('- -')
        try:
            lista[12].append((((row.getElementsByTagName("fecha_de_muerte"))[0]).firstChild.data))
        except:
            lista[12].append('- -')
        try:
            lista[13].append((((row.getElementsByTagName("fecha_diagnostico"))[0]).firstChild.data))
        except:
            lista[13].append('- -')
        try:
            lista[14].append((((row.getElementsByTagName("fecha_recuperado"))[0]).firstChild.data))
        except:
            lista[14].append('- -')
        try:
            lista[15].append((((row.getElementsByTagName("fecha_reporte_web"))[0]).firstChild.data))
        except:
            lista[15].append('- -')
        try:
            lista[16].append((((row.getElementsByTagName("tipo_recuperaci_n"))[0]).firstChild.data))
        except:
            lista[16].append('- -')
    return lista

app = Flask(__name__, template_folder="vista")#

@app.route('/')
@app.route('/pagina1')

def index():
    refresh_path()
    download_source()
    casos = xml_parsing()
    idCase = len(casos[0])
    #===================================================================================================================
    #Infectdos por ciudad
    ciudad = casos[3]
    array=coordenadasCiudades()
    lista=[]
    listaCaso=[]
    lista.append('Leticia')
    lista.append(-4.2152800)
    lista.append(-69.9405600)
    for i in range(len(array[0])):
        lista.append(array[0][i])
        lista.append(array[1][i])
        lista.append(array[2][i])

    for i in range(len(lista)):
        count=0
        if (type(lista[i]) == str):
            #print(lista[i])
            for j in range(len(casos[0])):
                if(lista[i] in ciudad[j]):
                    count += 1
                    #print(ciudad[j])
        listaCaso.append(count)

    #===================================================================================================================
    #Recuperados por ciudad
    recuperado = casos[5]
    listaRecuperado=[]

    for i in range(len(lista)):
        count=0
        if (type(lista[i]) == str):
            for j in range(len(casos[0])):
                if(recuperado[j] == 'Recuperado'):
                    if(lista[i] in ciudad[j]):
                        count += 1
        listaRecuperado.append(count)
    #===================================================================================================================



    return render_template("pagina1.html", lista=lista, listaCaso=listaCaso, listaRecuperado=listaRecuperado, idCase=idCase)

@app.route('/')
@app.route('/pagina2')

def index1():
    lista = xml_parsing()

    id = lista[0]
    fecha = lista[1]
    divipola = lista[2]
    ubicacion = lista[3]
    departamento = lista[4]
    atencion = lista[5]
    edad = lista[6]
    sexo = lista[7]
    tipo = lista[8]
    estado = lista[9]
    procedencia = lista[10]
    fis= lista[11]
    fechaDeMuerte = lista[12]
    fecha_diagnostico = lista[13]
    fecha_recuperado = lista[14]
    reporte_web = lista[15]
    x = len(id)


    return render_template("pagina2.html", id = id, fecha=fecha, divipola=divipola, Ubicacion= ubicacion, departamento= departamento, atencion= atencion,
                           edad=edad, sexo =sexo, tipo= tipo, estado=estado, procedencia=procedencia, fis=fis, fechaDeMuerte=fechaDeMuerte,
                           fecha_diagnostico=fecha_diagnostico, fecha_recuperado = fecha_recuperado, reporte_web=reporte_web,x=x)

@app.route('/')
@app.route('/pagina3')

def index2():
    count = [0,0,0]
    values = []
    lista = xml_parsing()
    sexo = lista[7]
    #para graficar por genero
    for i in range(len(lista[0])):
        if(sexo[i] == 'f' or sexo[i] == 'F'):
            count[0]+=1
        elif(sexo[i] == 'm' or sexo[i]== 'M'):
            count[1]+=1
        else:
            count[2]+=1

    values.insert(0, count[0])
    values.insert(1, count[1])
    values.insert(2, count[2])
    legend = "Infectados por genero"

    #===================================================================================================================
    #para graficar por intervalos de edad
    values2=[0,0,0,0,0,0,0,0,0,0]
    edad = lista[6]
    for i in range(len(lista[0])):
        if(edad[i] != '- -'):
            if(int(edad[i]) <= 10):
                values2[0]+=1
            elif(int(edad[i])>10 and int(edad[i])<=20):
                values2[1]+=1
            elif(int(edad[i])>20 and int(edad[i])<=30):
                values2[2]+=1
            elif(int(edad[i])>30 and int(edad[i])<=40):
                values2[3]+=1
            elif(int(edad[i])>40 and int(edad[i])<=50):
                values2[4]+=1
            elif(int(edad[i])>50 and int(edad[i])<=60):
                values2[5]+=1
            elif(int(edad[i])>60 and int(edad[i])<=70):
                values2[6]+=1
            elif(int(edad[i])>70 and int(edad[i])<=80):
                values2[7]+=1
            elif(int(edad[i])>80 and int(edad[i])<=90):
                values2[8]+=1
            elif(int(edad[i])>90 and int(edad[i])<=100):
                values2[9]+=1

    legend2 = "Infectados por rango de edad"
    #===================================================================================================================
    values3 = [0, 0, 0, 0, 0, 0]
    fecha_contagio = lista[13]
    id = lista[0]
    for i in range(len(id)):
        try:
            mes = datetime.fromisoformat(fecha_contagio[i])
            if(mes.strftime('%m') == '03'):
                values3[2] += 1
            elif(mes.strftime('%m') == '04'):
                values3[3] += 1
            elif(mes.strftime('%m') == '05'):
                values3[4] += 1
            elif(mes.strftime('%m') == '06'):
                values3[5]+=1
        except:
            c=1

    legend3 = 'Infectados diagnosticados por mes'
    labels2 = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio"]
    #===================================================================================================================
    #estado de los infectados
    values4 = [0, 0, 0, 0, 0]
    atencion = lista[5]
    for i in range(len(atencion)):
        if (atencion[i] != '- -'):
            if (atencion[i] == 'Casa'):
                values4[0] += 1
            elif (atencion[i] == 'Fallecido'):
                values4[1] += 1
            elif (atencion[i] == 'Hospital UCI'):
                values4[2] += 1
            elif (atencion[i] == 'Recuperado'):
                values4[3] += 1
            elif (atencion[i] == 'Hospital'):
                values4[4] += 1

    legend4 = 'Estado de los pacientes infectados en Colombia'
    labels3 = ['Casa','Fallecido','Hospital UCI','Recuperado','Hospital']
    #===================================================================================================================
    #contagiados y recuperados
    values5 = [values4[3],(values4[0]+values4[1]+values4[2])]
    #===================================================================================================================
    #recuperados por mes
    values6 = [0, 0, 0, 0, 0, 0]
    fecha_recuperado = lista[14]
    id6 = lista[0]
    for i in range(len(id6)):
        try:
            mes2 = datetime.fromisoformat(fecha_recuperado[i])
            if (mes2.strftime('%m') == '03'):
                values6[2]+=1
            elif (mes2.strftime('%m') == '04'):
                values6[3]+=1
            elif (mes2.strftime('%m') == '05'):
                values6[4]+=1
            elif (mes2.strftime('%m') == '06'):
                values6[5]+=1
        except:
            pollo = 1

    legend6 = 'Recuperados por mes'
    labels6 = ["Enero", "Febrero", "Marzo", "Abril", "Mayo","Junio"]
    #===================================================================================================================
    #casos importados, relacionados o en investigacion
    values7 = [0,0,0]
    tipo = xml_parsing()[8]
    id7 = xml_parsing()[0]
    for i in range(len(id7)):
        if tipo[i] != "- -":
            if tipo[i] == "Importado":
                values7[0]+=1
            elif tipo[i] == "Relacionado":
                values7[1]+=1
            elif tipo[i] == "En estudio":
                values7[2]+=1

    legend7 = 'Tipo de infeccion'
    labels7 = ["Importado", "Relacionado", "En estudio"]


    return render_template("pagina3.html", legend=legend,labels2=labels2, labels3=labels3, legend2=legend2,legend3=legend3,
                           legend4=legend4, values=values,values2=values2, values3=values3, values4=values4, values5=values5,
                           labels6=labels6, legend6=legend6, values6=values6, labels7=labels7, legend7=legend7, values7=values7)

@app.route('/')
@app.route('/pagina4')

def index3():

    return render_template("pagina4.html")

if __name__ == "__main__":
    app.run(debug = True,port=7500)#debug permite cambios en python