import mesa

import random

import math

#La clase banqueta tiene como objetivo representar a un agente banqueta, el cual va a servir como delimitador de los movimientos del agente coche, el cual se va a declarar más adelante
class Build(mesa.Agent):

    #La función de __init__ tiene como objetivo hacer de contructor de la clase, esta recibe el unique id asignado y el color que va a tomar este agente en la simulación Tiene una complejidad de O(1) y no tiene un valor de retorno
    def __init__(self, unique_id, model, color):

        super().__init__(unique_id, model)

        self.contador = 0

        self.color = color

    #La función de step es la encargada de realizar las acciones en su interior cada vez que se le llame al agente Build, no tiene valor de retorno ni parametros de entrada y tiene una complejidad de O(1)
    def step(self):

        self.contador += 1

#La clase Tope tiene como objetivo representar a un agente tope, el cual va a servir como delimitador de los movimientos del agente coche, el cual se va a declarar más adelante
class Tope(mesa.Agent):

    #La función de __init__ tiene como objetivo hacer de contructor de la clase, esta recibe el unique id asignado. Tiene una complejidad de O(1) y no tiene un valor de retorno
    def __init__(self, unique_id, model):
        
        super().__init__(unique_id, model)
        
        self.color = "brown"
        
        self.arribados = 0
    
    #La función de eliminar tiene como objetivo eliminar los coches que se encuentren en la misma celda que el agente tope con el objetivo de que las gráficas no se alteren No tiene un valor de retorno y tiene una compleijidad de O(n)
    def eliminar(self): #Ya elimina a los agentes que llegaron
        
        contenido = self.model.grid.get_cell_list_contents([self.pos])
        
        if len(contenido) > 1:
        
            for i in contenido:
        
                if type(i) == Coche:
        
                    i.finalizado = True
        
                    self.model.grid.remove_agent(i)
        
                    self.arribados += 1

    #La función de step es la encargada de realizar las acciones en su interior cada vez que se le llame al agente Tope, no tiene valor de retorno ni parametros de entrada y tiene una complejidad de O(1)
    def step(self):
        
        self.eliminar()

#La clase Detenedor tiene como objetivo representar a un agente detenedor, el cual va a servir como delimitador de los movimientos del agente coche, el cual se va a declarar más adelante
class Detenedor(mesa.Agent):
    
    #La función de __init__ tiene como objetivo hacer de contructor de la clase, esta recibe el unique id asignado, el color que va a tomar el agente en la simulación y el segundo agente detenedor. Tiene una complejidad de O(1) y no tiene un valor de retorno
    def __init__(self,unique_id,model, comparacion, color):
        
        super().__init__(unique_id, model)
        
        self.cocheDetenido = []
        
        self.Detenedor2 = []
        
        self.direccionComparacion = comparacion
        
        self.color = color

    def semaforoLibre(self):
        
        posicion = []
        
        posicion.append(self.pos)
        
        if self.direccionComparacion == "Arriba":
        
            temp = list(posicion[0])
        
            temp[1] += 1
        
            posicion = tuple(temp)
        
        else:
        
            temp = list(posicion[0])
        
            temp[0] += 1
        
            posicion = tuple(temp)

        contenido = self.model.grid.get_cell_list_contents(posicion)

        if len(contenido) == 1:
        
            return True
        
        else:
        
            return False
    
    #La función de dejarPasar es la encargada de indicarle al agente que puede dejar pasar al siguiente coche a la posicion del semaforo, no tiene parametros de entrada, tiene complejidad O(1) y no tiene valor de retorno
    def dejarPasar(self):

        if len(self.cocheDetenido) > 0:
        
            self.cocheDetenido[0].avanza = True
        
            self.cocheDetenido.clear()
        
        else: 
        
            pass

    #La función de step es la encargada de realizar las acciones en su interior cada vez que se le llame al agente Detenedor, no tiene valor de retorno ni parametros de entrada y tiene una complejidad de O(n)
    def step(self):
        
        if self.semaforoLibre() or self.Detenedor2[0].semaforoLibre():
        
            self.dejarPasar()
        
            self.Detenedor2[0].dejarPasar()
        
        else:
        
            contenido = self.model.grid.get_cell_list_contents(self.pos)
        
            if len(contenido) > 1:
        
                for i in contenido:
        
                    if type(i) == Coche:
        
                        self.cocheDetenido.append(i)
        
                        i.avanza = False

