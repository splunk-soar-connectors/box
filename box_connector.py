# --
# File: box_connector.py
#
# Copyright (c) 2018 Splunk Inc.
#
# SPLUNK CONFIDENTIAL – Use or disclosure of this material in whole or in part
# without a valid written license from Splunk Inc. is PROHIBITED.
#
# --

# Phantom App imports
import phantom.app as phantom
from phantom.base_connector import BaseConnector
from phantom.action_result import ActionResult
from phantom.vault import Vault

# Usage of the consts file is recommended
# from box_consts import *
import requests
import json
from bs4 import BeautifulSoup

from box import box


class RetVal(tuple):
    def __new__(cls, val1, val2=None):
        return tuple.__new__(RetVal, (val1, val2))


class BoxConnector(BaseConnector):

    def __init__(self):

        # Call the BaseConnectors init first
        super(BoxConnector, self).__init__()

    def _handle_test_connectivity(self, param):

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        # NOTE: test connectivity does _NOT_ take any parameters
        # i.e. the param dictionary passed to this handler will be empty.
        # Also typically it does not add any data into an action_result either.
        # The status and progress messages are more important.
        access_token = self.box._get_auth_token()
        if isinstance(access_token, str) or access_token is None:
            self.save_progress("Whoops, something went wrong in retrieving a token: " + str(access_token))
            return action_result.set_status(phantom.APP_ERROR)
        headers = {"Authorization": "Bearer " + str(access_token)}

        result = self.box._make_rest_call(url="https://api.box.com/2.0/folders/0", headers=headers)
        if result.get("type") != "error":
            self.save_progress("Test Connectivity Success")
            return action_result.set_status(phantom.APP_SUCCESS)
        else:
            self.save_progress("Test Connectivity Failed")
            return action_result.set_status(phantom.APP_ERROR)

    def _handle_upload_file(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))
        # Implement the handler here
        # use self.save_progress(...) to send progress messages back to the platform
        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))
        name = param["file_name"]
        folder_id = param["folder_id"]
        vault_id = param["vault_id"]

        file_path = Vault.get_file_path(vault_id)
        try:
            file = open(file_path)
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, "There was an issue opening the file: " + str(e.message))

        result = self.box._create_file(name=name, parent_id=folder_id, file=file)

        # Add an action result object to self (BaseConnector) to represent the action for this param

        action_result.add_data(result)
        summary = {}
        if result.get('type') != 'error' and result.get('entries'):
            entries = result.get('entries')[0]
            summary['file_id'] = str(entries.get('id'))
            summary['sha1'] = entries.get('sha1')
            summary = action_result.update_summary(summary)
        else:
            return action_result.set_status(phantom.APP_ERROR, "There was an issue with the file creation: " + str(result))
        # Add a dictionary that is made up of the most important values from data into the summary
        # BaseConnector will create a textual message based off of the summary dictionary
        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_create_folder(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))
        # Implement the handler here
        # use self.save_progress(...) to send progress messages back to the platform
        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))
        name = param["folder_name"]
        parent_id = param["parent_id"]

        result = self.box._create_folder(name=name, parent_id=parent_id)

        action_result.add_data(result)
        summary = {}

        if result.get('type') != 'error':
            summary['folder_id'] = str(result.get('id'))
            summary = action_result.update_summary(summary)
        else:
            return action_result.set_status(phantom.APP_ERROR, "There was an issue with the folder creation: " + str(result))
        # Add a dictionary that is made up of the most important values from data into the summary
        # BaseConnector will create a textual message based off of the summary dictionary
        return action_result.set_status(phantom.APP_SUCCESS)

    def handle_action(self, param):

        ret_val = phantom.APP_SUCCESS

        # Get the action that we are supposed to execute for this App Run
        action_id = self.get_action_identifier()

        self.debug_print("action_id", self.get_action_identifier())

        if action_id == 'test_connectivity':
            ret_val = self._handle_test_connectivity(param)

        elif action_id == 'upload_file':
            ret_val = self._handle_upload_file(param)

        elif action_id == 'create_folder':
            ret_val = self._handle_create_folder(param)

        return ret_val

    def initialize(self):

        # Load the state in initialize, use it to store data
        # that needs to be accessed across actions
        self._state = self.load_state()

        # get the asset config
        config = self.get_config()
        self.public_key = config.get('public_key')
        self.private_key = config.get('private_key')
        self.kid = config.get('box_key_kid')
        self.box_user_id = config.get('box_user_id')
        self.client_id = config.get('client_id')
        self.client_secret = config.get('client_secret')

        self.box = box(
            client_id=self.client_id,
            client_secret=self.client_secret,
            public_key=self.public_key,
            private_key=self.private_key,
            box_user_id=self.box_user_id,
            box_kid=self.kid
        )

        """
        # Access values in asset config by the name

        # Required values can be accessed directly
        required_config_name = config['required_config_name']

        # Optional values should use the .get() function
        optional_config_name = config.get('optional_config_name')
        """

        # self._base_url = config.get('base_url')

        return phantom.APP_SUCCESS

    def finalize(self):

        # Save the state, this data is saved accross actions and app upgrades
        self.save_state(self._state)
        return phantom.APP_SUCCESS


if __name__ == '__main__':

    import pudb
    import argparse

    pudb.set_trace()

    argparser = argparse.ArgumentParser()

    argparser.add_argument('input_test_json', help='Input Test JSON file')
    argparser.add_argument('-u', '--username', help='username', required=False)
    argparser.add_argument('-p', '--password', help='password', required=False)

    args = argparser.parse_args()
    session_id = None

    username = args.username
    password = args.password

    if (username is not None and password is None):

        # User specified a username but not a password, so ask
        import getpass
        password = getpass.getpass("Password: ")

    if (username and password):
        try:
            print ("Accessing the Login page")
            r = requests.get("https://127.0.0.1/login", verify=False)
            csrftoken = r.cookies['csrftoken']

            data = dict()
            data['username'] = username
            data['password'] = password
            data['csrfmiddlewaretoken'] = csrftoken

            headers = dict()
            headers['Cookie'] = 'csrftoken=' + csrftoken
            headers['Referer'] = 'https://127.0.0.1/login'

            print ("Logging into Platform to get the session id")
            r2 = requests.post("https://127.0.0.1/login", verify=False, data=data, headers=headers)
            session_id = r2.cookies['sessionid']
        except Exception as e:
            print ("Unable to get session id from the platfrom. Error: " + str(e))
            exit(1)

    with open(args.input_test_json) as f:
        in_json = f.read()
        in_json = json.loads(in_json)
        print(json.dumps(in_json, indent=4))

        connector = BoxConnector()
        connector.print_progress_message = True

        if (session_id is not None):
            in_json['user_session_token'] = session_id
            connector._set_csrf_info(csrftoken, headers['Referer'])

        ret_val = connector._handle_action(json.dumps(in_json), None)
        print (json.dumps(json.loads(ret_val), indent=4))

    exit(0)
