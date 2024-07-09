import mysql.connector
import subprocess
import sys

# Configuration de la base de données
db_config = {
    'user': 'root',
    'password': '',
    'host': '127.0.0.1',
    'database': 'vulnerability_analysis'
}

def run_nmap(url):
    try:
        result = subprocess.check_output(['nmap', '-A', url], stderr=subprocess.STDOUT)
        return result.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return f"Erreur d'exécution de Nmap : {e.output.decode('utf-8')}"

def save_nmap_result(url, result):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO nmap_results (url, result) VALUES (%s, %s)", (url, result))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Rapport pour {url} enregistré avec succès dans la table 'nmap_results'.")
    except mysql.connector.Error as err:
        print(f"Erreur MySQL : {err}")
    except Exception as ex:
        print(f"Erreur inattendue : {ex}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python analyze.py <url>")
        sys.exit(1)
    
    url = sys.argv[1]
    result = run_nmap(url)
    save_nmap_result(url, result)
    print(f"Rapport pour {url} avec Nmap : \n{result}")