#La clase TrafficLigth tiene como objetivo representar a un agente semaforo, el cual va a servir para el codigo de colores de la actividad, el cual se va a declarar más adelante
class TrafficLigth(mesa.Agent):

    #La función de __init__ tiene parametros de entrada como lo son la posicion del semaforo en el grid, no tiene valor de retorno y tiene compleidad de O(1), además, tiene el objetivo de inicializar el semaforo en el grid
    def __init__(self, unique_id, model, pos):
        
        super().__init__(unique_id, model)
        
        self.color = "yellow"
        
        self.prioridad = []
        
        self.contadorColor = 0
        
        self.agenteSemaforoSecundario = None
        
        self.activo = True

        self.posOriginal = pos

        self.pos_X = self.posOriginal[0]

        self.pos_Y = self.posOriginal[1]
        
        self.tiempoActualOrigen = 0

        self.tiempoReactivacion = 0

    #La función de cambioColor no tiene parametros de entrada, no tiene valor de retorno y tiene compleidad de O(1), además, tiene el objetivo de cambiar de color al semaforo a lo largo de la simulacion
    def cambioColor(self): #Ya cambia de color el semaforo
       
        if self.contadorColor == 1:
       
            self.color = "red"
       
        elif self.contadorColor == 2:
       
            self.color = "green"
       
        else:
       
            self.color = "yellow"
       
            self.contadorColor = 0

    #La función de asignacion no tiene parametros de entrada, no tiene valor de retorno y tiene compleidad de O(1), además, tiene el objetivo de asignar un coche a su lista de prioridad
    def asignacion(self): #Ya se mete su agente a su lista de prioridad
        
        contenidoMismaCelda = self.model.grid.get_cell_list_contents([self.pos])
        
        if len(contenidoMismaCelda) > 1:
        
            for i in contenidoMismaCelda:
        
                if type(i) == Coche:
        
                    i.avanza = False #Le dices que ya no avance
        
                    i.arribado = True
        
                    self.prioridad.append(i)
        
                    self.contadorColor = 1

    #La función de asignacion no tiene parametros de entrada, no tiene valor de retorno y tiene compleidad de O(1), además, tiene el objetivo de vaciar su lista de prioridad
    def vaciado(self): #Ya se limpia la lista de prioridad
        
        if len(self.prioridad) > 0:
        
            self.prioridad.clear()
        
            self.cambioColor()

    #La función de asignacion no tiene parametros de entrada, no tiene valor de retorno y tiene compleidad de O(1), además, tiene el objetivo de asegurar que ningun coche este cruzando en el momento
    def sinCochesCruzando(self):

        contenidosDerecha = self.model.grid.get_cell_list_contents(tuple([self.pos_X + 1 , self.pos_Y]))
        
        contenidosArriba = self.model.grid.get_cell_list_contents(tuple([self.pos_X , self.pos_Y + 1]))
        

        if len(contenidosDerecha) == 0 or len(contenidosArriba) == 0:

            self.contadorColor = 2 
            
            self.cambioColor()

            return True
        
        else:

            self.contadorColor = 1
            
            self.cambioColor()
           
            return False

    #La función de negociacion es la encargada de realizar las acciones de negociacion entre los diferentes agentes, no tiene parametro de entrada, ni valor de retornony tiene una complejidad de O(n^2)
    def negociacion(self):    

        vecinos = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )

        for i in vecinos: #Detecta a los vecinos
        
            contenido = self.model.grid.get_cell_list_contents(i) #Detecta si ya hay varias cosas en la celda, ya que se tendría semaforo y coche
            
            if len(contenido) > 1:
            
                for j in contenido:
            
                    if type(j) == TrafficLigth:
            
                        self.agenteSemaforoSecundario = j
        
        semaforoSecundario = self.agenteSemaforoSecundario
        

        if self.contadorColor == 1:
            
                self.cambioColor()
            
                semaforoSecundario.contadorColor = 2
            
                semaforoSecundario.cambioColor()

        if self.contadorColor == 2:
            
                self.cambioColor()
            
                semaforoSecundario.contadorColor = 1
            
                semaforoSecundario.cambioColor()

        if self.contadorColor != 1 and self.contadorColor != 2:
            
            self.cambioColor()
            
            semaforoSecundario.contadorColor = 4
            
            semaforoSecundario.cambioColor() 
            
        try:
            
            if len(semaforoSecundario.prioridad) == 0:

                if self.sinCochesCruzando():
            
                    self.contadorColor = 2
            
                    semaforoSecundario.contadorColor = 1

                    self.cambioColor()

                    semaforoSecundario.cambioColor()

                    self.prioridad[0].avanza = True

                    self.vaciado()

                    if self.contadorColor == 1:

                        self.cambioColor()

                        semaforoSecundario.contadorColor = 2

                        semaforoSecundario.cambioColor()

                    if self.contadorColor == 2:

                        self.cambioColor()

                        semaforoSecundario.contadorColor = 1

                        semaforoSecundario.cambioColor()
                            
                    if self.contadorColor != 1 and self.contadorColor != 2:

                        self.cambioColor()

                        semaforoSecundario.contadorColor = 4

                        semaforoSecundario.cambioColor() 
                        

                else:

                    self.contadorColor = 2

                    semaforoSecundario.contadorColor = 1


                    self.cambioColor()

                    semaforoSecundario.cambioColor()

                    self.prioridad[0].avanza = True

                    self.vaciado()

                    if self.contadorColor == 1:

                        self.cambioColor()

                        semaforoSecundario.contadorColor = 2

                        semaforoSecundario.cambioColor()

                    if self.contadorColor == 2:

                        self.cambioColor()

                        semaforoSecundario.contadorColor = 1

                        semaforoSecundario.cambioColor()
                            
                    if self.contadorColor != 1 and self.contadorColor != 2:

                        self.cambioColor()

                        semaforoSecundario.contadorColor = 4

                        semaforoSecundario.cambioColor() 

            #El otro si tiene cola de prioridad
            elif len(semaforoSecundario.prioridad) > 0:
                #El coche del otro semaforo tiene mayor velocidad que mi coche
                if semaforoSecundario.prioridad[0].velocidad > self.prioridad[0].velocidad: 

                    semaforoSecundario.contadorColor = 2

                    self.contadorColor = 1

                    self.cambioColor()
                    semaforoSecundario.cambioColor()

                    semaforoSecundario.prioridad[0].avanza = True


                #El coche del otro semaforo tiene menor velocidad que mi coche
                elif semaforoSecundario.prioridad[0].velocidad < self.prioridad[0].velocidad:

                    semaforoSecundario.contadorColor = 1

                    self.contadorColor = 2

                    self.cambioColor()

                    semaforoSecundario.cambioColor()

                    self.prioridad[0].avanza = True

                    self.vaciado()

                #El coche del otro semaforo tiene igual velocidad que mi coche
                else:

                    paso = random.randint(0,1)

                    if paso == 0:

                        semaforoSecundario.contadorColor = 2

                        self.contadorColor = 1

                        self.cambioColor()

                        semaforoSecundario.cambioColor()

                        semaforoSecundario.prioridad[0].avanza = True

                    else:

                        semaforoSecundario.contadorColor = 1

                        self.contadorColor = 2
                        
                        self.cambioColor()
                        
                        semaforoSecundario.cambioColor()
                        
                        self.prioridad[0].avanza = True
                        
                        self.vaciado()

        except: 

            if self.contadorColor == 1:
            
                        self.cambioColor()
            
                        semaforoSecundario.contadorColor = 2
            
                        semaforoSecundario.cambioColor()

            if self.contadorColor == 2:
            
                self.cambioColor()
            
                semaforoSecundario.contadorColor = 1
            
                semaforoSecundario.cambioColor()
                            
            if self.contadorColor != 1 and self.contadorColor != 2:
            
                self.cambioColor()
            
                semaforoSecundario.contadorColor = 4
            
                semaforoSecundario.cambioColor()      
                   
            pass
    
    #La función de step es la encargada de realizar las acciones en su interior cada vez que se le llame al agente Tope, no tiene valor de retorno ni parametros de entrada y tiene una complejidad de O(1)
    def step(self): 

        if len(self.prioridad) == 0:
            
            self.contadorColor = 0
            
            self.cambioColor()
            
            self.asignacion()

        elif len(self.prioridad) > 0:
            
            self.negociacion() 
            
            self.prioridad.clear()
            
