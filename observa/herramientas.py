
import requests
import bridges
import observa.biblioteca_modelos as biblioteca_modelos

def precalienta_modelos():

    print("En éste momento estoy precalentando los modelos...")
    # Obtener los nombres de los atributos del módulo biblioteca_modelos
    modelos = [attr for attr in dir(biblioteca_modelos) if not attr.startswith("__")]

    # Filtrar los atributos que no son variables (por ejemplo, funciones)
    modelos = [attr for attr in modelos if not callable(getattr(biblioteca_modelos, attr))]

    # Iterar sobre los nombres de los modelos y llamar a infiere
    for modelo in modelos:
        infiere(getattr(biblioteca_modelos, modelo), "texto genérico para precalentar...")

def obtenMasAlta(resultados): 

    # Acceder al primer resultado
    primer_resultado = resultados[0]

    # Acceder a la etiqueta con la puntuación más alta
    etiqueta_mas_probable = max(primer_resultado, key=lambda x: x['score'])['label']
    #print(etiqueta_mas_probable)  # Imprimirá 'ur' en este caso

    return etiqueta_mas_probable


def infiere(modelo, texto): 

    print("Estoy infiriendo el modelo: ", modelo)   
    headers = {"Authorization": f"Bearer {bridges.hug}", "x-wait-for-model": "true"}

    def query(payload):
        response = requests.post(modelo, headers=headers, json=payload)
        return response.json()
        
    output = query({
        "inputs": texto
    })

    return output

def traduccion_final(texto): 
    #Detecta que idiomas podrían ser: 
    idioma = obtenMasAlta(infiere(biblioteca_modelos.deteca_idioma, texto))

    funciones_inferencia = {
        'es': biblioteca_modelos.español_ingles,
        'pt': biblioteca_modelos.portugues_ingles,
        'it': biblioteca_modelos.italiano_ingles,
        'en': biblioteca_modelos.español_ingles
    }

    if idioma in funciones_inferencia:
        # print(f"Si, idioma {idioma}, está en la lista de funciones de inferencia.")
        # print(f" El idioma es {funciones_inferencia[idioma]} , ok...")
        texto = infiere(funciones_inferencia[idioma], texto)
        return texto[0]['translation_text']
    else:
        return "Lang Unknown"
    