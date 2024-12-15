from rest_framework import renderers
import json

class UserRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = {}
        
        if 'ErrorDetail' in str(data) or isinstance(data, dict) and 'errors' in data:
            response['status'] = 'failure'
            if 'errors' in data:
                response['errors'] = data['errors']
            elif 'non_field_errors' in data:
                response['errors'] = data['non_field_errors']
            else:
               response['errors'] = data

        else:
            response['status'] = 'success'
            response['data'] = data
        
        return json.dumps(response)