class Coche(mesa.Agent):

    #La función de __init__  tiene parametros de entrada como lo son la velocidad inicial del coche y el color que este va a tomar, no tiene valor de retorno y tiene compleidad de O(1), además, tiene el objetivo de inicializar el coche en el grid
    def __init__(self, unique_id, model, velocidad, color):
        
        super().__init__(unique_id, model)
        
        self.tiempoarribo = 0 #Guarda la distancia hasta la celda del semaforo
        
        self.coordenadasSemaforos = self.model.coordenadasSemaforos

        self.arribado = False #Se vuelve true cuando ya llego al semaforo
        
        self.velocidad = velocidad
        
        self.color = color
        
        self.visited = [] #Para que no este repite y repite los mismos lugares
        
        self.avanza = True #Sirve para indicare al coche que puede avanzar
        
        self.finalizado = False #Sirve para indicar cuando un coche ya llego a su destino

        self.movimientos = 0

    #La función de calculoDistancia no tiene parametros de entrada, no tiene valor de retorno y tiene compleidad de O(1), además, tiene el objetivo de indicar cual es la distancia del auto hasta el semaforo
    def calculoDistancia(self):
       
        if self.arribado == False:

            distanciaAgente = []
       
            distanciaAgente.append(self.pos)

            distancia1 = math.dist(self.pos, self.coordenadasSemaforos[0])

            distancia2 = math.dist(self.pos, self.coordenadasSemaforos[1])

            if distancia1 <= distancia2:

                self.tiempoarribo =   distancia1 / self.velocidad

            else:

                self.tiempoarribo = distancia2 / self.velocidad

    #La función de cambioVelicidad no tiene parametros de entrada, no tiene valor de retorno y tiene compleidad de O(1), además, tiene el objetivo de alterar la velocidad del auto de forma aleatoria en cada step
    def cambioVelocidad(self): #Para cambiar la velocidad del coche
        
        nuevaVelocidad = random.randint(1,50)
        
        self.velocidad = nuevaVelocidad

    #La funcion de move, recibe como parametro el self de la clase y tiene como objetivo seleccinar la siguiente celda hacia la que el agente se va a mover dentro del grid, al utilizar esta función, se elimina la posiblidad de que el agente se salga de los bordes del grid, haciendo que todos los movimientos que haga sean validos. No tiene un valor de retorno y tiene complejidad de O(n^2)
    def move(self): #Ya se mueven y son capaces de llegar al final

        celdas = self.model.grid.get_neighborhood(
            self.pos, moore=False, include_center=False
        )

        celdasVacias = 0
       
        celdasPosibles = []

        for i in celdas:

            if self.model.grid.is_cell_empty(i):
       
                celdasVacias += 1
       
                celdasPosibles.append(i)
       
            else:

                status = True
       
                contenido = self.model.grid.get_cell_list_contents([i])
                
                for j in contenido:
       
                    if type(j) == Build or type(j) == Coche:# and self.velocidad < 25: #Se agrega la velocidad
                    
                        status = False
                    
                        break

                    elif type(j) == TrafficLigth and self.arribado == True:
                   
                        status = False
                   
                        break
                        
                if status == True:
                   
                    celdasVacias += 1
                   
                    celdasPosibles.append(i)
                    
        
        if celdasVacias != 0:

            random.shuffle(celdasPosibles)
            
            for i in celdasPosibles:
            
                if i not in self.visited:
            
                    self.visited.append(i)
            
                    self.model.grid.move_agent(self, i)

    #La función de step es la encargada de realizar las acciones en su interior cada vez que se le llame al agente Tope, no tiene valor de retorno ni parametros de entrada y tiene una complejidad de O(1)           
    def step(self):
        
        if self.avanza == True and self.finalizado != True: #Si al coche le esta prmitido avanzar y todavía no termina, entonces avanza
        
            self.calculoDistancia()
        
            self.move()
        
            self.cambioVelocidad()
        
            self.movimientos += 1
        
            if not self.arribado:
        
                self.calculoDistancia()

