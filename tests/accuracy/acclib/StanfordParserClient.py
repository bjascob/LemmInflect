import  json
import  requests
import  logging


# Be sure to have the server running before instantiating this or it will
# raise an exception.
class StanfordParserClient(object):
    def __init__(self, port=5001):
        # Used by "requests" and prints lots of stuff that isn't useful
        logging.getLogger('urllib3').setLevel(logging.ERROR)
        self.server_url = 'http://localhost:%d' % (port)
        self.reqdict = {'annotators': 'lemma', 'outputFormat': 'json'}
        self._checkConnection()

    # Parse the text into a list of sentences
    def getParse(self, text):
        assert isinstance(text, str)
        snlp_ret  = self._annotate(text)
        if not snlp_ret or not snlp_ret.get('sentences', None):
            logging.warning('Empty return from server. text=%s' % text)
            return []
        if len(snlp_ret['sentences']) > 1:
            logging.warning('More than one sentence: in %s' % text)
        parsed = snlp_ret['sentences'][0]
        lemmas = [x['lemma'] for x in parsed['tokens']]
        if lemmas:
            return lemmas[0]
        else:
            return None

    # Perform a GET on the server which will get the main interface html page
    def _checkConnection(self):
        try:
            r = requests.get(self.server_url)
        except requests.exceptions.ConnectionError:
            raise Exception('Check whether you have started the CoreNLP server')

    # POST to the server to get the annotated data
    # Note that text needs to be a clean ascii string (not unicode)
    def _annotate(self, text):
        r = requests.post(self.server_url, params={'properties': str(self.reqdict)},
                          data=text.encode(), headers={'Connection': 'close'})
        r.raise_for_status()    # raise an excepection for a bad return        
        output = json.loads(r.text, strict=True)
        return output
