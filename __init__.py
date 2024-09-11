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
    # Afficher la page HTML qui contient le graphique
    return render_template('commits.html')  # Assurez-vous d'avoir un fichier `commits.html` dans le dossier `templates`

@app.route('/commits-data')
def get_commit_data():
    # URL de l'API pour récupérer les commits du repository
    api_url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Vérifie si la requête a réussi

        commits = response.json()
        # Extraire les minutes de chaque commit
        minutes_list = [extract_minutes(commit['commit']['author']['date']) for commit in commits]

        # Compter les occurrences de chaque minute
        minute_counts = {minute: minutes_list.count(minute) for minute in range(60)}

        return jsonify(minute_counts)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

def extract_minutes(date_string):
    """
    Extrait les minutes d'une date au format ISO.
    """
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    return date_object.minute
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html') #comm2
  
if __name__ == "__main__":
  app.run(debug=True)
  
