import bridges
import globales
import sulkuPypi
import sulkuFront
import gradio as gr
import gradio_client
import time
import tools

btn_buy = gr.Button("Get Credits", visible=False, size='lg')

#PERFORM es la app INTERNA que llamará a la app externa.
def perform(input1, input2, request: gr.Request):

    #Future: Maneja una excepción para el concurrent.futures._base.CancelledError
    #Future: Que no se vea el resultado anterior al cargar el nuevo resultado! (aunque solo se ven los resultados propios.)         

    tokens = sulkuPypi.getTokens(sulkuPypi.encripta(request.username).decode("utf-8"), globales.env)
    
    #1: Reglas sobre autorización si se tiene el crédito suficiente.
    autorizacion = sulkuPypi.authorize(tokens, globales.work)
    if autorizacion is True:
        try: 
            resultado = mass(input1, input2)
        except Exception as e:                       
            info_window, resultado, html_credits = sulkuFront.aError(request.username, tokens, excepcion = tools.titulizaExcepDeAPI(e))
            return resultado, info_window, html_credits, btn_buy
    else:
        info_window, resultado, html_credits = sulkuFront.noCredit(request.username)
        return resultado, info_window, html_credits, btn_buy    
    
    #Primero revisa si es imagen!: 
    if 1 == 1:
        #Si es imagen, debitarás.
        html_credits, info_window = sulkuFront.presentacionFinal(request.username, "debita")
    else: 
        #Si no es imagen es un texto que nos dice algo.
        info_window, resultado, html_credits = sulkuFront.aError(request.username, tokens, excepcion = tools.titulizaExcepDeAPI(resultado))
        return resultado, info_window, html_credits, btn_buy      
    
    #Lo que se le regresa oficialmente al entorno.
    return resultado, info_window, html_credits, btn_buy

#MASS es la que ejecuta la aplicación EXTERNA
def mass(input1, input2):
    
    api, tipo_api = tools.eligeAPI(globales.seleccion_api)

    client = gradio_client.Client(api, hf_token=bridges.hug)
    imagenDestiny = gradio_client.handle_file(input1) 
    
    try: 
        #imagen luego prompt
        result = client.predict(imagenDestiny, input2, api_name=globales.interface_api_name)
        print("Ésto es result: ", result)
          
                
        #(Si llega aquí, debes debitar de la quota, incluso si detecto no-face o algo.)
        #Future: Debe de aglutinarse ésto en una función con entrada y salida para no tener tanto texto.
        if tipo_api == "quota":
            print("Como el tipo api fue gratis, si debitaremos la quota.")
            sulkuPypi.updateQuota(globales.process_cost)
        #No debitas la cuota si no era gratis, solo aplica para Zero.         
        
        #result = splash_tools.desTuplaResultado(result)
        return result

    except Exception as e:
            #La no detección de un rostro es mandado aquí?! Siempre?
            mensaje = tools.titulizaExcepDeAPI(e)        
            return mensaje