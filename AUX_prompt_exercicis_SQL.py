import os, json, groq

# ─── PARÀMETRES BÀSICS ────────────────────────────────────────────────
DIRECTORI = "data_exercicis"
os.makedirs(DIRECTORI, exist_ok=True)

CURS = "XXXXXXXXXXXXXXXX"

CAPITOLS = [
    {
        "numero": 1,
        "titol": "Introducció a SQL i selecció de dades",
        "dificultat": "Fàcil",
        "temes": [
            "Entendre què és SQL",
            "Estructures bàsiques de base de dades: taules i columnes",
            "SELECT bàsic",
            "Filtres amb WHERE i operadors lògics"
        ]
    },
    {
        "numero": 2,
        "titol": "Ordenació, limitació i alias",
        "dificultat": "Fàcil",
        "temes": [
            "ORDER BY per ordenar resultats",
            "LIMIT per restringir files retornades",
            "Ús d'AS per alias de columnes i taules",
            "Comentaris en SQL"
        ]
    },
    {
        "numero": 3,
        "titol": "Funcions d'agregació i agrupació",
        "dificultat": "Fàcil",
        "temes": [
            "Funcions COUNT, SUM, AVG, MIN, MAX",
            "GROUP BY per agrupar resultats",
            "HAVING per filtrar agregacions",
            "Conceptes bàsics d'agrupació avançada"
        ]
    },
    {
        "numero": 4,
        "titol": "Joins entre taules",
        "dificultat": "Mitjà",
        "temes": [
            "INNER JOIN: combinar taules relacionades",
            "LEFT JOIN i RIGHT JOIN",
            "FULL JOIN",
            "Aliasing en joins complexos"
        ]
    },
    {
        "numero": 5,
        "titol": "Subconsultes i consultes anidades",
        "dificultat": "Mitjà",
        "temes": [
            "Subqueries a SELECT",
            "Subqueries a WHERE i FROM",
            "Comparació entre JOINs i Subqueries",
            "Subqueries correlacionades"
        ]
    },
    {
        "numero": 6,
        "titol": "Operadors avançats i filtres",
        "dificultat": "Mitjà",
        "temes": [
            "Ús de IN, NOT IN",
            "Ús de BETWEEN, LIKE i ILIKE",
            "Wildcard: %, _ en LIKE",
            "CASE WHEN per condicions dins SELECT"
        ]
    },
    {
        "numero": 7,
        "titol": "Funcions de text i data",
        "dificultat": "Mitjà",
        "temes": [
            "Manipulació de cadenes: LENGTH, UPPER, LOWER, CONCAT",
            "Extracció de subcadenes: SUBSTRING, LEFT, RIGHT",
            "Funcions de data: CURRENT_DATE, EXTRACT, DATE_TRUNC",
            "Operacions entre dates"
        ]
    },
    {
        "numero": 8,
        "titol": "CTE (Common Table Expressions) i modularització de consultes",
        "dificultat": "Avançat",
        "temes": [
            "Introducció a WITH",
            "Construir consultes modulars",
            "Millorar la llegibilitat amb CTEs",
            "CTEs recursius bàsics"
        ]
    },
    {
        "numero": 9,
        "titol": "Funcions analítiques (Window Functions)",
        "dificultat": "Avançat",
        "temes": [
            "Introducció a OVER()",
            "Funcions ROW_NUMBER, RANK, DENSE_RANK",
            "PARTITION BY i ORDER BY dins funcions analítiques",
            "SUM() OVER() i AVG() OVER() per anàlisi mòbil"
        ]
    },
    {
        "numero": 10,
        "titol": "Optimització de consultes i millors pràctiques",
        "dificultat": "Avançat",
        "temes": [
            "Indexació bàsica i impacte en rendiment",
            "Evitar consultes lentes: bones pràctiques",
            "Evitar N+1 Queries",
            "Lectura i interpretació de plans d'execució"
        ]
    }
]


PROMPT_BASE = """
Ets un professor expert en Data Analytics 
El teu objectiu és crear capítols d'un curs pràctic amb EXACTAMENT 5 exercicis cadascun. Exercicis reals que utilitzin codi i fórmules 100% real, no inventat.

Els exercicis poden ser de 4 tipus:
- "codi": exercicis pràctics de programació curta (1-5 línies de codi).
- "test": preguntes tipus test de 4 opcions (indicant quina és la correcta).
- "completar_codi": exercicis en que es dóna una part del codi i es demana completar-lo o afegir les parts que hi falten
- "IA": exercicis complexos que impliquen respostes llargues de codi que seran corregides mitjançant un LLM (simulant la correcció d’un professor). 

IMPORTANT: Les respostes sempre han de ser codi, exceptuant tipus test.

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
      "tipus": "codi",
      "descripcio": "Explicació didàctica del concepte, necessària perque l'alumne pugui resoldre l'exercici. Ha de ser completa com l'explicació d'un professor sobre un tema.",
      "enunciat": "Enunciat de l'exercici.",
      "solucio": "Resposta correcta a l'exercici, en cas que sigui tipus "exe" serà el resultat esperat del codi",
      "solucio_codi_1": "Codi de la solució, en tipus test serà null i en tipus codi i exe serà el codi de la solució. En cas d'excel, la solució en anlès, en altres cursos serà null",
      "solucio_codi_2": "En cas d'excel, la solució en castellà, en altres cursos serà null",
      "solucio_codi_2":null,
      "codi_a_completar": codi a completar, s'afegeix el parametre "<placeholder>" per les parts que s'hagin de completar. Per exemple: x + <placeholder> = 5,
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

    resposta = call_llm(PROMPT_BASE + frase)
    nom_fitxer = f"{CURS}_capitol_{cap['numero']}.json"
    desa(nom_fitxer, resposta)

print("🎯 Tots els capítols del curs EXCEL han estat creats correctament!")
