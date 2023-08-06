from sense_text_extractor import text_extract_pb2, text_extract_pb2_grpc
import grpc
import sense_core as sd


# python -m grpc_tools.protoc -I./ --python_out=./ --grpc_python_out=./ ./text_extract.proto

class SenseExtractResult(object):

    def __init__(self, resp):
        self.text = resp.text
        self.time = resp.time
        self.title = resp.title
        self.code = resp.code
        self.msg = resp.msg

    def is_code_pattern_failed(self):
        return self.code == -6

    def __str__(self):
        return "code={0},msg={1},title={2},time={3},text={4}".format(self.code, self.msg, self.title, self.time,
                                                                     self.text)


class SenseTextExtractor(object):

    def __init__(self, host=None, port=None, label=None):
        if label and len(label) > 0:
            self.host = sd.config(label, 'host')
            self.port = sd.config(label, 'port')
        else:
            self.host = host
            self.port = port

    def extract_text0(self, url, title, html='', pattern=None):
        channel = grpc.insecure_channel(self.host + ':' + self.port)
        stub = text_extract_pb2_grpc.TextExtractorStub(channel)
        extract_pattern = None
        if pattern:
            extract_pattern = text_extract_pb2.ExtractPattern(text=pattern.get('text'), title=pattern.get('title'),
                                                              time=pattern.get('time'))
        resp = stub.extract(text_extract_pb2.ExtractRequest(url=url, title=title, html=html, pattern=extract_pattern))

        result = SenseExtractResult(resp)
        if len(result.text) == 0:
            sd.log_info('extract text failed for ' + url + ' code is ' + str(resp.code))
        return result

    def extract_text(self, url, title, html='', pattern=None, retry_all=False):
        if not retry_all:
            return self.extract_text0(url, title, html, pattern)
        while True:
            try:
                return self.extract_text0(url, title, html, pattern)
            except Exception as ex:
                sd.log_exception(ex)
                sd.sleep(2)
