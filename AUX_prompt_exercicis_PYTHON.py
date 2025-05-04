import os, json, groq, time

# ─── PARÀMETRES BÀSICS ────────────────────────────────────────────────
DIRECTORI = "data_exercicis"
os.makedirs(DIRECTORI, exist_ok=True)

CURS = "Python"

CAPITOLS = [
  {
    "numero": 1,
    "titol": "Introducció a Python",
    "dificultat": "Fàcil",
    "descripcio": "Configura el teu entorn i crea els teus primers scripts Python per començar amb bon peu.",
    "temes": [
      "Instal·lació i primer script",
      "Imprimir per pantalla amb print()",
      "Comentaris i bones pràctiques",
      "Errors habituals de sintaxi",
      "Execució en entorns com Jupyter i Colab"
    ]
  },
  {
    "numero": 2,
    "titol": "Variables i Tipus de Dades",
    "dificultat": "Fàcil",
    "descripcio": "Aprèn a treballar amb diferents tipus de dades i fer càlculs bàsics amb Python.",
    "temes": [
      "Assignació de variables",
      "Tipus bàsics: int, float, str, bool",
      "Conversió entre tipus",
      "Operadors bàsics",
      "Funcions builtin com type(), len(), round()"
    ]
  },
  {
    "numero": 3,
    "titol": "Estructures de Dades",
    "dificultat": "Fàcil",
    "descripcio": "Domina les estructures fonamentals com llistes, tuples i diccionaris.",
    "temes": [
      "Llistes: creació, accés, slicing",
      "Tuples i la seva immutabilitat",
      "Diccionaris: claus i valors",
      "Sets: elements únics",
      "Iterar sobre col·leccions"
    ]
  },
  {
    "numero": 4,
    "titol": "Control de Flux",
    "dificultat": "Mitjà",
    "descripcio": "Controla el flux del teu programa amb condicions i bucles.",
    "temes": [
      "Condicions if, elif, else",
      "Operadors de comparació i lògics",
      "Bucle for i while",
      "Control de bucles amb break i continue",
      "Comprehensions (llistes i diccionaris)"
    ]
  },
  {
    "numero": 5,
    "titol": "Funcions i Estructures Modulars",
    "dificultat": "Mitjà",
    "descripcio": "Aprèn a definir funcions per reutilitzar codi i millorar l'estructura del teu projecte.",
    "temes": [
      "Definir funcions amb def",
      "Arguments i valors de retorn",
      "Funcions amb valors per defecte",
      "Scope i variables locals",
      "Importar mòduls i crear-ne"
    ]
  },
  {
    "numero": 6,
    "titol": "Introducció a Numpy",
    "dificultat": "Mitjà",
    "descripcio": "Descobreix Numpy per fer càlculs numèrics eficients amb arrays.",
    "temes": [
      "Arrays vs llistes",
      "Creació i manipulació d'arrays",
      "Indexació i slicing",
      "Operacions vectoritzades",
      "Funcions estadístiques bàsiques"
    ]
  },
  {
    "numero": 7,
    "titol": "Primer contacte amb Pandas",
    "dificultat": "Mitjà",
    "descripcio": "Comença a treballar amb dades estructurades fent servir Pandas.",
    "temes": [
      "Crear Series i DataFrames",
      "Llegir dades: CSV, Excel",
      "Accedir a files i columnes",
      "Filtrar i seleccionar dades",
      "Operacions bàsiques amb dades"
    ]
  },
  {
    "numero": 8,
    "titol": "Transformació de dades amb Pandas",
    "dificultat": "Avançat",
    "descripcio": "Aprèn a netejar, transformar i agrupar dades per extreure'n valor.",
    "temes": [
      "Tractar valors nuls",
      "Aplicar funcions amb apply()",
      "Agrupar amb groupby()",
      "Ordenar i reindexar",
      "Canviar tipus de dades i renombrar columnes"
    ]
  },
  {
    "numero": 9,
    "titol": "Visualització amb Matplotlib i Seaborn",
    "dificultat": "Avançat",
    "descripcio": "Crea gràfics atractius per interpretar i comunicar les teves dades.",
    "temes": [
      "Gràfics bàsics amb matplotlib.pyplot",
      "Estil i format dels gràfics",
      "Introducció a Seaborn",
      "Histogrames, barres i boxplots",
      "Exportar gràfics a imatge"
    ]
  },
  {
    "numero": 10,
    "titol": "Projecte Final: Anàlisi d’un conjunt de dades",
    "dificultat": "Avançat",
    "descripcio": "Integra tot l’après en un projecte d’anàlisi de dades del món real.",
    "temes": [
      "Carregar i explorar un dataset real",
      "Aplicar transformacions i càlculs amb Pandas",
      "Visualitzar patrons amb gràfics",
      "Fer servir funcions per modularitzar el procés",
      "Exportar resultats a CSV o Excel"
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
    chat = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
    )
    return chat.choices[0].message.content.strip()

# ─── HELPERS ──────────────────────────────────────────────────────────
def bloc_json(text: str) -> str:
    i, j = text.find("{"), text.rfind("}")
    if i == -1 or j == -1 or j <= i:
        raise ValueError("Cap JSON trobat")
    return text[i:j+1]

def desa(nom_fitxer: str, raw: str):
    path = os.path.join(DIRECTORI, nom_fitxer)
    try:
        data = json.loads(bloc_json(raw))
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✅ Creat: {path}")
    except Exception as e:
        print(f"⚠️ Error desant {nom_fitxer}: {e}")

# ─── CONTEXT DEL FORMAT JSON ──────────────────────────────────────────
context_estructura = r"""
{
  "curs": {
    "nom": "Python", 
    "subnom": "Data Analytics",
    "descripcio": "Aprèn a dominar Python per l'anàlisi de dades amb aquest curs pràctic.",
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
      "tipus": "codi", (pot ser 'codi', 'completar' o 'test')
      "descripcio": "Explicació didàctica del concepte, necessària perque l'alumne pugui resoldre l'exercici. Ha de ser completa com l'explicació d'un professor sobre un tema. Dóna exemples però que no siguin exactament iguals que la solució.",
      "enunciat": "Enunciat de l'exercici. Si vols incloure una taula, utilitza el camp 'taula'.",
      "solucio": "Resposta correcta a l'exercici per tipus test, en la resta null",
      "solucio_codi_1": "Codi de la solució, en tipus test serà null i en tipus codi i exe serà el codi de la solució. En cas d'excel, la solució en anlès, en altres cursos serà null",
      "solucio_codi_2": "En cas d'excel, la solució en castellà, en altres cursos serà null",
      "solucio_codi_2":null,
      "codi_a_completar":"Només en exercicis tipus completar_codi, el codi a completar per l'alumne. En altres tipus serà null. S'ha de posar <placeholder> on s'ha d'emplenar el codi.",
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

print("🎯 Tots els capítols del curs PYTHON han estat creats correctament!")