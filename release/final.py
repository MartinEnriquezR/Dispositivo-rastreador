import RPi.GPIO as GPIO #librerias de Raspberry Pi GPIO
import serial, time, re #librerias de python
from datetime import datetime, timedelta #librerias de tiempo
import time #libreria de tiempo


servidor = 'http://backend-upiita.herokuapp.com/alerta/publicar-alternativo/?'
servidor_desactivacion = 'http://backend-upiita.herokuapp.com/alerta/desactivacion-alternativo/?'
port = "/dev/ttyS0" #direccion del puerto serial
numero_serie = 400 #numero de serie del dispositivo rastreador
nombre_alerta = '' #nombre de la alerta
fecha_hora_inicio = '' #fecha de inicio de la alerta
push_button = 40


def borrarInformacionAlerta(): #borrar la informacion de la alerta
    global nombre_alerta
    global fecha_hora_inicio
    nombre_alerta = ''
    fecha_hora_inicio = ''
#channel
def alerta():
    
    print('---Envio de la primera ubicacion---')
    modulo.enviarInformacion() # enviar la primera ubicacion [~20 seg]

    while True: 
        time.sleep(240) #esperar 4 minutos para enviar la siguiente ubicacion
        estado_alerta = modulo.alertaDesactivada() #verificar si la alerta fue desactivada [~20 seg]
        print('*****Estado de la alerta: ' + str(estado_alerta) + ' *****')
        if estado_alerta == False:
            borrarInformacionAlerta() #borrar la informacion de la alerta
            break #salir del bucle y de la funcion
        else:
            modulo.enviarInformacion() #enviar la siguiente ubicacion [~20 seg]

    print('---Fin de la alerta---')

