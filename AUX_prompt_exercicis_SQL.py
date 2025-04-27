import os, json, groq

# ─── PARÀMETRES BÀSICS ────────────────────────────────────────────────
DIRECTORI = "data_exercicis"
os.makedirs(DIRECTORI, exist_ok=True)

CURS = "SQL"

CAPITOLS = [
    {
        "numero": 1,
        "titol": "Introducció a SQL i primeres consultes",
        "dificultat": "Fàcil",
        "temes": [
            "Què és SQL",
            "Bases de dades i taules",
            "Com funciona SELECT",
            "Primers SELECT * FROM taula"
        ]
    },
    {
        "numero": 2,
        "titol": "Filtrar dades amb WHERE",
        "dificultat": "Fàcil",
        "temes": [
            "Clàusula WHERE",
            "Operadors lògics (=, <>, >, <, >=, <=)",
            "Operadors booleans (AND, OR, NOT)",
            "Filtrar text, números i dates"
        ]
    },
    {
        "numero": 3,
        "titol": "Ordenar i limitar resultats",
        "dificultat": "Fàcil",
        "temes": [
            "ORDER BY ascendent i descendent",
            "LIMIT per limitar files",
            "OFFSET per saltar files",
            "Casos pràctics amb ordenació"
        ]
    },
    {
        "numero": 4,
        "titol": "Treballar amb funcions d'agregació",
        "dificultat": "Mitjà",
        "temes": [
            "Funcions COUNT, SUM, AVG, MIN, MAX",
            "GROUP BY per agrupar resultats",
            "HAVING per filtrar grups",
            "Diferència entre WHERE i HAVING"
        ]
    },
    {
        "numero": 5,
        "titol": "Joins: combinar taules",
        "dificultat": "Mitjà",
        "temes": [
            "INNER JOIN: obtenir coincidències",
            "LEFT JOIN: incloure totes les files d'una taula",
            "RIGHT JOIN i FULL JOIN",
            "Entendre claus primàries i estrangeres"
        ]
    },
    {
        "numero": 6,
        "titol": "Subconsultes i consultes avançades",
        "dificultat": "Mitjà",
        "temes": [
            "Subconsultes a SELECT, WHERE i FROM",
            "Operadors IN, ANY, ALL, EXISTS",
            "Consultes amb agregacions dins subconsultes",
            "Casos pràctics de subconsultes"
        ]
    },
    {
        "numero": 7,
        "titol": "Crear i modificar estructures de dades",
        "dificultat": "Mitjà",
        "temes": [
            "CREATE TABLE: crear taules",
            "ALTER TABLE: modificar columnes",
            "DROP TABLE: eliminar taules",
            "Tipus de dades bàsics (INTEGER, VARCHAR, DATE...)"
        ]
    },
    {
        "numero": 8,
        "titol": "Inserir, actualitzar i eliminar dades",
        "dificultat": "Mitjà",
        "temes": [
            "INSERT INTO: inserir registres",
            "UPDATE: modificar registres existents",
            "DELETE: eliminar registres",
            "Bones pràctiques per evitar errors catastròfics"
        ]
    },
    {
        "numero": 9,
        "titol": "Funcions de text, números i dates",
        "dificultat": "Avançat",
        "temes": [
            "Funcions de text: CONCAT, SUBSTRING, UPPER, LOWER",
            "Funcions numèriques: ROUND, FLOOR, CEIL",
            "Funcions de dates: NOW, DATEADD, DATEDIFF",
            "Aplicació pràctica en consultes reals"
        ]
    },
    {
        "numero": 10,
        "titol": "SQL per a l'anàlisi de dades",
        "dificultat": "Avançat",
        "temes": [
            "Càlculs de percentatges i ratios",
            "Casos d'ús amb PIVOT i CASE",
            "Agrupar dades per períodes (mes, any)",
            "Exemples reals d'analítica amb SQL"
        ]
    }
]


PROMPT_BASE = """
Ets un professor expert en Data Analytics i Data Science. 
El teu objectiu és crear capítols d'un curs pràctic amb EXACTAMENT 5 exercicis cadascun. Exercicis reals que utilitzin codi i fórmules 100% real, no inventat.

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
    "nom": "EXCEL", (pot ser SQL, PYTHON, EXCEL o DAX, segons el que es demani)
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
