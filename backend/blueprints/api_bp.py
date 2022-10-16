from flask import Blueprint, jsonify, request, Response, stream_with_context
from jinja2 import TemplateNotFound
from api_lib import scraper
from api_lib.constants import SearchAlgorithmTypes
import requests

app = Blueprint('api_bp', __name__,
                        template_folder='../templates')

@app.route('/scrape/<term>')
def scrape(term):
    try:
        # Generator function
        def generate():
            url = request.args.get('url')
            for x in scraper.get_site(url, term, SearchAlgorithmTypes.BFS):
                yield str(x)
            
        # Run generator
        return stream_with_context(generate())
    
    # Catch exception
    except Exception as e:
        return jsonify(e)


@app.route('/api/google/<term>')
def api_google(term):
    url = "https://jobs.googleapis.com/v4/{parent=projects/*/tenants/*}/jobs:search"
    meta = {
        "allowMissingIds": True,
        "deviceInfo": {
            "deviceType": "BOT",
            "id": 123456
        }
    }
    body = {
        "searchMode": "JOB_SEARCH",
        "requestMetadata": meta,
        "jobQuery": {
            "query": term
        },
        "enableBroadening": False,
    }
    response = requests.request("POST", url, json=body)

    print(response.text)
    
    return response.text