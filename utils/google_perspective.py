import json 
import logging

from googleapiclient import discovery

class perspective_client():
  def __init__(self, key):
    logging.info("setting up GOOGLE PERSPECTIVE API")
    self.pers_client = discovery.build(
          "commentanalyzer",
          "v1alpha1",
          developerKey=key,
          discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
          static_discovery=False,
        )
  def analyze_quote(self, text_to_analyze):
    logging.info(f"utils-perspective_client - analizing new quote :'{text_to_analyze}'")
    analyze_request = {
      'comment': { 'text':  text_to_analyze},
      'requestedAttributes': {'TOXICITY': {}}
    }

    response = self.pers_client.comments().analyze(body=analyze_request).execute()
    response = json.dumps(response, indent=2)
    response_to_dict = json.loads(response)
    toxicity = response_to_dict['attributeScores']['TOXICITY']['summaryScore']['value']
    return toxicity