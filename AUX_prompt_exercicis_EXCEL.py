import os, json, groq, time

# ─── PARÀMETRES BÀSICS ────────────────────────────────────────────────
DIRECTORI = "data_exercicis"
os.makedirs(DIRECTORI, exist_ok=True)

CURS = "Excel"

CAPITOLS = [
  {
    "numero": 1,
    "titol": "Fórmules bàsiques i operacions elementals",
    "dificultat": "Fàcil",
    "descripcio": "Aprèn a fer operacions bàsiques a Excel com sumar, restar, multiplicar o dividir, i descobreix com funcionen les referències de cel·les.",
    "temes": [
      "Referenciar una cel·la o rang (símbol = o + per començar una fórmula)",
      "SUMA",
      "CONTAR",
      "Operadors matemàtics",
      "Combinar fórmules i operadors matemàtics (ex: mitjana amb SUMA()/CONTAR())"
    ]
  },
  {
    "numero": 2,
    "titol": "Referències absolutes i relatives amb $",
    "dificultat": "Fàcil",
    "descripcio": "Entén com funciona el símbol $ per fixar cel·les i construir fórmules més potents.",
    "temes": [
      "Referència absoluta o relativa (i impacte de $)",
      "Fixar una cel·la o rang",
      "Fixar només les files",
      "Fixar només les columnes",
      "Rang acumulatiu (ex: C$1:C1)"
    ]
  },
  {
    "numero": 3,
    "titol": "Funcions numèriques útils",
    "dificultat": "Fàcil",
    "descripcio": "Descobreix funcions que t’ajuden a analitzar dades numèriques i fer càlculs ràpids.",
    "temes": [
      "MIN / MAX",
      "PROMEDIO",
      "REDONDEAR (MÁS / MENOS) i redondeig a desenes",
      "SUMAPRODUCTO",
      "ALEATORIO / ALEATORIO.ENTRE"
    ]
  },
  {
    "numero": 4,
    "titol": "Funcions condicionals",
    "dificultat": "Mitjà",
    "descripcio": "Aprèn a aplicar condicions a les fórmules per controlar els resultats segons criteris específics.",
    "temes": [
      "SI",
      "SI.CONJUNTO",
      "Anidar múltiples SI",
      "Y i O amb SI",
      "SUMAR.SI, CONTAR.SI, MAX.SI, i versions CONJUNTO",
      "SI.ERROR"
    ]
  },
  {
    "numero": 5,
    "titol": "Treballar amb dates i hores",
    "dificultat": "Mitjà",
    "descripcio": "Gestiona i transforma valors de data i hora amb funcions dedicades.",
    "temes": [
      "Hora com a número (sumar/restar dies)",
      "HOY / AHORA",
      "AÑO, MES, DIA",
      "HORA, MINUTO, SEGUNDO",
      "FECHA.MES",
      "FRAC.AÑO (ex: càlcul de trimestre)"
    ]
  },
  {
    "numero": 6,
    "titol": "Funcions de text i manipulació de cadenes",
    "dificultat": "Mitjà",
    "descripcio": "Manipula textos i extreu informació rellevant amb funcions de text potents.",
    "temes": [
      "TEXTO (formats com 'aaaa-dd')",
      "Concatenar textos (ex: texto + 'kg')",
      "IZQUIERDA, DERECHA",
      "EXTRAER",
      "LARGO",
      "HALLAR",
      "Combinació EXTRAER i HALLAR",
      "SUSTITUIR"
    ]
  },
  {
    "numero": 7,
    "titol": "Funcions matricials i llistes dinàmiques",
    "dificultat": "Mitjà",
    "descripcio": "Crea resultats dinàmics i automàtics amb funcions matricials modernes.",
    "temes": [
      "FILTRAR",
      "UNICO",
      "ORDENAR / TRANSPOSAR",
      "SECUENCIA"
    ]
  },
  {
    "numero": 8,
    "titol": "Funcions de cerca i referència",
    "dificultat": "Mitjà",
    "descripcio": "Cerca valors dins taules i treballa amb cel·les de forma dinàmica.",
    "temes": [
      "BUSCARX",
      "INDICE / COINCIDIR",
      "INDIRECTO",
      "FILA/COLUMNA + INDIRECTO"
    ]
  },
  {
    "numero": 9,
    "titol": "Trucs avançats amb fórmules combinades",
    "dificultat": "Avançat",
    "descripcio": "Aprèn combinacions potents de funcions per resoldre problemes pràctics amb elegància.",
    "temes": [
      "SI + CONTAR.SI per identificar valors repetits",
      "BUSCARX amb múltiples criteris concatenats",
      "BUSCAR + HALLAR per classificar textos segons paraules clau",
      "SUMAPRODUCTO per comptar amb múltiples condicions",
      "Comptar valors únics (=SUMA(1/COMPTAR.SI(A2:A100, A2:A100)))"
    ]
  }
]


