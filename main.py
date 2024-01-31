import os
from flask import Flask
from prometheus_client import Gauge, generate_latest, CollectorRegistry, CONTENT_TYPE_LATEST

app = Flask(__name__)
registry = CollectorRegistry()

fileCount = Gauge('file_count', 'Número total de arquivos no diretório', registry=registry)

# Diretório que deseja monitorar
directoryMonitor = '/Users/Username/Documents/'

def countFiles(directory):
    count = 0
    for _, dirs, files in os.walk(directory):
        count += len(files)
    return int(count)

@app.route('/metrics')
def metrics():
    currentCount = countFiles(directoryMonitor)
    fileCount.set(currentCount)
    return generate_latest(registry), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.run(debug=True, port=8000)