class ModeloCamino(mesa.Model):

    #La funcion __init__ tiene el objetivo de ser el constructor de la clase ModeloCamino, recibe como parametros el self de la clase, el numero de coches tanto verticales y horizontales que se van a tener, el ancho y el alto del grid que se va a construir Todos estos parametros tienen el objetivo de ser asignados dentro de esta función para servir como atributos de la presente clase. Además, se declaran y se colocan los diferentes agentes en el grid. Tiene una complejidad de O(n^2) y no posee valor de retorno
    def __init__(self, ancho, alto, numCochesVertical, numCochesHorizontal):
        
        self.grid = mesa.space.MultiGrid(ancho, alto, False)

        self.schedule = mesa.time.RandomActivationByType(self)

        self.numCochesVertical = numCochesVertical
        
        self.numCochesHorizontal = numCochesHorizontal
        
        self.cantidadAgentes = 0
        
        self.coordenadasSemaforos = [] 
        
        self.running = True
        
        self.promedioVelocidadesAcumuladas = []
        
        self.promedioTiemposAcumuladas = []
        
        self.tiempoActual = 0

        #Se agregan semaforos
        for i in range(0,2):
        
            if i != 0:
        
                Semaforos = TrafficLigth(i, self, [int(ancho/2), int(alto/2)-1])
        
                self.schedule.add(Semaforos)
        
                self.grid.place_agent(Semaforos, (int(ancho/2), int(alto/2)-1)) 
        
                self.coordenadasSemaforos.append(Semaforos.pos)
        
            else:
        
                Semaforos = TrafficLigth(i, self, [int(ancho/2)-1, int(alto/2)])
        
                self.schedule.add(Semaforos)
        
                self.grid.place_agent(Semaforos, (int(ancho/2)-1, int(alto/2))) 
        
                self.coordenadasSemaforos.append(Semaforos.pos)
        
            self.cantidadAgentes += 1

        #Se agregan coches vertical
        for i in range(0, numCochesVertical):
            
            cocheVertical = Coche(i + self.cantidadAgentes, self, 22 , "orange") #random.randint(5,25)
            
            self.schedule.add(cocheVertical)
            
            self.grid.place_agent(cocheVertical, (int(ancho/2), 0))
            
            cocheVertical.visited.append(cocheVertical.pos) #Para que no se quede atorado en la posicion original            
            
            self.cantidadAgentes += 1

        #Se agregan coches horizontal
        for i in range(0, numCochesHorizontal):
            
            cocheHorizontal = Coche(i + numCochesVertical + self.cantidadAgentes, self, 35, "purple")
            
            self.schedule.add(cocheHorizontal)
            
            self.grid.place_agent(cocheHorizontal, (0, int(alto/2)))
            
            cocheHorizontal.visited.append(cocheHorizontal.pos)  #Para que no se quede atorado en la posicion original 
            
            self.cantidadAgentes += 1
        
        #Se agregan banquetas
        for i in range(0,ancho):
            
            for j in range(0, alto):
            
                if (j != int(alto/2) and i != int(alto/2)) or (i != int(ancho/2) and j != int(ancho/2)) and self.grid.is_cell_empty(pos=(i,j)):
                
                    Banquetas = Build((self.cantidadAgentes+ numCochesVertical +numCochesHorizontal)*5,self,"red")
                
                    self.schedule.add(Banquetas)
                
                    self.grid.place_agent(Banquetas,(i,j))
                
                    self.cantidadAgentes += 1

        #Se agregan finales
        Topes = Tope((self.cantidadAgentes+numCochesHorizontal+numCochesVertical)*8,self)
        
        self.schedule.add(Topes)
        
        self.grid.place_agent(Topes,(int(ancho/2),int(alto-1)))
        
        self.cantidadAgentes += 1

        Topes = Tope((self.cantidadAgentes+numCochesHorizontal+numCochesVertical)*8,self)
        
        self.schedule.add(Topes)
        
        self.grid.place_agent(Topes,(ancho-1,int(alto/2)))

        self.datacollector = mesa.DataCollector(
            
            {
            
                "CochesArribados": ModeloCamino.cochesArribados,
            
                "PromedioVelocidades": ModeloCamino.promedioVelocidades,
            
                "PromedioDistancias": ModeloCamino.promedioTiempos,
            
                "MovimientosAgentes": ModeloCamino.movimientosAgentes,
            
            }
        )

    #La funcion de step es la responsable de llamar al step de los diferentes agentes y así poder realizar las funciones del programa, además, es la responsable de llamar al data colletor para que este se actualice en cada uno de los pasos del programa. Recibe como parametros el self de la clase, no tiene valor de retorno y posee una complejidad de O(n)
    def step(self):

        #self.scheduleSemaforo.step()
        self.schedule.step(False, True)

        self.tiempoActual += 1

        self.datacollector.collect(self)

        contador = 0

        for i in self.schedule.agents:
        
            if type(i) == Coche and i.finalizado == False:
        
                contador+=1

        if contador == 0:
        
            for i in self.schedule.agents:
        
                if type(i) == TrafficLigth:
        
                    i.contadorColor = 0
        
                    i.cambioColor()

            self.running = False

    #La función movimientosAgentes en un metodo estatico ya que este no cambia por el paso del tiempo, recibe como parametro el modelo del que se van a obtener los datos con los que se planea trabajar, tiene el objetivo de retornar un numero entero que indica la cantidad de movimientos que los agentes realizaron en el grid. Tiene una complejidad de O(n)
    @staticmethod
    def movimientosAgentes(model):
        
        acumulado = 0
        
        for agent in model.schedule.agents:
        
            if type(agent) == Coche:
        
                acumulado = acumulado + agent.movimientos

        return acumulado

    #La función cochesArribados en un metodo estatico ya que este no cambia por el paso del tiempo, recibe como parametro el modelo del que se van a obtener los datos con los que se planea trabajar, tiene el objetivo de retornar un numero entero que indica la cantidad de conches arribados en el grid. Tiene una complejidad de O(n)
    @staticmethod
    def cochesArribados(model):
        
        acumulado = 0
        
        for agent in model.schedule.agents:
        
            if type(agent) == Tope:
        
                acumulado = acumulado + agent.arribados

        return acumulado

    #La función promedioVelocidades en un metodo estatico ya que este no cambia por el paso del tiempo, recibe como parametro el modelo del que se van a obtener los datos con los que se planea trabajar, tiene el objetivo de retornar un numero entero que indica el promedio de las velocidades de llegada de los coches al semaforo en el grid. Tiene una complejidad de O(n)
    @staticmethod
    def promedioVelocidades(model):

        promedio = []

        for agent in model.schedule.agents:

            if type(agent) == Coche and agent.finalizado != True:

                promedio.append(agent.velocidad)

        if len(promedio) == 0:

            if len(model.promedioVelocidadesAcumuladas) == 0:
                return 0
            else:

                return model.promedioVelocidadesAcumuladas[-1]

        else:

            model.promedioVelocidadesAcumuladas.append(sum(promedio) / len(promedio))

            return sum(promedio) / len(promedio)
    
    #La función promedioTiempos en un metodo estatico ya que este no cambia por el paso del tiempo, recibe como parametro el modelo del que se van a obtener los datos con los que se planea trabajar, tiene el objetivo de retornar un numero entero que indica el promedio de los tiempos de llegada de los coches al semaforo en el grid. Tiene una complejidad de O(n)
    @staticmethod
    def promedioTiempos(model):

        promedio = []

        for agent in model.schedule.agents:

            if type(agent) == Coche and agent.arribado != True:

                promedio.append(agent.tiempoarribo)

        if len(promedio) == 0:

            if len(model.promedioTiemposAcumuladas) == 0:
                return 0
            else:

                return model.promedioTiemposAcumuladas[-1]

        else:

            model.promedioTiemposAcumuladas.append(sum(promedio) / len(promedio))

            return sum(promedio) / len(promedio)



