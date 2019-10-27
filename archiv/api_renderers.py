from rest_framework import renderers


class ArchresTeiRenderer(renderers.BaseRenderer):
    media_type = "text/xml"
    format = "tei"

    def render(self, data, media_type=None, renderer_context=None):
        if 'results' in data.keys():
            print(data.keys())
            result = """<teiCorpus version="3.3.0" xmlns="http://www.tei-c.org/ns/1.0">"""
            for x in data['results']:
                result += x['tei_doc'].decode("utf-8")
            end = """</teiCorpus>"""
            result = result + end
        else:
            result = data['tei_doc']
        return result