PROMPT_BASE = """
Ets un professor expert en Data Analytics i Data Science. 
El teu objectiu és crear capítols d'un curs pràctic amb EXACTAMENT 5 exercicis cadascun. Exercicis reals que utilitzin codi i fórmules 100% reals, no inventat.
En Excel utilitza solució codi 1 per posar la fórmula en angles i solució codi 2 per posar la fórmula en castellà, no utilizis formules en catala.
Tots els capítols fan referència a un curs d'Excel enfocat a les fòrmules.

Els exercicis poden ser de 4 tipus (han de ser variats):
- "codi": exercicis pràctics de programació curta (1-5 línies de codi).
- "test": preguntes tipus test de 4 opcions (indicant quina és la correcta).
- "completar": exercicis pràctics de programació on l'alumne ha d'omplir el codi que falta. La solució és el codi complet.

Instruccions importants:
- Tots els exercicis s'han de poder resoldre directament amb les dades generades (enunciat, resposta), no es pot fer referència a cap altre fitxer o base de dades externa.
- Cap exercici pot fer referencia a que l'usuari ha de fer servir una eina externa (excel, etc.) per resoldre'l.
- Fes els enunciats clars, directes i pràctics, adaptats al nivell de dificultat indicat (Fàcil, Mitjà, Avançat).
- Si generes un exercici de tipus "test", recorda afegir 4 opcions amb la resposta correcta.
- Sempre segueix l'estructura JSON que et proporciono sense modificar-la.
- El camp descripció és molt important, ja que és la part pedagògica del curs. Ha de ser clara i útil per a l'alumne.

IMPORTANT: 
- No saltis cap camp del JSON.
- No afegeixis text fora del JSON.
"""

# ─── GROQ ─────────────────────────────────────────────────────────────
KEY = os.getenv("GROQ_API_KEY")
client = groq.Groq(api_key=KEY)

def call_llm(prompt: str) -> str:
    try:
        chat = client.chat.completions.create(
            model="meta-llama/llama-4-maverick-17b-128e-instruct",
            messages=[{"role": "user", "content": prompt}],
        )
        return chat.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ Error greu cridant a l'API: {e}")
        raise SystemExit("Aturant execució per error greu a la crida de l'API.")

# ─── HELPERS ──────────────────────────────────────────────────────────
def bloc_json(text: str) -> str:
    i, j = text.find("{"), text.rfind("}")
    if i == -1 or j == -1 or j <= i:
        raise ValueError("Cap JSON trobat o mal format.")
    return text[i:j+1]

def desa(nom_fitxer: str, raw: str):
    path = os.path.join(DIRECTORI, nom_fitxer)
    data = json.loads(bloc_json(raw))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✅ Creat: {path}")



# ─── CONTEXT DEL FORMAT JSON ──────────────────────────────────────────
context_estructura = r"""
{
  "curs": {
    "nom": "Excel", (pot ser SQL, PYTHON, EXCEL o DAX, segons el que es demani)
    "descripcio": "Aprèn a dominar Excel des de zero fins a nivell avançat, aplicat a l'anàlisi de dades.",
    "color_fons": "#F4F8F4"
  },
  "capitol": {
    "titol": "Títol del capítol",
    "numero": 1,
    "dificultat": "Fàcil",
    "preu": 0.00
  },
  "exercicis": [
    {
      "numero": 1,
      "titol": "Títol de l'exercici",
      "tipus": "codi", (pot ser 'codi' o 'test')
      "descripcio": "Explicació didàctica del concepte, necessària perque l'alumne pugui resoldre l'exercici. Ha de ser completa com l'explicació d'un professor sobre un tema. Dóna exemples però que no siguin exactament iguals que la solució.",
      "enunciat": "Enunciat de l'exercici. Si vols incloure una taula, utilitza el camp 'taula'.",
      "solucio": "Resposta correcta a l'exercici per tipus test, en la resta null",
      "solucio_codi_1": "Codi de la solució, en tipus test serà null i en tipus codi i exe serà el codi de la solució. En cas d'excel, la solució en anlès, en altres cursos serà null",
      "solucio_codi_2": "En cas d'excel, la solució en castellà, en altres cursos serà null",
      "solucio_codi_2":null,
      "codi_a_completar":"Només en exercicis tipus completar_codi, el codi a completar per l'alumne. En altres tipus serà null",
      "temps_estimat_minuts": 5,
      "respostes_test": ["Resposta 1", "Resposta 2", "Resposta 3", "Resposta 4"], (només si és tipus test, sino null)
      "pista_1": "Primera pista. (Una frase)",
      "pista_2": "Segona pista. (Una frase",
      "imatge_1": null,
      "descripcio_imatge_1": null,
      "imatge_2": null,
      "descripcio_imatge_2": null
      "taula": {"Camp1": ["Valor1","Valor2"], "Camp2": ["Valor3","Valor4"]}, (En cas de que es vulgui incloure una taula a l'enunciat, en format JSON. En cas contrari, null)
    }
  ]
}
"""



# ─── BUCLE PRINCIPAL ──────────────────────────────────────────────────
for cap in CAPITOLS:
    temes_str = ", ".join(cap['temes'])
    frase = (
        f"Genera el JSON per al capítol {cap['numero']} del curs {CURS}. "
        f"El títol del capítol és: {cap['titol']}. "
        f"La dificultat del capítol és: {cap['dificultat']}. "
        f"Els exercicis han de cobrir aquests temes: {temes_str}. "
        f"Segueix l'estructura exacta següent: {context_estructura}\n\n"
    )

    # Nova part: retries
    intents = 0
    max_intents = 3
    mentre_no_aconseguit = True

    while mentre_no_aconseguit and intents < max_intents:
        intents += 1
        try:
            print(f"🛠️ Generant capítol {cap['numero']} (Intent {intents})...")
            resposta = call_llm(PROMPT_BASE + frase)
            nom_fitxer = f"{CURS}_capitol_{cap['numero']}.json"
            desa(nom_fitxer, resposta)
            mentre_no_aconseguit = False
        except (ValueError, json.JSONDecodeError) as e:
            print(f"⚠️ Error processant JSON: {e}")
            if intents < max_intents:
                print("🔄 Reintentant en 2 segons...")
                time.sleep(2)
            else:
                print(f"❌ No s'ha pogut generar correctament el capítol {cap['numero']} després de {max_intents} intents.")
                raise SystemExit(f"Aturant execució perquè el capítol {cap['numero']} ha fallat massa intents.")

print("🎯 Tots els capítols del curs EXCEL han estat creats correctament!")