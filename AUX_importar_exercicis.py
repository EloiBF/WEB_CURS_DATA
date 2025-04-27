import os
import json
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app_django.settings")  # Substitueix amb el nom correcte
django.setup()

from app_django.models import Curs, Capitol, Exercici  # Substitueix amb el nom real de la teva app

data_dir = os.path.join(os.path.dirname(__file__), 'data_exercicis')

def importar_exercicis_des_de_fitxer(path_fitxer):
    with open(path_fitxer, 'r', encoding='utf-8') as f:
        dades = json.load(f)

    # Creem o obtenim el curs
    curs_data = dades['curs']
    curs, _ = Curs.objects.get_or_create(nom=curs_data['nom'], defaults={
        "descripcio": curs_data['descripcio'],
        "color_fons": curs_data['color_fons'],
    })

    # Creem o obtenim el capítol
    capitol_data = dades['capitol']
    capitol, _ = Capitol.objects.get_or_create(
        curs=curs,
        numero=capitol_data['numero'],
        defaults={
            "titol": capitol_data['titol'],
            "dificultat": capitol_data['dificultat'],
            "preu": capitol_data['preu'],
        }
    )

    # Processar els exercicis
    for exercici_data in dades['exercicis']:
        # Comprovar si el número d'exercici està present
        if 'numero' not in exercici_data:
            print(f"❌ El camp 'numero' falta per a l'exercici: {exercici_data}")
            continue  # O també podries llançar un error si prefereixes que el procés es detingui

        # Assignar respostes_test i temps_estimat_minuts si existeixen al JSON
        pista_1 = exercici_data.pop("pista_1", "")
        pista_2 = exercici_data.pop("pista_2", "")
        respostes_test = exercici_data.pop("respostes_test", [])
        temps_estimat_minuts = exercici_data.pop("temps_estimat_minuts", None)
        
        # Afegir els camps al diccionari de dades de l'exercici
        exercici_data['respostes_test'] = respostes_test
        exercici_data['temps_estimat_minuts'] = temps_estimat_minuts
        exercici_data["pista_1"] = pista_1
        exercici_data["pista_2"] = pista_2

        
        # Assignar els valors de l'exercici amb seguretat per evitar errors amb camps nuls
        exercici_data = {k: v for k, v in exercici_data.items() if k in [field.name for field in Exercici._meta.fields]}

        # Crear o actualitzar l'exercici
        exercici, created = Exercici.objects.update_or_create(
            curs=curs,
            capitol=capitol,
            numero=exercici_data.get("numero"),  # Aquí es fa servir el 'numero'
            defaults=exercici_data,
        )

        # Mostrar el resultat
        print(f"{'✅ Creat' if created else '🔁 Actualitzat'}: Exercici {exercici.numero} - {exercici.titol or 'Sense títol'}")


if __name__ == '__main__':
    if not os.path.exists(data_dir):
        print(f"❌ No trobat el directori: {data_dir}")
        exit()

    fitxers = [f for f in os.listdir(data_dir) if f.endswith('.json')]
    if not fitxers:
        print("📭 No hi ha fitxers JSON a importar.")
        exit()

    for fitxer in fitxers:
        print(f"\n📥 Important fitxer: {fitxer}")
        try:
            importar_exercicis_des_de_fitxer(os.path.join(data_dir, fitxer))
        except Exception as e:
            print(f"⚠️ Error amb el fitxer {fitxer}: {e}")
