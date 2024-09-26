import json
import utils

def lambda_handler(event, context):
    # O Intent "CommitDiario" foi ativado, agora realizar o commit no repositorio
    try:
        utils.commit_to_github()
        
        # Resposta para a Alexa
        return {
            'version': '1.0',
            'response': {
                'outputSpeech': {
                    'type': 'PlainText',
                    'text': 'Feito.'
                },
                'shouldEndSession': True
            }
        }

    except Exception as e:
        return {
            'version': '1.0',
            'response': {
                'outputSpeech': {
                    'type': 'PlainText',
                    'text': f"Falha ao realizar o commit: {str(e)}"
                },
                'shouldEndSession': True
            }
        }
