import os, json, sqlite3, groq

# ─── PARÀMETRES ───────────────────────────────────────────────────────
DIRECTORI = "data_exercicis"
CURS = "PYTHON"
DB_PATH = "app_django/BDD.sqlite"
MAX_CAPITOLS = 10

PROMPT_BASE = """
Modifica el JSON tal que:
- solucio: sigui el camp en que es mostra la solució de l'execució del codi de l'exercici
- solucio_codi: sigui el camp en que es mostra el codi de l'exercici (i que executant hauria de donar la solució)
Important: solucio ha de ser el resultat de l'execució del codi de solucio_codi, no poden ser el mateix.
Contingut actual del capítol {capitol}:

{json_exercicis}

Retorna només el JSON revisat.
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

def descriu_taules(path: str) -> str:
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    descripcio = ""

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    taules = [row[0] for row in cursor.fetchall()]
    
    for taula in taules:
        cursor.execute(f"PRAGMA table_info({taula})")
        columnes = cursor.fetchall()
        descripcio += f"\nTaula '{taula}':\n"
        for col in columnes:
            descripcio += f" - {col[1]} ({col[2]})\n"
    
    conn.close()
    return descripcio

# ─── BUCLE DE CAPÍTOLS ────────────────────────────────────────────────
taules_info = descriu_taules(DB_PATH)

for CAPITOL in range(1, MAX_CAPITOLS + 1):
    print(f"\n>>> Revisant capítol {CAPITOL}...")

    nom_fitxer = os.path.join(DIRECTORI, f"{CURS}_capitol_{CAPITOL}.json")
    if not os.path.exists(nom_fitxer):
        print(f"Fitxer no trobat: {nom_fitxer}, el salto.")
        continue

    with open(nom_fitxer, "r", encoding="utf-8") as f:
        json_exercicis = f.read()

    prompt = PROMPT_BASE.format(
        capitol=CAPITOL,
        curs=CURS,
        descripcio_taules=taules_info,
        json_exercicis=json_exercicis
    )

    resposta = call_llm(prompt)

    try:
        json_net = bloc_json(resposta)
        dades = json.loads(json_net)
    except Exception as e:
        print(f"Error en recuperar JSON del capítol {CAPITOL}:", e)
        print("Resposta crua:")
        print(resposta)
        continue

    nom_sortida = os.path.join(DIRECTORI, f"{CURS}_capitol_{CAPITOL}.json")
    with open(nom_sortida, "w", encoding="utf-8") as f:
        json.dump(dades, f, ensure_ascii=False, indent=2)

    print(f"Capítol {CAPITOL} revisat i guardat com {nom_sortida}")