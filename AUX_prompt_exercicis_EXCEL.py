import os, json, groq, time

# ─── PARÀMETRES BÀSICS ────────────────────────────────────────────────
DIRECTORI = "data_exercicis"
os.makedirs(DIRECTORI, exist_ok=True)

CURS = "XXXXXXXXXX"

CAPITOLS = [
    {
        "numero": 1,
        "titol": "Introducció als Fulls de càlcul",
        "dificultat": "Fàcil",
        "temes": [
            "Què són els fulls de càlcul",
            "Estructura bàsica: files, columnes i cel·les",
            "Moviment i selecció eficient dins el full"
        ]
    },
    {
        "numero": 2,
        "titol": "Formats i primera personalització",
        "dificultat": "Fàcil",
        "temes": [
            "Formats de número, moneda, data i hora",
            "Pinzell de formats",
            "Ajustar amplades i alçades",
            "Primers formats ràpids de taula"
        ]
    },
    {
        "numero": 3,
        "titol": "Operacions bàsiques i Pegat especial",
        "dificultat": "Fàcil",
        "temes": [
            "Copiar, tallar i enganxar",
            "Pegat especial: valors, fórmules, transposar",
            "Buscar i reemplaçar amb caràcters comodí"
        ]
    },
    {
        "numero": 4,
        "titol": "Fórmules inicials i operacions bàsiques",
        "dificultat": "Fàcil",
        "temes": [
            "SUMA, RESTA, MULTIPLICACIÓ i DIVISIÓ",
            "Referències relatives i absolutes ($)",
            "Gestió d’errors comuns en fórmules"
        ]
    },
    {
        "numero": 5,
        "titol": "Gestió de Taules i Filtres",
        "dificultat": "Mitjà",
        "temes": [
            "Aplicar i gestionar filtres",
            "Convertir rangs en taules",
            "Segmentació de dades",
            "Bases de dades simples a Excel"
        ]
    },
    {
        "numero": 6,
        "titol": "Fórmules de text i neteja de dades",
        "dificultat": "Mitjà",
        "temes": [
            "Concatenació i manipulació de textos",
            "Funcions IZQUIERDA, DERECHA, EXTRAER",
            "Funcions HALLAR i SUBSTITUTE",
            "Neteja d'espais i correcció de textos"
        ]
    },
    {
        "numero": 7,
        "titol": "Anàlisi de dades amb Gràfics",
        "dificultat": "Mitjà",
        "temes": [
            "Crear i editar gràfics bàsics",
            "Tipus de gràfics: barres, línies, circulars",
            "Gràfics combinats",
            "Minigràfics i formats visuals"
        ]
    },
    {
        "numero": 8,
        "titol": "Fórmules lògiques i condicionals",
        "dificultat": "Mitjà",
        "temes": [
            "Funció SI i SI.ERROR",
            "Funcions Y i O",
            "SUMAR.SI, CONTAR.SI, PROMEDIO.SI",
            "Fórmules amb condicions complexes"
        ]
    },
    {
        "numero": 9,
        "titol": "Gestió de Dates i Temps",
        "dificultat": "Mitjà",
        "temes": [
            "Tractament de formats de dates i hores",
            "Funcions DIA, MES, ANY, HOY",
            "Càlculs d'edats, trimestres i períodes",
            "Operacions amb hores i minuts"
        ]
    },
    {
        "numero": 10,
        "titol": "Taules dinàmiques i informes visuals",
        "dificultat": "Avançat",
        "temes": [
            "Crear taules dinàmiques",
            "Filtrar i segmentar taules dinàmiques",
            "Crear gràfics dinàmics",
            "Personalitzar informes amb resum de dades"
        ]
    },
    {
        "numero": 11,
        "titol": "Eficiència amb Excel: Trucs i optimització",
        "dificultat": "Mitjà",
        "temes": [
            "Shortcuts de teclat essencials",
            "Enllaços dins del full i entre fulls",
            "Rastrejar valors i fórmules",
            "Accesos directes a utilitats amagades"
        ]
    },
    {
        "numero": 12,
        "titol": "Fórmules per a Cerca i Filtrat",
        "dificultat": "Mitjà",
        "temes": [
            "BUSCARX (i diferències amb BUSCARV, BUSCARH)",
            "FILTRAR rangs segons condicions",
            "Buscar dins del text",
            "Creuar taules amb BUSCARX complexos"
        ]
    },
    {
        "numero": 13,
        "titol": "Més utilitats d'Excel per a dades",
        "dificultat": "Mitjà",
        "temes": [
            "Text en columnes",
            "Importar i netejar CSVs",
            "Treure duplicats amb eina o fórmula UNICOS",
            "Buscar Objectiu i Solver per optimitzacions"
        ]
    },
    {
        "numero": 14,
        "titol": "Formats personalitzats i condicions avançades",
        "dificultat": "Avançat",
        "temes": [
            "Formats personalitzats de números i dates",
            "Formats condicionals amb fórmules avançades",
            "Validació de dades amb fórmules personalitzades",
            "Secrets de les taules dinàmiques avançades"
        ]
    },
    {
        "numero": 15,
        "titol": "Automatització amb Macros (VBA Bàsic)",
        "dificultat": "Avançat",
        "temes": [
            "Què són les macros i VBA",
            "Gravar macros senzilles",
            "Editar i executar una macro",
            "Aplicacions pràctiques d'automatització"
        ]
    }
]