class SIM808:
    """funcion para enviar comandos AT"""
    def comando(self,comando,patron,limite):
        ejecucion = True
        while ejecucion == True:
            conteoRespuestas = 0
            respuestasRecibidas = ''
            mensaje = bytes('{}\r'.format(comando),encoding='utf-8') #generar el comando
            print('Comando: {} ingresado'.format(mensaje))
            ser.write(mensaje)
            while conteoRespuestas < limite:
                try:
                    respuesta = ser.readline() #leer la respuesta
                    respuestasRecibidas += respuesta.decode('utf-8') #decodificar a utf-8
                    print(f'^^^{respuestasRecibidas}')
                    conteoRespuestas += 1 #incrementar el contador
                except:
                    print('***No se leyo el buffer***')

            if re.search(patron,respuestasRecibidas):
                print(f'+++Encontrado en el buffer: {respuestasRecibidas}')
                ejecucion = False
            else:
                print(f'+++No encontrado en el buffer: {respuestasRecibidas}')
    
    """funcion para encender el modulo GPS""" #[1.54 seg]
    def encenderGPS(self):
        print('---Encendiendo el modulo GPS---')
        start = time.time()
        self.comando('AT+CGPSPWR=1',r'OK',5)
        
        print(f'---Modulo GPS encendido---{ time.time()-start }')
        time.sleep(1) #esperar 1 segundo
    
    """Establecer los parametros para la comunicacion GPRS""" #[2.86 seg]
    def parametrosGPRS(self):
        print('---Estableciendo parametros del GPRS---')
        start = time.time()
        self.comando('AT+CGATT=1',r'OK',3) #attach or detach from GRPS
        
        #configurando el uso de GPRS y el envio de paquetes
        self.comando('AT+SAPBR=3,1,\"Contype\",\"GPRS\"',r'OK',3)
        
        #configuracion del APN, user y password de la red
        self.comando('AT+SAPBR=3,1,\"APN\",\"internet.itelcel.com\"',r'OK',3)
        self.comando('AT+SAPBR=3,1,\"USER\",\"webgprs\"',r'OK',3)
        self.comando('AT+SAPBR=3,1,\"PWD\",\"webgprs2002\"',r'OK',3)

        print(f'---Parametros del GPRS establecidos---{time.time()-start}')
    
    """funcion para conocer el status del modulo GPS""" #[]  
    def statusGPS(self):
        print('---Verificando el estado del GPS---')
        start = time.time()
        self.comando('AT+CGPSSTATUS?',r'CGPSSTATUS: Location 3D Fix',5)
        print(f'---Estado del GPS correcto---{time.time()-start}')
    
    """inicializar el sim808""" #[7.44 seg]
    def __init__(self):
        self.encenderGPS() #encender el modulo GPS
        self.parametrosGPRS() #establecer los parametros para GPRS
        time.sleep(2.5)
        self.configurarHTTP() #configurando el envio por HTTP
    
    #funcion que devuleve la informacion necesaria para la alerta [0.21 seg]
    def cordenadas(self):
        
        print('---Obteniendo las cordenadas---')
        start = time.time()
        self.statusGPS() #verificar el estado del GPS
        
        ejecucion = True
        while ejecucion == True:
            conteoRespuestas = 0
            respuestasRecibidas = ''

            ser.write(b'AT+CGNSINF\r') #comando para obtener las cordenadas geograficas

            while conteoRespuestas < 3: #contar las primeras 3 respuestas
                try:
                    respuesta = ser.readline()
                    respuestasRecibidas += respuesta.decode('utf-8')
                    conteoRespuestas += 1
                except:
                    pass

            #encontrar el timestamptz, latitud y logitud
            if re.search(r'CGNSINF: 1,1,',respuestasRecibidas):
                
                #expresiones regulares
                regex = re.compile(r'CGNSINF: 1,1,(.*?),(.*?),(.*?),')
                variables = regex.search(respuestasRecibidas)

                #timestamptz y cordenadas
                timestamptz = variables.group(1)
                latitud = variables.group(2)
                longitud = variables.group(3)
                
                #salir del bucle
                ejecucion = False
        
        #datos de la ubicacion
        ano = timestamptz[0:4] #4 digitos
        mes = timestamptz[4:6] #2 digitos
        dia = timestamptz[6:8] #2 digitos
        horas = timestamptz[8:10] #2 digitos
        minutos = timestamptz[10:12] #2 digitos
        segundos = timestamptz[12:14] #2 digitos

        print(f'---Cordenadas obtenidas---{time.time()-start}')

        #formato UTC-5
        ano_r,mes_r,dia_r,horas_r,minutos_r,segundos_r = self.reducirHoras(
            ano,mes,dia,horas,minutos,segundos
        )
        return ano_r,mes_r,dia_r,horas_r,minutos_r,segundos_r,latitud,longitud
    
    #funcion para configurar la comunicacion con HTTP []
    def configurarHTTP(self):
        print('---Configurando comunicacion HTTP---')
        start = time.time()
        self.comando('AT+SAPBR=1,1',r'OK',10) #open the carrier 
        self.comando('AT+SAPBR=2,1',r'SAPBR: 1,1',3) #status del carrier

        self.comando('AT+HTTPINIT',r'OK',3) #iniciar el servicio HTTP

        #This command defines the carrier profile. Usually this is always 1
        self.comando('AT+HTTPPARA=\"CID\",1',r'OK',3)

        print(f'---HTTP configurado---{time.time()-start}')

    #funcion para enviar la informacion al servidor []
    def enviarInformacion(self):
        start = time.time()
        #obtener las cordenadas
        ano,mes,dia,horas,minutos,segundos,latitud,longitud = self.cordenadas()

        # obtener la informacion restante de la alerta
        nombre_alerta = self.generarNombreAlerta(ano,mes,dia,horas,minutos,segundos)
        fecha_hora_inicio = self.generarFechaHoraInicio(ano,mes,dia,horas,minutos,segundos)
        fecha_hora = self.generarFechaHora(ano,mes,dia,horas,minutos,segundos)

        #añadir las variables al enlace url
        enlace = servidor \
            + 'numero-serie=' + str(numero_serie) + '&' \
            + 'nombre-alerta=' + nombre_alerta + '&' \
            + 'fecha-hora-inicio=' + fecha_hora_inicio + '&' \
            + 'latitud=' + latitud + '&' \
            + 'longitud=' + longitud + '&' \
            + 'fecha-hora=' + fecha_hora

        print('---Enviando informacion---')
        self.comando('AT+HTTPPARA="URL","{}"'.format(enlace),r'OK',3) #configurando la url
        #tamaño del paquete a enviar 192 bytes
        #tiempo de espera antes de abortar el envio 10 segundos
        self.comando('AT+HTTPDATA=192,10000',r'OK',25)
        #envio de contenido
        # POST=1 / GET=0
        # status code 200
        self.comando('AT+HTTPACTION=1',r'HTTPACTION: (.*?),200,',18)
        print(f'---Envio de informacion finalizado---{time.time()-start}')

    #funcion para generar u obtener el nombre_alerta
    def generarNombreAlerta(self,ano,mes,dia,horas,minutos,segundos):
        #ejemplo 21/05/24/13:00:00
        global nombre_alerta
        if len(nombre_alerta) == 0:
            nombre_alerta = ano[2:4]+'/'+mes+'/'+dia+'/'+horas+':'+minutos+':'+segundos
        return nombre_alerta

    #funcion para generar u obtener la fecha_hora_inicio de la alerta
    def generarFechaHoraInicio(self,ano,mes,dia,horas,minutos,segundos):
        #ejemplo 2021-05-24T13:00:00
        global fecha_hora_inicio
        if len(fecha_hora_inicio) == 0:
            fecha_hora_inicio = ano+'-'+mes+'-'+dia+'T'+horas+':'+minutos+':'+segundos
        return fecha_hora_inicio 

    #funcion para generar la fecha_hora
    def generarFechaHora(self,ano,mes,dia,horas,minutos,segundos):
        #ejemplo 2021-05-24T13:00:00
        fecha_hora = ano+'-'+mes+'-'+dia+'T'+horas+':'+minutos+':'+segundos
        return fecha_hora 

    #funcion para cerrar la conexion [3.29 seg]
    def finalizarConexionHTTP(self):
        print('---Finalizando conexion HTTP---')
        start = time.time()
        self.comando('AT+HTTPTERM',r'OK',5) #terminate http service
        self.comando('AT+SAPBR=0,1',r'OK',5) #cerrando la comunicacion GPRS
        print(f'---Conexion HTTP finalizada---{time.time()-start}')

    #funcion para saber si la alerta fue desactivada []
    def alertaDesactivada(self):
        #enlace url
        enlace = servidor_desactivacion \
            + 'numero-serie=' + str(numero_serie)

        print('---Verificando el status de la alerta---')
        start = time.time()
        ejecutar = True
        while ejecutar == True:
            self.comando('AT+HTTPPARA="URL","{}"'.format(enlace),r'OK',3) 
            self.comando('AT+HTTPDATA=100,10000',r'OK',25)
            self.comando('AT+HTTPACTION=0',r'HTTPACTION: (.*?),200,',18) #status code 200
            response = self.readResponseHTTP('AT+HTTPREAD',6) #guardar la respuesta del servidor
            if re.search(r'false',response): #leer la respuesta del servidor
                estado_alerta = False #la alerta fue desactivada
                ejecutar = False #salir del bucle
            elif re.search(r'true',response):
                estado_alerta = True #la alerta continua activa
                ejecutar = False #salir del bucle

        print(f'---Verificacion del status de la alerta finalizada---{time.time()-start}')
        return estado_alerta #devolver el estado de la alerta

    #funcion para leer la respuesta que envia el servidor [1.07 seg]
    def readResponseHTTP(self,comando,limite):
        
        ejecucion = True
        start = time.time()
        while ejecucion == True:
            conteoRespuestas = 0
            respuestasRecibidas = ''
            mensaje = bytes('{}\r'.format(comando),encoding='utf-8') #generar el comando AT
            print('Comando: {} ingresado'.format(mensaje))
            ser.write(mensaje) #enviar comando
            
            while conteoRespuestas < limite:
                try:
                    respuesta = ser.readline()
                    respuestasRecibidas += respuesta.decode('utf-8')
                    conteoRespuestas += 1
                except:
                    pass

            #verificar que el mensaje no este vacio
            if len(respuestasRecibidas) != 0:
                ejecucion = False

        print(f'---Respuesta capturada---{time.time()-start}')
        return respuestasRecibidas

    #funcion para substraer 5 horas a la alerta
    def reducirHoras(self,ano,mes,dia,horas,minutos,segundos):
        #string --> datetime object
        date_time_str = ano+'/'+mes+'/'+dia+' '+horas+':'+minutos+':'+segundos
        date_time_obj = datetime.strptime(date_time_str,'%Y/%m/%d %H:%M:%S')
        # restar 5 horas
        new_date_time = date_time_obj - timedelta(hours=5)
        #datetime object --> string
        ano_r = new_date_time.strftime('%Y')
        mes_r = new_date_time.strftime('%m')
        dia_r = new_date_time.strftime('%d')
        horas_r = new_date_time.strftime('%H')
        minutos_r = new_date_time.strftime('%M')
        segundos_r = new_date_time.strftime('%S')

        return ano_r,mes_r,dia_r,horas_r,minutos_r,segundos_r

    """funcion para enviar comandos AT [prueba]
    def comando(self,comando,patron,limite):
        ejecucion = True
        while ejecucion == True:
            time.sleep(0.2)
            buffer = ''
            conteo_limite = 0
            mensaje = bytes('{}\r'.format(comando),encoding='utf-8')
            print(f'Comando ingresado: {str(mensaje)}')
            ser.write(mensaje)
            while conteo_limite < limite:
                try:
                    respuesta = ser.readline()
                    buffer += respuesta.decode('utf-8')
                    conteo_limite += 1
                    print(f'conteo: {conteo_limite} -- {buffer}')
                    if re.search(patron,buffer):
                        print(f'Buffer: {buffer}')
                        ejecucion = False 
                        conteo_limite = 1000
                except:
                    print('No se leyo el buffer')
    """


"""Configuracion del modulo SIM808"""
ser = serial.Serial(port,baudrate=9600,timeout=0.5) #configuracion del puerto serial
modulo = SIM808() #inicializar el SIM808

"""Configuracion de la interrupcion"""
GPIO.setwarnings(False) #apagar los warnings
GPIO.setmode(GPIO.BOARD) #numeracion de la placa
GPIO.setup( # entrada con resistencia pull-down
    push_button, 
    GPIO.IN, 
    pull_up_down=GPIO.PUD_DOWN
)
"""
GPIO.add_event_detect( #configuracion de la interrupcion
    push_button,
    GPIO.RISING,
    callback=alerta, 
    bouncetime= 3000 # [3 seg]
)
"""

while True: #loop
    if GPIO.input(40) == GPIO.HIGH:
        alerta()

#modulo.alertaDesactivada()
#modulo.enviarInformacion() #enviar una alerta
#modulo.finalizarConexionHTTP() #finalizar la conexion