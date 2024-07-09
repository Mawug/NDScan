from http.server import SimpleHTTPRequestHandler, HTTPServer
import urllib.parse
import subprocess
import mysql.connector
import jinja2

PORT = 8000

db_config = {
    'user': 'root',
    'password': '',
    'host': '127.0.0.1',
    'database': 'vulnerability_analysis'
}

class MyHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/analyze':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            params = urllib.parse.parse_qs(post_data.decode('utf-8'))
            url = params.get('url')[0]

            # Assurez-vous que l'URL a un protocole
            if not url.startswith('http://') and not url.startswith('https://'):
                url = 'http://' + url
            
            # Exécutez le script d'analyse avec Nmap et ZAP
            subprocess.run(['python3', 'analyze.py', url])
            subprocess.run(['python3', 'analyze_zap.py', url])

            # Récupérer le rapport depuis la base de données
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute("SELECT report FROM analyses WHERE url = %s ORDER BY created_at DESC LIMIT 1", (url,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            
            report = result[0] if result else "Aucun rapport trouvé."
            
            # Générer la page de rapport
            template_loader = jinja2.FileSystemLoader(searchpath="./")
            template_env = jinja2.Environment(loader=template_loader)
            template = template_env.get_template("report.html")
            html_content = template.render(url=url, report=report)
            
            # Envoyer la réponse
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

httpd = HTTPServer(('localhost', PORT), MyHandler)
print(f"Serving on port {PORT}")
httpd.serve_forever()
