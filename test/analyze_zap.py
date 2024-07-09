import time
import mysql.connector
from zapv2 import ZAPv2

# Configuration de la base de données
db_config = {
    'user': 'root',
    'password': '',
    'host': '127.0.0.1',
    'database': 'vulnerability_analysis'
}

# Configuration de ZAP
ZAP_API_KEY = 'rlminssppe06h577ks4m2c460k'  # Assurez-vous que la clé API est correcte
zap = ZAPv2(apikey=ZAP_API_KEY)

def run_zap_scan(url):
    zap.urlopen(url)
    time.sleep(2)  # Attendez que l'URL s'ouvre
    
    print(f"Début de l'analyse active pour {url}")
    scanid = zap.ascan.scan(url)
    
    while int(zap.ascan.status(scanid)) < 100:
        print(f"Progrès : {zap.ascan.status(scanid)}%")
        time.sleep(5)
    
    print(f"Analyse terminée pour {url}")
    report = zap.core.htmlreport()
    return report

def save_zap_result(url, report):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO owasp_results (url, result) VALUES (%s, %s)", (url, report))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Rapport pour {url} enregistré avec succès dans la table 'owasp_results'.")
    except mysql.connector.Error as err:
        print(f"Erreur MySQL : {err}")
    except Exception as ex:
        print(f"Erreur inattendue : {ex}")

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: python analyze_zap.py <url>")
        sys.exit(1)
    
    url = sys.argv[1]
    report = run_zap_scan(url)
    save_zap_result(url, report)
    print(f"Rapport pour {url} avec OWASP ZAP : \n{report}")
