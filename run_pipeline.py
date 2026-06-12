import subprocess
import sys
from datetime import datetime

def run(script):
    print(f"\n{'='*40}")
    print(f"▶ Lancement : {script}")
    print(f"{'='*40}")
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        print(f"\n❌ Erreur dans {script} — pipeline arrêté")
        sys.exit(1)

if __name__ == "__main__":
    start = datetime.now()
    print(f"\n🚀 Pipeline démarré à {start.strftime('%H:%M:%S')}")

    run("scripts/extract.py")
    run("scripts/transform.py")
    run("scripts/load.py")

    end = datetime.now()
    duree = (end - start).seconds
    print(f"\n✅ Pipeline terminé en {duree} secondes !")
