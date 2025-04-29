from django.shortcuts import render, get_object_or_404
from .models import Curs, Capitol, Exercici
import os
import groq
import re
from django.conf import settings
from dotenv import load_dotenv

# Carregar les variables d'entorn des del fitxer .env
load_dotenv()

# Connexió a la IA (Groq)
KEY = os.getenv("GROQ_API_KEY")
client = groq.Groq(api_key=KEY)

# Landing page general amb tots els cursos
def landing_page(request):
    cursos = Curs.objects.all().order_by('nom')
    return render(request, 'landing_page.html', {'cursos': cursos})


def index_curs(request, curs_nom):
    curs = get_object_or_404(Curs, nom=curs_nom)
    capitols = Capitol.objects.filter(curs=curs).order_by('numero').prefetch_related('exercicis')
    return render(request, 'index_curs.html', {'curs': curs, 'capitols': capitols})




def enviar_contacte(request):
    """Rep el formulari de contacte i retorna gràcies."""
    if request.method == 'POST':
        nom      = request.POST.get('nom')
        email    = request.POST.get('email')
        missatge = request.POST.get('missatge')

        # TODO: envia correu, desa a BD, etc.
        # Per ara, només mostrem un missatge flash
        messages.success(request, "Gràcies per contactar, %s! Et respondrem aviat." % nom)

        return redirect('landing_page')  # Torna a l’inici amb missatge
    # Si algú hi arriba amb GET, redirigeix
    return redirect('landing_page')



def correccio_test(resposta_usuari: str, solucio: str) -> tuple:
    def normalitza_text(text: str) -> str:
        return re.sub(r'\s+', ' ', text.strip().lower())
    resposta_normalitzada = normalitza_text(resposta_usuari)
    solucio_normalitzada = normalitza_text(solucio)

    if resposta_normalitzada == solucio_normalitzada:
        return True, "✅ Resposta correcta!"
    else:
        return False, "❌ Resposta incorrecta."

def correccio_codi(resposta_usuari: str, solucio: str) -> tuple:
    resposta_net = re.sub(r'\s+', '', resposta_usuari)
    solucio_net = re.sub(r'\s+', '', solucio)
    if resposta_net == solucio_net:
        return True, "Resposta correcta!"
    else:
        return False, "El codi no coincideix amb la solució esperada."


def correccio_exe(resposta_usuari: str, solucio: str, solucio_codi: str) -> tuple:
    import sys
    import io
    import traceback

    try:
        stdout_original = sys.stdout
        sys.stdout = io.StringIO()

        exec(resposta_usuari, {})

        resultat_obtingut = sys.stdout.getvalue().strip()
        sys.stdout = stdout_original

        if resultat_obtingut == solucio.strip():
            return True, "Resposta correcta!"
        else:
            return False, f"Resposta incorrecta. Esperat: {solucio!r}, Obtingut: {resultat_obtingut!r}."
    except Exception as e:
        sys.stdout = stdout_original
        return False, "Error d'execució. Revisa el teu codi."

def correccio_ia(resposta_usuari: str, solucio: str, enunciat: str = "", descripcio: str = "") -> tuple:
    prompt = f"""
Ets un professor que revisa una resposta d'un alumne. Avalua si la resposta és correcta, tenint en compte què demana l'exercici. 

🧠 CONTEXT DE L'EXERCICI:
Explicació acadèmica del tema: {descripcio}
Enunciat: {enunciat}

✅ RESPOSTA CORRECTA:
{solucio}

✍️ RESPOSTA DE L'ALUMNE:
{resposta_usuari}

Digues si la resposta és correcta o no, començant la teva resposta amb "SI" o "NO", i després explica el perquè en una frase clara i curta.
"""

    try:
        chat = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
        )
        resposta = chat.choices[0].message.content.strip()
        inici = resposta[:4].strip().lower()

        if inici.startswith("si"):
            return True, "Resposta correcta!", resposta
        elif inici.startswith("no"):
            return False, "Resposta incorrecta!", resposta
        else:
            return False, "Resposta incorrecta!", "Resposta de l'IA no reconeguda: " + resposta
    except Exception as e:
        return False, "No s'ha pogut generar la correcció amb IA.", f"Error: {e}"



def correccio_completar_codi(resposta_usuari, solucio_codi_1, solucio_codi_2=None):
    """
    Corregeix un exercici de completar codi, comparant el codi complet enviat per l'usuari amb les solucions possibles.
    """
    resposta_usuari_normalitzada = resposta_usuari.strip().replace(' ', '').replace('\n', '')
    solucio_codi_1_normalitzada = solucio_codi_1.strip().replace(' ', '').replace('\n', '')
    solucio_codi_2_normalitzada = solucio_codi_2.strip().replace(' ', '').replace('\n', '') if solucio_codi_2 else None

    if resposta_usuari_normalitzada == solucio_codi_1_normalitzada:
        return True, "✅ Codi correcte! Bona feina."
    elif solucio_codi_2_normalitzada and resposta_usuari_normalitzada == solucio_codi_2_normalitzada:
        return True, "✅ Codi correcte! Bona feina."
    else:
        return False, "❌ El codi no és correcte. Revisa la resposta."



