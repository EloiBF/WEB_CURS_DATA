import os, json, time
import groq

# ─── PARÀMETRES ───────────────────────────────────────────────────────
DIRECTORI = "data_exercicis"
CURS = "SQL"  # O el que vulguis: PYTHON, SQL, DAX...
MAX_CAPITOLS = 10

PROMPT_BASE_OLD = """
Ets un professor expert en Data. 
El teu objectiu és crear capítols amb EXACTAMENT 5 exercicis cadascun del curs {curs}, utilitzant codi i fórmules reals.

IMPORTANT:
- Inclou tots els camps del JSON, si cal deixa'ls en null, no en pot faltar cap. Els noms dels camps han de ser exactament els mateixos que els del JSON, no canviis cap ni canviis l'idioma.
- No afegeixis camps diferents al JSON.
- La resposta ha de ser només el JSON en format diccionari, sense comentaris abans ni després, per evitar errors en el procés automatitzat.

Els exercicis poden ser de 4 tipus:
- "codi": programació curta (1-5 línies).
- "test": preguntes tipus test amb 4 opcions (indicant la correcta).
- "exe": completar o corregir fragments de codi (només per Python).
- "IA": exercicis complexos amb respostes llargues o obertes corregides per un LLM.

Instruccions importants:
- Tots els exercicis han de ser resolts amb les dades generades, sense referències externes.
- No cal usar eines externes com Excel.
- Fes els enunciats clars, adaptats al nivell indicat (Fàcil, Mitjà, Avançat).
- Per "test", afegeix 4 opcions amb la correcta.
- Per "IA", proposa casos pràctics o anàlisis de casos.
- Segueix estrictament l'estructura JSON proporcionada.
- El camp descripció és fonamental per l'explicació pedagògica.
"""

PROMPT_BASE = """
Et comparteixo un JSON amb exercicis del curs {curs}. No modifiquis l'estructura ni els exercicis, només has de fer petits canvis:
Ajusta el camp solucio_codi del JSON tal que: solucio_codi_1 tingui el valor actual de solucio_codi i solucio_codi_2 sigui null.
També assegura't que el camp descripcio sigui clar i útil per a l'alumne, tai i com es defineix a l'exemple de context.

IMPORTANT:
- Inclou tots els camps del JSON, si cal deixa'ls en null, no en pot faltar cap. Els noms dels camps han de ser exactament els mateixos que els del JSON, no canviis cap ni canviis l'idioma.
- No afegeixis camps diferents al JSON.
- La resposta ha de ser només el JSON en format diccionari, sense comentaris abans ni després, per evitar errors en el procés automatitzat.
"""

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
      "solucio": "Resposta correcta a l'exercici, en cas que sigui tipus 'exe' serà el resultat esperat del codi",
      "solucio_codi_1": "Codi de la solució, en tipus test serà null i en tipus codi i exe serà el codi de la solució. En cas d'excel, la solució en anglès, en altres cursos serà null",
      "solucio_codi_2": "En cas d'excel, la solució en castellà, en altres cursos serà null",
      "solucio_codi_2":null,
      "codi_a_completar":null,
      "temps_estimat_minuts": 5,
      "respostes_test": [],
      "pista_1": "Primera pista. (Una frase)",
      "pista_2": "Segona pista. (Una frase)",
      "imatge_1": null,
      "descripcio_imatge_1": null,
      "imatge_2": null,
      "descripcio_imatge_2": null
    }
  ]
}
"""

# ─── GROQ ─────────────────────────────────────────────────────────────
KEY = os.getenv("GROQ_API_KEY")
client = groq.Groq(api_key=KEY)

def call_llm(prompt: str) -> str:
    try:
        chat = client.chat.completions.create(
            #model="llama-3.3-70b-versatile",
            model="deepseek-r1-distill-llama-70b",
            messages=[{"role": "user", "content": prompt}],
        )
        print( chat.choices[0].message.content.strip())
        return chat.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ Error cridant a l'API: {e}")
        raise SystemExit("Aturant execució per error greu.")

# ─── HELPERS ──────────────────────────────────────────────────────────
def bloc_json(text: str) -> str:
    i, j = text.find("{"), text.rfind("}")
    if i == -1 or j == -1 or j <= i:
        raise ValueError("Cap JSON trobat o mal format")
    return text[i:j+1]

# ─── BUCLE PRINCIPAL ──────────────────────────────────────────────────
for cap in range(1, MAX_CAPITOLS + 1):
    print(f"\n>>> Revisant capítol {cap}...")

    fitxer_path = os.path.join(DIRECTORI, f"{CURS}_capitol_{cap}.json")
    if not os.path.exists(fitxer_path):
        print(f"Fitxer no trobat: {fitxer_path}, saltant...")
        continue

    with open(fitxer_path, "r", encoding="utf-8") as f:
        json_exercicis = f.read()

    prompt = PROMPT_BASE.format(curs=CURS, json_exercicis=json_exercicis)

    intents = 0
    max_intents = 30
    mentre_no_aconseguit = True

    while mentre_no_aconseguit and intents < max_intents:
        intents += 1
        try:
            resposta = call_llm(prompt)
            json_net = bloc_json(resposta)
            dades = json.loads(json_net)

            # Guardar correcció
            with open(fitxer_path, "w", encoding="utf-8") as f:
                json.dump(dades, f, indent=2, ensure_ascii=False)

            print(f"✅ Capítol {cap} revisat i corregit.")
            mentre_no_aconseguit = False

        except (ValueError, json.JSONDecodeError) as e:
            print(f"⚠️ Error processant JSON del capítol {cap}: {e}")
            if intents < max_intents:
                print("🔄 Reintentant en 2 segons...")
                time.sleep(2)
            else:
                print(f"❌ Error definitiu al capítol {cap} després de {max_intents} intents.")
                raise SystemExit(f"Aturant execució per error a capítol {cap}.")

print("\n🎯 Tots els capítols han estat revisats i corregits correctament!")
