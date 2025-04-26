import os, json, groq

# ─── PARÀMETRES BÀSICS ────────────────────────────────────────────────
DIRECTORI = "data_exercicis"
os.makedirs(DIRECTORI, exist_ok=True)

CURSOS = ["PYTHON"]          # ← afegeix o treu cursos


MAX_CAPITOLS = 10                            # volem 10 per curs
PROMPT_BASE = """Ets un professor… (mateix text llarg que ja tens)"""

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

def desa(cap: str, raw: str):
    path = os.path.join(DIRECTORI, cap)
    try:
        data = json.loads(bloc_json(raw))
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✅ {path}")
    except Exception as e:
        print(f"⚠️  Error desant {cap}: {e}")

def context_curs(curs: str) -> str:
    caps = [
        json.load(open(os.path.join(DIRECTORI, f), encoding="utf-8"))
        for f in os.listdir(DIRECTORI)
        if f.startswith(f"{curs}_") and f.endswith(".json")
    ]
    caps.sort(key=lambda c: c["capitol"]["numero"])
    return json.dumps(caps, ensure_ascii=False)

def capítols_existents(curs: str) -> int:
    return sum(1 for f in os.listdir(DIRECTORI) if f.startswith(f"{curs}_") and f.endswith(".json"))




context_estructura = r"""
  {
    "curs": {
      "nom": "SQL",                       // Nom del curs (sempre el mateix per a tots els capítols d’aquest curs)
      "descripcio": "Aprèn SQL des de zero i domina les consultes de dades com un professional.",
      "color_fons": "#F4F8F4"             // Color hexadecimal opcional
    },
  
    "capitol": {
      "titol": "Introducció a SQL i SELECT bàsic", // Títol del capítol (decidit per l’IA)
      "numero": 1,                                 // Número de capítol (incremental)
      "dificultat": "Fàcil",                       // Fàcil / Mitjà / Avançat…
      "preu": 0.00                                 // 0.00 si és gratuït, altrament preu en euros
    },
  
    "exercicis": [
      {
        "numero": 1,                    // Número dins del capítol (1‑5)
        "titol": "Consulta bàsica amb SELECT",
        "tipus": "codi",                // "codi" o "test"
        "descripcio": "Explicació acadèmica del concepte: què és SELECT *, quan s’usa, bones pràctiques…",
        "enunciat": "Escriu una consulta SQL per seleccionar totes les columnes de la taula `clients`.",
        "solucio": "SELECT * FROM clients;",      // Codi o resposta correcta
        "temps_estimat_minuts": 3,
  
        // Per exercicis tipus test:
        "respostes_test": [],           // [] per “codi”; [] amb 4 opcions per “test”
  
        // Pistes (opcionals però recomanades)
        "pista_1": "Utilitza l’asterisc (*) per seleccionar totes les columnes.",
        "pista_2": "No oblidis el punt i coma al final de la consulta.",
  
        // Camps d’imatges (habitualment null si no calen)
        "imatge_1": null,
        "descripcio_imatge_1": null,
        "imatge_2": null,
        "descripcio_imatge_2": null
      },
  
      // …exercicis 2, 3, 4, 5 (mateixa estructura) …
    ]
  }
"""



instruccions_addicionals = "El curs de Python s'ha d'enfocar a analistes de dades i científics de dades. Ha de començar amb una introducció a Python i després passar a pandas, scikit-learn. Ensenyar també les clases, funcions i estructures de dades bàsiques de Python. Els ultims cursos han de ser molt enfocats a data analytics i machine learning, i proposar preguntes sobre plantejaments reals de data analytics."







# ─── BUCLE PRINCIPAL ─────────────────────────────────────────────────
for curs in CURSOS:
    while (n := capítols_existents(curs)) < MAX_CAPITOLS:
        num_nou = n + 1
        frase = (
            f"Els capítols existents són:\n{context_curs(curs)}\n\n"
            f"Genera el JSON per al capítol {num_nou} del curs {curs}. "
            f"Ha de contenir EXACTAMENT 5 exercicis i seguir l'esquema indicat. Generalment els exercicis són de tipus 'codi' però pot haver-ne un de tipus 'test' sobretot per fer referència a funcionalitats de programes que no són codi directament, o a preguntes teòriques. Intenta variar entre codi i test.\n"
            f"Els JSON han de tenir aquesta estructura exacta: {context_estructura}\n"
            f"Escull tu mateix un títol apropiat pel capítol {num_nou}.\n"
            f"Instruccions addicionals: {instruccions_addicionals}"
                        
        )
        resposta = call_llm(PROMPT_BASE + frase)
        nom_fitxer = f"{curs}_capitol_{num_nou}.json"
        desa(nom_fitxer, resposta)

print("🎉 Ja tens 10 capítols per a cada curs!")
