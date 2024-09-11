from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)

@app.route("/contact/")
def MaPremiereAPI():
    return render_template("contact.html")

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def monhistogramme():
    return render_template("histogramme.html")

@app.route('/commits/')
def display_commits():
    # Affiche la page HTML qui contient le graphique
    return render_template('commits.html')  # Assurez-vous que ce fichier est dans le dossier 'templates'

@app.route('/commits-data')
def get_commit_data():
    # URL de l'API GitHub pour récupérer les commits
    api_url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'

    try:
        # Effectue une requête GET pour récupérer les données de l'API
        response = requests.get(api_url)
        response.raise_for_status()  # Vérifie si la requête a réussi

        # Transforme les données en format JSON
        commits = response.json()
        # Extraire les minutes de chaque commit
        minutes_list = [extract_minutes(commit['commit']['author']['date']) for commit in commits]

        # Compte le nombre de commits pour chaque minute de 0 à 59
        minute_counts = {minute: minutes_list.count(minute) for minute in range(60)}

        # Retourne les données sous format JSON pour être utilisé par le graphique
        return jsonify(minute_counts)
    except requests.exceptions.RequestException as e:
        # Gestion des erreurs de la requête
        return jsonify({'error': str(e)}), 500

def extract_minutes(date_string):
    """
    Extrait les minutes d'une date au format ISO : '2024-02-11T11:57:27Z'
    """
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    return date_object.minute
  
@app.route('/')
def hello_world():
    return render_template('hello.html') #comm
  
if __name__ == "__main__":
  app.run(debug=True)
  
