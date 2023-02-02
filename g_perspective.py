## google perspective 
from googleapiclient import discovery
import json
import os 
from dotenv import load_dotenv
load_dotenv()
PERSPECTIVE_API = os.environ['G_PER_TOKEN']

class perspective_client():
  def __init__(self, key):
    self.pers_client = discovery.build(
          "commentanalyzer",
          "v1alpha1",
          developerKey=key,
          discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
          static_discovery=False,
        )
  def analyze_quote(self, text_to_analyze):
    analyze_request = {
      'comment': { 'text':  text_to_analyze},
      'requestedAttributes': {'TOXICITY': {}}
    }

    response = self.pers_client.comments().analyze(body=analyze_request).execute()
    response = json.dumps(response, indent=2)
    response_to_dict = json.loads(response)
    toxicity = response_to_dict['attributeScores']['TOXICITY']['summaryScore']['value']
    return toxicity
