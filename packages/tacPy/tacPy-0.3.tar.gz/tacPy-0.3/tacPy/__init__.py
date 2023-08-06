"""
A quick little Talend Administration Server API Client

Developed against Talend 6.3
"""
__all__ = ['Client']
import requests
import json
import base64
import os

INCLUDED_HELP_LOCATION = os.path.dirname(__file__) + '/full_tac_api_help.txt.example'  # Deprecated - For Reference


def process_help_file(help_text):
    """
    Returns a dictionary sort of representing important bits from the API help output
    """
    split_help = help_text.splitlines()

    command_dict = {}
    in_sample = False
    in_ec = False
    sample_line_list = []

    for line in split_help:
        ss = line.split(':')
        if ss[0].strip() == 'Command':
            current_command = ss[1].strip()
            command_dict[current_command] = {
                'require_auth': True,
                'sample': '',
                'spec_error_codes': {}
            }
            continue

        if ss[0].strip() == 'Requires authentication':
            command_dict[current_command]['require_auth'] = True if ss[1].strip() == 'true' else False
            continue

        if ss[0].strip() == 'Sample':
            in_sample = True
            continue

        if in_sample:
            if line.strip() == '':
                in_sample = False
                command_dict[current_command]['sample'] = '\n'.join(sample_line_list)
                sample_line_list = []
                continue
            if ss[0].strip() == 'Specific error codes':
                in_sample = False
                in_ec = True
                command_dict[current_command]['sample'] = '\n'.join(sample_line_list)
                sample_line_list = []
                continue

            sample_line_list.append(line)

        if in_ec:
            if line.strip() == '':
                in_ec = False
                continue

            command_dict[current_command]['spec_error_codes'][int(ss[0].strip())] = ss[1].strip()

    return command_dict


class Client:
    def _build_help(self):
        """
        This basically builds the help file as seen in the example
        :return:
        """
        h = Method(base_url=self.base_url, action_name='help', requires_auth=False,
                   auth_user=self.auth_user, auth_pass=self.auth_pass, response_codes={}, sample=None)

        api_help_text = ''

        for l in h().json()['help'].splitlines():
            sl = l.strip()
            if len(sl) > 0 and sl[0] == '*':
                c = sl.split()[1]
                api_help_text += h(commandName=c).json()['help']

        return api_help_text

    def __init__(self, tac_host, auth_pass=None, auth_user=None,
                 tac_name='org.talend.administrator', tac_port='8080', protocol='http'):
        self.auth_pass = auth_pass
        self.auth_user = auth_user
        self.base_url = protocol + '://' + tac_host + ':' + tac_port + '/' + tac_name + '/metaServlet?'
        self.help_file = process_help_file(self._build_help())

        self.endpoint = EmptyObj()
        for command, data in self.help_file.items():
            setattr(
                self.endpoint,
                command,
                Method(base_url=self.base_url, action_name=command, requires_auth=data['require_auth'],
                       auth_user=self.auth_user, auth_pass=self.auth_pass, response_codes=data['spec_error_codes'],
                       sample=data['sample'])
            )


class Method:
    def __init__(self, base_url, action_name, requires_auth, auth_user, auth_pass, response_codes, sample):
        self.last_response = None
        self.response_codes = response_codes
        self.__doc__ = 'Sample params for {an}:\n\n{s}'.format(an=action_name, s=sample)
        self.base_url = base_url
        self.base_params = {
            'actionName': action_name
        }

        if requires_auth:
            self.base_params['authUser'] = auth_user
            self.base_params['authPass'] = auth_pass

    def __call__(self, **kwargs):
        params = self.base_params.copy()
        for k, v in kwargs.items():
            params[k] = v

        encoded_params = base64.b64encode(json.dumps(params).encode('utf-8')).decode('utf-8')
        full_url = self.base_url + encoded_params

        self.last_response = requests.get(url=full_url)
        return self.last_response

    def jr(self, **kwargs):
        """
        Return the dict of the return instead of the requests object
        :param kwargs:
        :return: dict
        """
        return self(**kwargs).json()

    def print_sample(self):
        """
        Print it on the fly
        :return:
        """
        print(self.__doc__)
        return None

    def return_sample(self):
        """
        For when you want to return the sample as a string
        :return:
        """
        return self.__doc__


class EmptyObj:
    pass
