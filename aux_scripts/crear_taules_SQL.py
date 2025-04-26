import sqlite3

conn = sqlite3.connect("app_django/BDD.sqlite")
cur = conn.cursor()

# ─── DROP TAULES SI EXISTEIXEN ───────────────────────────────────────
taules = ["detalls_comanda", "comandes", "clients", "productes", "empleats"]
for t in taules:
    cur.execute(f"DROP TABLE IF EXISTS {t}")

# ─── CREACIÓ DE TAULES ────────────────────────────────────────────────
cur.execute("""
CREATE TABLE clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT,
    ciutat TEXT,
    pais TEXT
)
""")

cur.execute("""
CREATE TABLE empleats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT,
    carrec TEXT,
    oficina TEXT
)
""")

cur.execute("""
CREATE TABLE productes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT,
    categoria TEXT,
    preu REAL
)
""")

cur.execute("""
CREATE TABLE comandes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER,
    empleat_id INTEGER,
    data_comanda TEXT,
    FOREIGN KEY (client_id) REFERENCES clients(id),
    FOREIGN KEY (empleat_id) REFERENCES empleats(id)
)
""")

cur.execute("""
CREATE TABLE detalls_comanda (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    comanda_id INTEGER,
    producte_id INTEGER,
    quantitat INTEGER,
    descompte REAL DEFAULT 0,
    FOREIGN KEY (comanda_id) REFERENCES comandes(id),
    FOREIGN KEY (producte_id) REFERENCES productes(id)
)
""")

# ─── INSERCIÓ DE DADES DE PROVA ───────────────────────────────────────
cur.executescript("""
INSERT INTO clients (nom, ciutat, pais) VALUES
('Anna Puig', 'Barcelona', 'Espanya'),
('Joan Roca', 'Girona', 'Espanya'),
('Laura Soler', 'València', 'Espanya');

INSERT INTO empleats (nom, carrec, oficina) VALUES
('Marta Serra', 'Comercial', 'BCN'),
('Pau Casals', 'Comercial', 'VAL');

INSERT INTO productes (nom, categoria, preu) VALUES
('Portàtil X1', 'Electrònica', 1200),
('Smartphone Z3', 'Electrònica', 800),
('Tauleta T8', 'Electrònica', 450),
('Cadira ergonòmica', 'Mobles', 150);

INSERT INTO comandes (client_id, empleat_id, data_comanda) VALUES
(1, 1, '2024-04-01'),
(2, 1, '2024-04-03'),
(3, 2, '2024-04-10');

INSERT INTO detalls_comanda (comanda_id, producte_id, quantitat, descompte) VALUES
(1, 1, 1, 0),
(1, 4, 2, 0.1),
(2, 2, 1, 0.05),
(3, 3, 3, 0);
""")

conn.commit()
conn.close()

print("Base de dades creada amb èxit.")