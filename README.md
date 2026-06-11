# 📊 Data Job Market Analytics

Pipeline ETL complet d'analyse du marché de l'emploi Data en France.

## 🎯 Objectif

Collecter automatiquement des offres d'emploi Data via l'API Adzuna,
les transformer et les charger dans PostgreSQL pour produire des insights
sur les métiers, compétences et régions qui recrutent le plus.

## 🏗️ Architecturede
API Adzuna → extract.py → data/raw/ → transform.py → data/silver/ → load.py → PostgreSQL
## 📈 Résultats

### Répartition par métier
| Métier | Offres |
|---|---|
| Data Engineer | 154 |
| Data Scientist | 147 |
| Data Analyst | 145 |

### Top 5 compétences
| Compétence | Catégorie | Offres |
|---|---|---|
| Power BI | BI | 32 |
| Python | Langage | 30 |
| SQL | Langage | 30 |
| Azure | Cloud | 22 |
| Spark | Big Data | 18 |

### Top régions
| Région | Offres |
|---|---|
| Île-de-France | 220 |
| Auvergne-Rhône-Alpes | 36 |
| Nouvelle-Aquitaine | 27 |

### Top entreprises recruteuses
| Entreprise | Offres |
|---|---|
| Collective.work | 20 |
| Kaino | 13 |
| MBDA | 7 |
| Capgemini | 5 |

##  Stack technique

- **Python** — extraction et transformation
- **Pandas** — nettoyage des données
- **PostgreSQL** — stockage et analyse
- **Docker** — base de données en local
- **API Adzuna** — source des offres d'emploi

## 🚀 Lancer le projet

### 1. Cloner le repo
```bash
git clone https://github.com/mbayecheikh8593/data-job-market-analytics.git
cd data-job-market-analytics
```

### 2. Installer les dépendances
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Configurer les variables d'environnement
```bash
cp .env.example .env
# Remplir ADZUNA_APP_ID et ADZUNA_API_KEY
```

### 4. Lancer PostgreSQL
```bash
cd docker && docker compose up -d && cd ..
```

### 5. Lancer le pipeline ETL
```bash
python scripts/extract.py
python scripts/transform.py
python scripts/load.py
```

## 📁 Structure du projet