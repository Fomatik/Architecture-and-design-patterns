class GetRequests:

    @staticmethod
    def parse_input_param(params: str) -> dict:
        result = {}
        if params:
            params_list = params.split('&')
            for param in params_list:
                k, v = param.split('=')
                result[k] = v
        return result

    def get_request_params(self, request: dict) -> dict:
        params = self.parse_input_param(request['QUERY_STRING'])
        return params


class PostRequests:

    @staticmethod
    def parse_input_param(params: str) -> dict:
        result = {}
        if params:
            params_list = params.split('&')
            for param in params_list:
                k, v = param.split('=')
                result[k] = v
        return result

    @staticmethod
    def get_wsgi_input_data(data: dict) -> bytes:
        content_len_data = data.get('CONTENT_LENGTH')
        content_len = int(content_len_data) if content_len_data else 0

        data = data['wsgi.input'].read(content_len) if content_len else b''
        return data

    def parse_wsgi_input_data(self, data: bytes) -> dict:
        if data:
            data_str = data.decode('utf-8')
            data_dict = self.parse_input_param(data_str)
            return data_dict

    def get_wsgi_input_params(self, data: dict) -> dict:
        data = self.get_wsgi_input_data(data)
        data_dict = self.parse_wsgi_input_data(data)
        return data_dict
