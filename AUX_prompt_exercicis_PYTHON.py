import os, json, groq

# ─── PARÀMETRES BÀSICS ────────────────────────────────────────────────
DIRECTORI = "data_exercicis"
os.makedirs(DIRECTORI, exist_ok=True)

CURS = "PYTHON"

CAPITOLS = [
    # Introducció a Python
    {
        "numero": 1,
        "titol": "Variables i tipus de dades",
        "dificultat": "Fàcil",
        "temes": [
            "Creació de variables",
            "Tipus bàsics: int, float, str, bool",
            "Conversió de tipus",
            "Bones pràctiques de nomenclatura"
        ]
    },
    {
        "numero": 2,
        "titol": "Llistes i tuples",
        "dificultat": "Fàcil",
        "temes": [
            "Crear i accedir a llistes",
            "Modificació d'elements",
            "Llistes vs Tuples",
            "Iterar sobre llistes"
        ]
    },
    {
        "numero": 3,
        "titol": "Diccionaris i conjunts",
        "dificultat": "Mitjà",
        "temes": [
            "Crear i accedir a diccionaris",
            "Actualitzar valors",
            "Ús de conjunts (sets)",
            "Operacions entre conjunts"
        ]
    },
    {
        "numero": 4,
        "titol": "Funcions i paràmetres",
        "dificultat": "Mitjà",
        "temes": [
            "Definir funcions",
            "Paràmetres i valors per defecte",
            "Retornar valors",
            "Funcions lambda"
        ]
    },
    {
        "numero": 5,
        "titol": "Classes i introducció a OOP",
        "dificultat": "Mitjà",
        "temes": [
            "Definir classes i objectes",
            "Atributs i mètodes",
            "El mètode __init__",
            "Encapsulació bàsica"
        ]
    },

    # Pandas
    {
        "numero": 6,
        "titol": "Introducció a Pandas",
        "dificultat": "Mitjà",
        "temes": [
            "Crear DataFrames i Series",
            "Accedir a dades",
            "Filtres i selecció condicional",
            "Descripció de dades (describe, info)"
        ]
    },
    {
        "numero": 7,
        "titol": "Manipulació de dades amb Pandas",
        "dificultat": "Mitjà",
        "temes": [
            "Agrupacions amb groupby",
            "Merge i Join de taules",
            "Tractar valors nuls",
            "Aplicar funcions (apply, map)"
        ]
    },

    # Models de Machine Learning amb Scikit-learn
    {
        "numero": 8,
        "titol": "Regressió lineal amb Scikit-learn",
        "dificultat": "Avançat",
        "temes": [
            "Creació de datasets simples",
            "Separar dades d'entrenament i test",
            "Entrenar models de regressió",
            "Interpretar mètriques de regressió (MSE, R2)"
        ]
    },
    {
        "numero": 9,
        "titol": "Classificació amb Scikit-learn",
        "dificultat": "Avançat",
        "temes": [
            "Entrenar un model de classificació",
            "Mètriques de classificació (accuracy, precision, recall)",
            "Matriu de confusió",
            "Avaluació del model"
        ]
    },
    {
        "numero": 10,
        "titol": "Clustering amb Scikit-learn",
        "dificultat": "Avançat",
        "temes": [
            "K-means clustering",
            "Elbow method",
            "Interpretar resultats de clustering",
            "Aplicacions pràctiques del clustering"
        ]
    }
]

PROMPT_BASE = """
Ets un professor expert en Data Analytics i Data Science. 
El teu objectiu és crear capítols d'un curs pràctic amb EXACTAMENT 5 exercicis cadascun. Exercicis reals que utilitzin codi i fórmules 100% reals, no inventades.

Els exercicis poden ser de 4 tipus:
- "codi": exercicis pràctics de programació curta (només per cursos de SQL, Excel o DAX).
- "exe": exercicis pràctics de programació curta EN PYTHON (1-5 línies de codi, executables directament).
- "test": preguntes tipus test de 4 opcions (indicant quina és la correcta).
- "IA": exercicis llargs (per exemple, entrenar models de ML en Python) que seran corregits per un LLM.

Instruccions importants:
- Tots els exercicis s'han de poder resoldre directament amb les dades generades (enunciat, resposta), no es pot fer referència a cap altre fitxer o base de dades externa.
- Si generes un exercici de tipus "test", recorda afegir 4 opcions amb la resposta correcta.
- Segueix estrictament l'estructura JSON que et proporciono sense modificar-la.
- El camp descripció és molt important: ha de ser una explicació didàctica necessària per resoldre l'exercici. Com si un professor t'expliqués el tema abans de passar a resoldre l'exercici, inclou exemples de codi, sense donar directament la resposta identica.

IMPORTANT:
- No saltis cap camp del JSON.
- No afegeixis text fora del JSON.
- Sigues didàctic i extens en el camp descripció.

Ets un formador rigorós però motivador. El teu objectiu és ajudar l'alumne a avançar pas a pas cap a la seva màxima autonomia.
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
    "nom": "PYTHON",
    "descripcio": "Domina Python per a l'anàlisi de dades, des de programació bàsica fins a models de Machine Learning aplicats.",
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
      "tipus": "exe",
      "descripcio": "Explicació didàctica necessària per resoldre l'exercici. Com si un professor t'expliqués el tema abans de passar a resoldre l'exercici. ",
      "enunciat": "Enunciat clar de l'exercici.",
      "solucio": "Resposta correcta.",
      "solucio_codi_1": "Codi de la solució (si aplica).",
      "solucio_codi_2": null,
      "temps_estimat_minuts": 5,
      "respostes_test": [],
      "pista_1": "Primera pista.",
      "pista_2": "Segona pista.",
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
        f"Cada capítol ha de contenir EXACTAMENT 5 exercicis, barrejant tipus 'exe', 'test' i 'IA' segons la complexitat. "
        f"Segueix l'estructura exacta següent: {context_estructura}\n\n"
    )

    resposta = call_llm(PROMPT_BASE + frase)
    nom_fitxer = f"{CURS}_capitol_{cap['numero']}.json"
    desa(nom_fitxer, resposta)

print("🎯 Tots els capítols del curs PYTHON han estat creats correctament!")