def exercici(request, curs_nom, capitol_num, exercici_num):
    print(f"⚙️ Inici de la vista 'exercici' per al curs: {curs_nom}, capítol: {capitol_num}, exercici: {exercici_num}")

    # Recuperem el curs pel nom
    curs = get_object_or_404(Curs, nom=curs_nom)
    
    # Recuperem el capítol pel número
    capitol = get_object_or_404(Capitol, numero=capitol_num, curs=curs)
    
    # Recuperem l'exercici pel número dins del capítol
    exercici = get_object_or_404(Exercici, numero=exercici_num, capitol=capitol)

    missatge = ''
    resposta_correcta = False
    resposta_ia = ''

    if request.method == 'POST':
        tipus = exercici.tipus.lower().strip()

        if tipus == 'completar_codi':
            # Reconstruïm la resposta completa amb els inputs d'usuari
            respostes_usuari = request.POST.getlist('respostes_completar')
            print(f"📥 Respostes rebudes per completar_codi: {respostes_usuari}")
            if not respostes_usuari:
                resposta_usuari = ''
            else:
                codi_a_completar = exercici.codi_a_completar
                resposta_usuari = codi_a_completar
                for resposta in respostes_usuari:
                    resposta_usuari = resposta_usuari.replace('<placeholder>', resposta.strip(), 1)
        else:
            resposta_usuari = request.POST.get('resposta_usuari', '').strip()

        if not resposta_usuari:
            missatge = "Si us plau, escriu una resposta abans d'enviar-la ✏️"
        else:
            solucio = exercici.solucio.strip() if exercici.solucio else ''
            solucio_codi_1 = exercici.solucio_codi_1.strip() if exercici.solucio_codi_1 else ''
            solucio_codi_2 = exercici.solucio_codi_2.strip() if exercici.solucio_codi_2 else ''
            enunciat = exercici.enunciat
            descripcio = exercici.descripcio

            print(f"📨 Resposta rebuda: {resposta_usuari}")
            print(f"📘 Tipus d'exercici: {tipus}")
            print(f"📘 Solucio: {solucio}")
            print(f"📘 Solucio_codi_1: {solucio_codi_1}")
            print(f"📘 Solucio_codi_2: {solucio_codi_2}")

            if tipus == 'test':
                print("🔍 Cridant correcció per a TEST")
                resposta_correcta, missatge = correccio_test(resposta_usuari, solucio)

            elif tipus == 'codi':
                print("🔍 Cridant correcció per a CODI")
                if solucio_codi_1:
                    resposta_correcta, missatge = correccio_codi(resposta_usuari, solucio_codi_1)
                elif solucio_codi_2:
                    resposta_correcta, missatge = correccio_codi(resposta_usuari, solucio_codi_2)
                else:
                    resposta_correcta = False
                    missatge = "No s'ha trobat cap solució vàlida per al codi."

            elif tipus == 'exe':
                print("🔍 Cridant correcció per a EXE amb execució i output")
                print(f"📤 Resultat esperat: {solucio}")
                resposta_correcta, missatge = correccio_exe(resposta_usuari, solucio, solucio_codi_1)

            elif tipus == 'ia':
                print("🤖 Cridant correcció per a IA")
                resposta_correcta, missatge, resposta_ia = correccio_ia(resposta_usuari, solucio, enunciat, descripcio)

            elif tipus == 'completar_codi':
                print("🧩 Cridant correcció per a COMPLETAR_CODI")
                resposta_correcta, missatge = correccio_completar_codi(
                    resposta_usuari,
                    solucio_codi_1,
                    solucio_codi_2
                )

            else:
                print(f"⚠️ Tipus d'exercici no reconegut: {tipus}")

    # Obtenir els exercicis següents i anteriors pel seu número dins del mateix capítol
    exercici_seguent = Exercici.objects.filter(capitol=capitol, numero=exercici.numero + 1).first()
    exercici_anterior = Exercici.objects.filter(capitol=capitol, numero=exercici.numero - 1).first()

    # Preparar codi amb placeholders substituïts per inputs si és completar_codi
    def reemplaçar_placeholders(codi):
        count = 0
        def replacer(match):
            nonlocal count
            count += 1
            return f'<input type="text" name="respostes_completar" class="placeholder-input" data-index="{count}">'
        return re.sub(r'<placeholder>', replacer, codi)

    if exercici.tipus.lower().strip() == 'completar_codi' and exercici.codi_a_completar:
        codi_a_completar_html = reemplaçar_placeholders(exercici.codi_a_completar)
    else:
        codi_a_completar_html = ''

    return render(request, 'exercici.html', {
        'curs': curs,
        'capitol': capitol,
        'exercici': exercici,
        'missatge': missatge,
        'opcions': exercici.respostes_test if exercici.tipus == 'test' else None,
        'exercici_seguent': exercici_seguent,
        'exercici_anterior': exercici_anterior,
        'resposta_correcta': resposta_correcta,
        'codi_a_completar_html': codi_a_completar_html,
        'resposta_ia': resposta_ia,
    })
