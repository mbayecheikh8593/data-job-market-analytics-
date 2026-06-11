import os
import json
import glob
import pandas as pd
import re
from datetime import datetime

# ─── 1. Chargement des données brutes ───────────────────────────────────────
def load_raw(pattern="data/raw/adzuna_*.json"):
    files = sorted(glob.glob(pattern))
    if not files:
        raise FileNotFoundError("Aucun fichier raw trouvé")
    latest = files[-1]
    print(f"Fichier chargé : {latest}")
    with open(latest, encoding="utf-8") as f:
        return json.load(f)

# ─── 2. Normalisation des intitulés de poste ────────────────────────────────
TITRE_MAP = {
    "data engineer":       ["data engineer", "ingénieur data", "ingenieur data"],
    "data analyst":        ["data analyst", "analyste data", "analyste de données"],
    "data scientist":      ["data scientist", "scientifique des données"],
    "analytics engineer":  ["analytics engineer"],
    "bi developer":        ["bi developer", "business intelligence", "power bi", "tableau developer"],
    "ml engineer":         ["machine learning engineer", "ml engineer"],
}

def normalise_titre(titre):
    t = titre.lower()
    for cat, keywords in TITRE_MAP.items():
        if any(kw in t for kw in keywords):
            return cat
    return "other"

# ─── 3. Extraction des compétences ──────────────────────────────────────────
COMPETENCES = {
    "Langage":   ["python", "sql", "scala", "java", "r", "julia"],
    "Cloud":     ["aws", "gcp", "azure", "bigquery", "redshift", "snowflake"],
    "Big Data":  ["spark", "kafka", "hadoop", "hive", "flink"],
    "BI":        ["power bi", "tableau", "looker", "metabase", "qlik"],
    "Orches.":   ["airflow", "dbt", "prefect", "dagster", "luigi"],
    "DevOps":    ["docker", "kubernetes", "git", "github", "gitlab", "terraform"],
}

def extract_competences(description):
    if not description:
        return []
    desc = description.lower()
    found = []
    for categorie, skills in COMPETENCES.items():
        for skill in skills:
            pattern = r'\b' + re.escape(skill.strip()) + r'\b'
            if re.search(pattern, desc):
                found.append({"competence": skill.strip(), "categorie": categorie})
    return found

# ─── 4. Extraction ville / région ───────────────────────────────────────────
def extract_location(loc_field):
    if not loc_field:
        return None, None
    area = loc_field.get("area", [])
    ville  = area[-1] if len(area) >= 1 else None
    region = area[1]  if len(area) >= 2 else None
    return ville, region

# ─── 5. Pipeline principal ──────────────────────────────────────────────────
def transform(raw):
    rows = []
    competences_rows = []

    for job in raw:
        job_id  = f"adzuna_{job.get('id', '')}"
        titre   = job.get("title", "")
        company = job.get("company", {}).get("display_name", None)
        created = job.get("created", None)
        desc    = job.get("description", "")
        ville, region = extract_location(job.get("location"))

        rows.append({
            "job_id":           job_id,
            "titre_raw":        titre,
            "titre_normalise":  normalise_titre(titre),
            "entreprise":       company,
            "ville":            ville,
            "region":           region,
            "date_publication": created,
            "source":           "adzuna",
            "description":      desc,
        })

        for comp in extract_competences(desc):
            competences_rows.append({"job_id": job_id, **comp})

    df_jobs  = pd.DataFrame(rows)
    df_comps = pd.DataFrame(competences_rows)

    # Déduplication
    df_jobs = df_jobs.drop_duplicates(subset="job_id")

    # Format date
    df_jobs["date_publication"] = pd.to_datetime(df_jobs["date_publication"], errors="coerce")

    return df_jobs, df_comps

# ─── 6. Sauvegarde ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    raw = load_raw()
    df_jobs, df_comps = transform(raw)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs("data/silver", exist_ok=True)

    jobs_path  = f"data/silver/jobs_{ts}.csv"
    comps_path = f"data/silver/competences_{ts}.csv"

    df_jobs.to_csv(jobs_path,  index=False, encoding="utf-8")
    df_comps.to_csv(comps_path, index=False, encoding="utf-8")

    print(f"\n✓ {len(df_jobs)} offres transformées  → {jobs_path}")
    print(f"✓ {len(df_comps)} compétences extraites → {comps_path}")
    print(f"\nRépartition par métier :")
    print(df_jobs["titre_normalise"].value_counts().to_string())
    print(f"\nTop 10 compétences :")
    print(df_comps["competence"].value_counts().head(10).to_string())
