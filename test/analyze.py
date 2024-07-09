import mysql.connector
import subprocess
import sys

# Configuration de la base de données
db_config = {
    'user': 'root',  # Le nom d'utilisateur par défaut est 'root'
    'password': '',  # Par défaut, il n'y a pas de mot de passe pour l'utilisateur 'root'
    'host': '127.0.0.1',
    'database': 'vulnerability_analysis'
}

def run_nmap(url):
    try:
        # Utilisation de subprocess pour exécuter Nmap et récupérer les résultats
        result = subprocess.check_output(['nmap', '-A', url], stderr=subprocess.STDOUT)
        return result.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return f"Erreur d'exécution de Nmap : {e.output.decode('utf-8')}"

def save_report(url, report):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO analyses (url, report) VALUES (%s, %s)", (url, report))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Rapport pour {url} enregistré avec succès.")
    except mysql.connector.Error as err:
        print(f"Erreur : {err}")

def get_report(url):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT report FROM analyses WHERE url = %s ORDER BY created_at DESC LIMIT 1", (url,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result[0] if result else "Aucun rapport trouvé."
    except mysql.connector.Error as err:
        print(f"Erreur : {err}")
        return None

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python analyze.py <url>")
        sys.exit(1)
    
    url = sys.argv[1]
    report = run_nmap(url)
    save_report(url, report)
    print(f"Rapport pour {url} : \n{report}")
