import bridges
import globales
import sulkuPypi
import sulkuFront
import gradio as gr
import gradio_client
import tools
import observa.herramientas as observa_herramientas
import observa.biblioteca_modelos as biblioteca_modelos

mensajes, sulkuMessages = tools.get_mensajes(globales.mensajes_lang)

btn_buy = gr.Button("Get Credits", visible=False, size='lg')

#PERFORM es la app INTERNA que llamará a la app externa.
def perform(input1, input2, request: gr.Request):

    tokens = sulkuPypi.getTokens(sulkuPypi.encripta(request.username).decode("utf-8"), globales.env)
    
    #1: Reglas sobre autorización si se tiene el crédito suficiente.
    autorizacion = sulkuPypi.authorize(tokens, globales.work)
    if autorizacion is True:
        try: 
            resultado, observacion = mass(input1, input2)
        except Exception as e:                       
            info_window, resultado, html_credits = sulkuFront.aError(request.username, tokens, excepcion = tools.titulizaExcepDeAPI(e))
            return resultado, info_window, html_credits, btn_buy
    else:
        info_window, resultado, html_credits = sulkuFront.noCredit(request.username)
        return resultado, info_window, html_credits, btn_buy    
    
    #Primero revisa si es imagen!: 
    if 1 == 1:
        #Si es imagen, debitarás.
        html_credits, info_window = sulkuFront.presentacionFinal(request.username, "debita", observacion)
    else: 
        #Si no es imagen es un texto que nos dice algo.
        info_window, resultado, html_credits = sulkuFront.aError(request.username, tokens, excepcion = tools.titulizaExcepDeAPI(resultado))
        return resultado, info_window, html_credits, btn_buy      
    
    #Lo que se le regresa oficialmente al entorno.
    return resultado, info_window, html_credits, btn_buy

#MASS es la que ejecuta la aplicación EXTERNA
def mass(input1, input2): #input1 es la imagen e input2 es el texto.

    print("La pregunta recibida es: ")
    print(input2)
    api, tipo_api = tools.eligeAPI(globales.seleccion_api)

    texto = observa_herramientas.traduccion_final(input2)
    observacion = ""
    if texto == "Lang Unknown": 
        texto = "Describe the image" #Como desconoció el idioma harémos una pregunta estándar.
        observacion = mensajes.lang_unk

    imagenDestiny = gradio_client.handle_file(input1)  

    client = gradio_client.Client(api, hf_token=bridges.hug)    
    
    try:         
        result = client.predict(imagenDestiny, texto, api_name=globales.interface_api_name)
        print("La pregunta final quedó: ", texto)
        print("Ésto es result: ", result)
        #Siempre traduciremos del inglés al español.
        traduccion = observa_herramientas.infiere(biblioteca_modelos.ingles_español, result)
        resultado = traduccion[0]['translation_text']
                 
        #(Si llega aquí, debes debitar de la quota, incluso si detecto no-face o algo.)
        #Future: Debe de aglutinarse ésto en una función con entrada y salida para no tener tanto texto.
        if tipo_api == "quota":
            print("Como el tipo api fue quota, si debitaremos la quota.")
            sulkuPypi.updateQuota(globales.process_cost)
        #No debitas la cuota si no era gratis, solo aplica para Zero.         
                
        return resultado, observacion

    except Exception as e:
            mensaje = tools.titulizaExcepDeAPI(e)        
            return mensaje