# MGPEB - Fase 2 - Gabriel Romero - RM 575479
from datetime import datetime, timedelta # importa datetime e timedelta para calcular e formatar o horario de pouso

# identificação da lista e seus respectivos dicionarios
modulos = [
    {"nome": "laboratorio", "combustivel" : 18, "massa": 4, "criticidade" : 1, "chegada" : "10:15", "erro_sensores": False, "altitude" : 100, "velocidade" : 10}, # laboratorio: pesquisa cientifica, criticidade baixa
    {"nome": "suprimentos", "combustivel" : 65, "massa": 7, "criticidade" : 3, "chegada" : "10:40", "erro_sensores": False, "altitude" : 100, "velocidade" : 10}, # suprimentos: comida, agua e pecas de reposicao
    {"nome": "lancador",  "combustivel" : 80, "massa": 9, "criticidade" : 4, "chegada" : "11:10", "erro_sensores": True, "altitude" : 100, "velocidade" : 10}, # lancador: veiculo de subida (MAV), o foguete de retorno
    {"nome": "habitat", "combustivel" : 45, "massa": 12, "criticidade" : 5, "chegada" : "11:30", "erro_sensores": False, "altitude" : 100, "velocidade" : 10}, # habitat: suporte a vida, onde a tripulacao vive
    {"nome": "energia", "combustivel" : 55, "massa": 8, "criticidade" : 5, "chegada" : "12:00", "erro_sensores": False, "altitude" : 100, "velocidade" : 10}, # energia: usina que gera eletricidade para a base
    {"nome": "isru", "combustivel" : 12, "massa": 6, "criticidade" : 4, "chegada" : "12:25", "erro_sensores": False, "altitude" : 100, "velocidade" : 10} # isru: usina que produz oxigenio e combustivel do ar de Marte
    ]

#listas e variaveis criadas vazias para mudar o status dos modulos
pousados = []
grupo_normal = []
em_espera = []
alerta = []
historico = []
abortado = []
area_livre = True

# busca linear: percorre todos os modulos e guarda o de menor combustivel (detector de emergencia)
menor = modulos[0]
for modulo in modulos:
    if modulo["combustivel"] < menor["combustivel"]:
        menor = modulo
print("Modulo em emergencia (menos combustivel):")
print(menor)

# separa os modulos em grupos conforme a faixa de combustivel: aborta, alerta ou normal 
for modulo in modulos:
    # avalia o minimo de combustivel para pouso
    if modulo["combustivel"] < 10:
        abortado.append(modulo)
        print(f"ALERTA: {modulo['nome']} com combustivel baixo do necessario para pouso, seguirá em orbita")
    # verificação de alerta para prioridade de pouso
    elif modulo["combustivel"] >= 10 and modulo["combustivel"] <= 15:
        alerta.append(modulo)
    # combustivel acima de 15%: vai para o grupo normal (a ordenacao por criticidade vem depois)
    else:
        grupo_normal.append(modulo)
contador_pouso = 0
# horario base: ponto de partida do cronograma de pouso (cada pouso soma 30 min a partir das 10:00)
horario_base = datetime.strptime("10:00", "%H:%M")
# monta a fila de prioridade: alerta por menor combustivel, normal por maior criticidade, e junta os dois (alerta primeiro)
fila_alerta = sorted(alerta, key=lambda m: m["combustivel"])
fila_normal = sorted(grupo_normal, key=lambda m: m["criticidade"], reverse=True)
ordem_pouso = fila_alerta + fila_normal
print("=== Autorizacao de pouso (ordem de prioridade) ===")

# autorização de pouso
for modulo in ordem_pouso:
    if modulo["combustivel"] >= 10 and area_livre and not modulo["erro_sensores"] : 
        modulo["altitude"] = 0
        modulo["velocidade"] = 0
        if modulo["altitude"] == 0 and modulo["velocidade"] == 0 and not modulo["erro_sensores"]:
            pousados.append(modulo)
            historico.append(modulo)   # <-- essa é a PILHA
            modulo["hora_pouso"] = (horario_base + timedelta(minutes=30 * contador_pouso)).strftime("%H:%M")
            contador_pouso = contador_pouso + 1
            print(f"{modulo['nome']}: POUSADO com sucesso")
    else:
        em_espera.append(modulo)       # travou
        print(f"{modulo['nome']}: EM ESPERA - PROBLEMA IDENTIFICADO")

print("=== Historico de pousos (ordem real, horario corrigido) ===")
for modulo in historico:
    print(f"{modulo['nome']} - pousou as {modulo['hora_pouso']}")

print(f"Ultimo pouso registrado (topo da pilha): {historico[-1]['nome']} as {historico[-1]['hora_pouso']}")

print("=== Pendencias e ocorrencias ===")
if alerta:
    print("Em alerta (combustivel baixo, mas pousou):")
    for modulo in alerta:
        print(f"- {modulo['nome']}")
if em_espera:
    print("Em espera (travaram, problema identificado):")
    for modulo in em_espera:
        print(f"- {modulo['nome']}")
if abortado:
    print("Abortados (seguem em orbita de Marte):")
    for modulo in abortado:
        print(f"- {modulo['nome']}")