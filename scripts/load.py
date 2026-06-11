import os
import glob
import pandas as pd
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", 5432),
        dbname=os.getenv("POSTGRES_DB", "datajobs"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "postgres")
    )

def load_latest_csv(pattern):
    files = sorted(glob.glob(pattern))
    if not files:
        raise FileNotFoundError(f"Aucun fichier trouvé : {pattern}")
    return pd.read_csv(files[-1])

def load_emplois(conn, df):
    cursor = conn.cursor()
    count = 0
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO emplois (job_id, titre_raw, titre_normalise, entreprise, ville, region, date_publication, source)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (job_id) DO NOTHING
        """, (
            row["job_id"],
            row["titre_raw"],
            row["titre_normalise"],
            row["entreprise"],
            row["ville"],
            row["region"],
            row["date_publication"] if pd.notna(row["date_publication"]) else None,
            row["source"]
        ))
        count += cursor.rowcount
    conn.commit()
    cursor.close()
    print(f"✓ {count} offres insérées dans emplois")

def load_competences(conn, df):
    cursor = conn.cursor()
    count = 0
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO competences (job_id, competence, categorie)
            VALUES (%s, %s, %s)
        """, (row["job_id"], row["competence"], row["categorie"]))
        count += cursor.rowcount
    conn.commit()
    cursor.close()
    print(f"✓ {count} compétences insérées dans competences")

if __name__ == "__main__":
    print("Connexion à PostgreSQL...")
    conn = get_connection()
    print("Connecté !\n")

    df_jobs  = load_latest_csv("data/silver/jobs_*.csv")
    df_comps = load_latest_csv("data/silver/competences_*.csv")

    load_emplois(conn, df_jobs)
    load_competences(conn, df_comps)

    conn.close()
    print("\n✓ Pipeline terminé !")
