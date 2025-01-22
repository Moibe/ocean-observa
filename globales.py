import gradio as gr

#MAIN
version = "1.1.2"
env = "prod"
aplicacion = "observa"

seleccion_api = "eligeAOB" #eligeQuotaOCosto , eligeAOB o eligeGratisOCosto
max_size = 20 #queue size

#A o B
api_a = ("vikhyatk/moondream2", "gratis")
api_b = ("Moibe/observa", "gratis") #Se considera gratis pq aunqu eestá en Zero no cuesta minutos.

process_cost = 0
interface_api_name = "/answer_question" #El endpoint al que llamará client.


seto = "observa"
work = "picswap"
app_path = "/observa"
server_port=7833
#tema = tools.theme_selector()
tema = gr.themes.Default()
flag = "auto" #never, auto o manual.

neural_wait = 3
mensajes_lang = "es"