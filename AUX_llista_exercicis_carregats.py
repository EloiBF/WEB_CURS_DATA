import sqlite3

# Connecta't a la base de dades
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Consulta per obtenir els capítols
cursor.execute('''
    SELECT id, numero, titol
    FROM app_django_capitol
    ORDER BY numero
''')
capitols = cursor.fetchall()

for capitol in capitols:
    capitol_id, numero, titol = capitol
    print(f"Capítol {numero}: {titol}")

    # Consulta els exercicis d'aquest capítol
    cursor.execute('''
        SELECT numero, titol
        FROM app_django_exercici
        WHERE capitol_id = ?
        ORDER BY numero
    ''', (capitol_id,))
    exercicis = cursor.fetchall()

    if exercicis:
        for exercici in exercicis:
            num_exercici, titol_exercici = exercici
            print(f"   - Exercici {num_exercici}: {titol_exercici or 'Sense títol'}")
    else:
        print("   (Aquest capítol encara no té exercicis)")

    print('-' * 40)

# Tanca la connexió
conn.close()
