import os, json, groq

# ─── PARÀMETRES BÀSICS ────────────────────────────────────────────────
DIRECTORI = "data_exercicis"
os.makedirs(DIRECTORI, exist_ok=True)

CURS = "PYTHON_MACHINE_LEARNING"

CAPITOLS = [
    {
        "numero": 1,
        "titol": "Introducció a Machine Learning i Scikit-learn",
        "dificultat": "Fàcil",
        "temes": [
            "Què és el Machine Learning?",
            "Tipus de problemes: supervisat vs no supervisat",
            "Pipeline bàsic amb Scikit-learn",
            "Divisió de dades amb train_test_split"
        ]
    },
    {
        "numero": 2,
        "titol": "Regressió lineal i mètriques de regressió",
        "dificultat": "Mitjà",
        "temes": [
            "Entrenar un model de regressió lineal amb sklearn",
            "Interpretar coeficients i intercept",
            "Mètriques de regressió: MAE, MSE, RMSE, R²",
            "Visualització de resultats amb Matplotlib/Seaborn"
        ]
    },
    {
        "numero": 3,
        "titol": "Classificació binària amb Logistic Regression",
        "dificultat": "Mitjà",
        "temes": [
            "Problemes de classificació binària",
            "LogisticRegression a sklearn",
            "Mètriques de classificació: accuracy, precision, recall, f1",
            "Matriu de confusió i classificació de probabilitats"
        ]
    },
    {
        "numero": 4,
        "titol": "Models basats en arbres: Decision Trees i Random Forest",
        "dificultat": "Avançat",
        "temes": [
            "DecisionTreeClassifier i DecisionTreeRegressor",
            "Overfitting i control de profunditat (max_depth, min_samples)",
            "RandomForest per millorar generalització",
            "Importància de variables"
        ]
    },
    {
        "numero": 5,
        "titol": "Classificació amb K-Nearest Neighbors (KNN)",
        "dificultat": "Mitjà",
        "temes": [
            "Com funciona el KNN",
            "Normalització de dades (StandardScaler)",
            "Entrenament i predicció amb KNeighborsClassifier",
            "Elecció òptima de K i corbes d'error"
        ]
    },
    {
        "numero": 6,
        "titol": "Clustering amb K-Means i t-SNE",
        "dificultat": "Avançat",
        "temes": [
            "Clustering no supervisat: KMeans",
            "Detecció del nombre òptim de clústers (elbow method)",
            "Visualització 2D amb t-SNE",
            "Interpretació pràctica dels resultats"
        ]
    },
    {
        "numero": 7,
        "titol": "Selecció de models i validació creuada",
        "dificultat": "Avançat",
        "temes": [
            "Cross-validation amb cross_val_score",
            "GridSearchCV per optimització d’hiperparàmetres",
            "Comparar models amb mètriques comunes",
            "Pipeline amb transformadors + model final"
        ]
    }
]



PROMPT_BASE = """
Ets un professor expert en Data Analytics. 
El teu objectiu és crear capítols d'un curs pràctic amb EXACTAMENT 5 exercicis cadascun. Exercicis reals que utilitzin codi i fórmules 100% reals, no inventades.

Els exercicis poden ser de 4 tipus:
- "codi": exercicis pràctics de programació curta (només per cursos de SQL, Excel o DAX).
- "completar_codi": exercicis en que es dóna una part del codi i es demana completar-lo o afegir les parts que hi falten
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
    "nom": "Python",
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
      "codi_a_completar": codi a completar, s'afegeix el parametre "<placeholder>" per les parts que s'hagin de completar. Per exemple: x + <placeholder> = 5, 
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