from Agentes import *

from mesa.visualization.UserParam import UserSettableParameter

import matplotlib.pyplot as plt

import pandas as pd

def agent_portrayal(agent):

    portrayal = {

        "Shape": "circle",

        "Filled": "true",

        "Layer": "coche",

        "Color": agent.color,

        "r": 0.5,

    }

    if type(agent) == Build:

        portrayal["Layer"] = "Build"
        
    if type(agent) == TrafficLigth:

        portrayal["Layer"] = "TrafficLigth"
    

    return portrayal

grid = mesa.visualization.CanvasGrid(agent_portrayal, 10, 10, 750, 750)

simulation_parametrosIteraciones = {

    "numCochesVertical": UserSettableParameter(
        "slider",
        "Number of Horizontal Agents",
        50,
        1,
        50,
        1,
        description = "Elige cuantos agentes estan en la simulacion",   
    ),

    "numCochesHorizontal": UserSettableParameter(
        "slider",
        "Number of Vertical Agents",
        50,
        1,
        50,
        1,
        description = "Elige cuantos agentes estan en la simulacion",   
    ),

    "ancho": 10,

    "alto": 10,
}

movimientosGeneralesAgentes = mesa.visualization.ChartModule(

    [
        {"Label": "CochesArribados","Color": "green"},
    ],

data_collector_name='datacollector')

promedioVelocidades = mesa.visualization.ChartModule(

    [

        {"Label": "PromedioVelocidades","Color": "red"}

    ],

data_collector_name='datacollector')



#La variable de server tiene el objetivo de guardar el servidor generado con los parametros y graficas declarados previamente para su posterior despliegue en el puerto 8521
server = mesa.visualization.ModularServer(
    
    ModeloCamino, [grid, movimientosGeneralesAgentes, promedioVelocidades, promedioTiempos], "Trafico Simulacion", simulation_parametrosIteraciones

)

server.port = 8521

server.launch()