# Temporal, per crear el que falta
CAPITOLS = [
    {
        "numero": 1,
        "titol": "Introducció als Fulls de càlcul",
        "dificultat": "Fàcil",
        "temes": [
            "Què són els fulls de càlcul",
            "Estructura bàsica: files, columnes i cel·les",
            "Moviment i selecció eficient dins el full"
        ]
    },
    {
        "numero": 2,
        "titol": "Formats i primera personalització",
        "dificultat": "Fàcil",
        "temes": [
            "Formats de número, moneda, data i hora",
            "Pinzell de formats",
            "Ajustar amplades i alçades",
            "Primers formats ràpids de taula"
        ]
    },
    {
        "numero": 3,
        "titol": "Operacions bàsiques i Pegat especial",
        "dificultat": "Fàcil",
        "temes": [
            "Copiar, tallar i enganxar",
            "Pegat especial: valors, fórmules, transposar",
            "Buscar i reemplaçar amb caràcters comodí"
        ]
    },
    {
        "numero": 4,
        "titol": "Fórmules inicials i operacions bàsiques",
        "dificultat": "Fàcil",
        "temes": [
            "SUMA, RESTA, MULTIPLICACIÓ i DIVISIÓ",
            "Referències relatives i absolutes ($)",
            "Gestió d’errors comuns en fórmules"
        ]
    },
    {
        "numero": 5,
        "titol": "Gestió de Taules i Filtres",
        "dificultat": "Mitjà",
        "temes": [
            "Aplicar i gestionar filtres",
            "Convertir rangs en taules",
            "Segmentació de dades",
            "Bases de dades simples a Excel"
        ]
    },
    {
        "numero": 6,
        "titol": "Fórmules de text i neteja de dades",
        "dificultat": "Mitjà",
        "temes": [
            "Concatenació i manipulació de textos",
            "Funcions IZQUIERDA, DERECHA, EXTRAER",
            "Funcions HALLAR i SUBSTITUTE",
            "Neteja d'espais i correcció de textos"
        ]
    },
    {
        "numero": 7,
        "titol": "Anàlisi de dades amb Gràfics",
        "dificultat": "Mitjà",
        "temes": [
            "Crear i editar gràfics bàsics",
            "Tipus de gràfics: barres, línies, circulars",
            "Gràfics combinats",
            "Minigràfics i formats visuals"
        ]
    }
]



PROMPT_BASE = """
Ets un professor expert en Data Analytics i Data Science. 
El teu objectiu és crear capítols d'un curs pràctic amb EXACTAMENT 5 exercicis cadascun. Exercicis reals que utilitzin codi i fórmules 100% real, no inventat.
En Excel utilitza solució codi 1 per posar la fórmula en angles i solució codi 2 per posar la fórmula en castellà, no utilizis formules en catala.	

Els exercicis poden ser de 4 tipus:
- "codi": exercicis pràctics de programació curta (1-5 línies de codi).
- "test": preguntes tipus test de 4 opcions (indicant quina és la correcta).
- "exe": exercicis per completar o corregir fragments de codi pre-existents (només aplicable a cursos de Python).
- "IA": exercicis complexos que impliquen respostes llargues de codi o respostes obertes que seran corregides mitjançant un LLM (simulant la correcció d’un professor).

Instruccions importants:
- Tots els exercicis s'han de poder resoldre directament amb les dades generades (enunciat, resposta), no es pot fer referència a cap altre fitxer o base de dades externa.
- Cap exercici pot fer referencia a que l'usuari ha de fer servir una eina externa (excel, etc.) per resoldre'l.
- Fes els enunciats clars, directes i pràctics, adaptats al nivell de dificultat indicat (Fàcil, Mitjà, Avançat).
- Si generes un exercici de tipus "test", recorda afegir 4 opcions amb la resposta correcta.
- Per "IA", proposa casos pràctics més llargs i reals (com mini-projectes o anàlisi de casos).
- Sempre segueix l'estructura JSON que et proporciono sense modificar-la.
- El camp descripció és molt important, ja que és la part pedagògica del curs. Ha de ser clara i útil per a l'alumne.

IMPORTANT: 
- No saltis cap camp del JSON.
- No afegeixis text fora del JSON.

Ets un formador rigorós però optimista. El teu objectiu és ajudar l'alumne a avançar pas a pas cap a la seva màxima autonomia.
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
      "tipus": "codi", (pot ser 'codi' o 'test'. Només per exercicis del curs Python pot ser 'exe' ja que el codi es pot executar)
      "descripcio": "Explicació didàctica del concepte, necessària perque l'alumne pugui resoldre l'exercici. Ha de ser completa com l'explicació d'un professor sobre un tema.",
      "enunciat": "Enunciat de l'exercici.",
      "solucio": "Resposta correcta a l'exercici, en cas que sigui tipus "exe" serà el resultat esperat del codi",
      "solucio_codi_1": "Codi de la solució, en tipus test serà null i en tipus codi i exe serà el codi de la solució. En cas d'excel, la solució en anlès, en altres cursos serà null",
      "solucio_codi_2": "En cas d'excel, la solució en castellà, en altres cursos serà null",
      "solucio_codi_2":null,
      "codi_a_completar":null,
      "temps_estimat_minuts": 5,
      "respostes_test": [],
      "pista_1": "Primera pista. (Una frase)",
      "pista_2": "Segona pista. (Una frase",
      "imatge_1": null,
      "descripcio_imatge_1": null,
      "imatge_2": null,
      "descripcio_imatge_2": null
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
        f"Cada capítol ha de contenir EXACTAMENT 5 exercicis, variats entre 'codi' i 'test'. "
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