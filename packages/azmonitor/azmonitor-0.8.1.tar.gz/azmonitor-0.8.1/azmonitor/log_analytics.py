import json
import requests
import datetime
import hashlib
import hmac
import base64

class LogAnalytics:

    log_type = 'AzLogAnalytics'
    customer_id = ''
    shared_key = ''

    def __init__(self, log_type, customer_id, shared_key):
        """Log Analytics Class
        
        Arguments:
            log_type {str} -- he log type is the name of the event that is being submitted
            customer_id {str} -- Update the customer ID to your Log Analytics workspace ID
            shared_key {str} -- For the shared key, use either the primary or the secondary Connected Sources client authentication key
        """
        self.log_type = log_type
        self.customer_id = customer_id
        self.shared_key = shared_key

    def _build_signature(self, date, content_length, method, content_type, resource):
        x_headers = 'x-ms-date:' + date
        string_to_hash = method + "\n" + str(content_length) + "\n" + content_type + "\n" + x_headers + "\n" + resource
        bytes_to_hash = bytes(string_to_hash, encoding='utf-8')  
        decoded_key = base64.b64decode(self.shared_key)
        encoded_hash = base64.b64encode(hmac.new(decoded_key, bytes_to_hash, digestmod=hashlib.sha256).digest()).decode()
        authorization = "SharedKey {}:{}".format(self.customer_id,encoded_hash)
        return authorization

    def log(self, dict_data):
        """Build and send a request to the POST API
        
        Arguments:
            dict_data {dict} -- value dictionary
        """

        return(self.logs([dict_data]))

    def logs(self, list_dict_data):
        """Build and send a request to the POST API
        
        Arguments:
            list_dict_data {list} -- List of value dictionaries
        
        Returns:
            bool -- Response of Data Collector API
        """
        method = 'POST'
        content_type = 'application/json'
        resource = '/api/logs'
        result = False
        rfc1123date = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
        body = json.dumps(list_dict_data)
        content_length = len(body)
        signature = self._build_signature(rfc1123date, content_length, method, content_type, resource)
        uri = 'https://' + self.customer_id + '.ods.opinsights.azure.com' + resource + '?api-version=2016-04-01'
        headers = {
            'content-type': content_type,
            'Authorization': signature,
            'Log-Type': self.log_type,
            'x-ms-date': rfc1123date
        }
        response = requests.post(uri,data=body, headers=headers)
        if (response.status_code >= 200 and response.status_code <= 299):
            result = True
        return result
        