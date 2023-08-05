# coding: utf-8

"""
    HyperDrive

    HyperDrive REST API

    OpenAPI spec version: 1.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

from __future__ import absolute_import

import sys
import os
import re

# python 2 and python 3 compatibility library
from six import iteritems

from ..configuration import Configuration
from ..api_client import ApiClient


class ExperimentApi(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        config = Configuration()
        if api_client:
            self.api_client = api_client
        else:
            if not config.api_client:
                config.api_client = ApiClient()
            self.api_client = config.api_client

    def cancel_experiment(self, arm_scope, run_id, authorization, run_history_host, **kwargs):
        """
        
        

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.cancel_experiment(arm_scope, run_id, authorization, run_history_host, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str arm_scope:  (required)
        :param str run_id:  (required)
        :param str authorization:  (required)
        :param str run_history_host:  (required)
        :return: CancelExperimentResposeDto
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.cancel_experiment_with_http_info(arm_scope, run_id, authorization, run_history_host, **kwargs)
        else:
            (data) = self.cancel_experiment_with_http_info(arm_scope, run_id, authorization, run_history_host, **kwargs)
            return data

    def cancel_experiment_with_http_info(self, arm_scope, run_id, authorization, run_history_host, **kwargs):
        """
        
        

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.cancel_experiment_with_http_info(arm_scope, run_id, authorization, run_history_host, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str arm_scope:  (required)
        :param str run_id:  (required)
        :param str authorization:  (required)
        :param str run_history_host:  (required)
        :return: CancelExperimentResposeDto
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['arm_scope', 'run_id', 'authorization', 'run_history_host']
        all_params.append('callback')
        all_params.append('_return_http_data_only')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method cancel_experiment" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'arm_scope' is set
        if ('arm_scope' not in params) or (params['arm_scope'] is None):
            raise ValueError("Missing the required parameter `arm_scope` when calling `cancel_experiment`")
        # verify the required parameter 'run_id' is set
        if ('run_id' not in params) or (params['run_id'] is None):
            raise ValueError("Missing the required parameter `run_id` when calling `cancel_experiment`")
        # verify the required parameter 'authorization' is set
        if ('authorization' not in params) or (params['authorization'] is None):
            raise ValueError("Missing the required parameter `authorization` when calling `cancel_experiment`")
        # verify the required parameter 'run_history_host' is set
        if ('run_history_host' not in params) or (params['run_history_host'] is None):
            raise ValueError("Missing the required parameter `run_history_host` when calling `cancel_experiment`")

        resource_path = '/{arm_scope}/runs/{run_id}/cancel'.replace('{format}', 'json')
        path_params = {}
        if 'arm_scope' in params:
            path_params['arm_scope'] = params['arm_scope']
        if 'run_id' in params:
            path_params['run_id'] = params['run_id']

        query_params = {}

        header_params = {}
        if 'authorization' in params:
            header_params['Authorization'] = params['authorization']
        if 'run_history_host' in params:
            header_params['RunHistoryHost'] = params['run_history_host']

        form_params = []
        local_var_files = {}

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = []

        return self.api_client.call_api(resource_path, 'POST',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='CancelExperimentResposeDto',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'),
                                            _return_http_data_only=params.get('_return_http_data_only'))

    def create_experiment(self, arm_scope, config, authorization, **kwargs):
        """
        
        

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.create_experiment(arm_scope, config, authorization, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str arm_scope:  (required)
        :param file config:  (required)
        :param str authorization:  (required)
        :return: ExperimentResponseDto
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.create_experiment_with_http_info(arm_scope, config, authorization, **kwargs)
        else:
            (data) = self.create_experiment_with_http_info(arm_scope, config, authorization, **kwargs)
            return data

    def create_experiment_with_http_info(self, arm_scope, config, authorization, **kwargs):
        """
        
        

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.create_experiment_with_http_info(arm_scope, config, authorization, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str arm_scope:  (required)
        :param file config:  (required)
        :param str authorization:  (required)
        :return: ExperimentResponseDto
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['arm_scope', 'config', 'authorization']
        all_params.append('callback')
        all_params.append('_return_http_data_only')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_experiment" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'arm_scope' is set
        if ('arm_scope' not in params) or (params['arm_scope'] is None):
            raise ValueError("Missing the required parameter `arm_scope` when calling `create_experiment`")
        # verify the required parameter 'config' is set
        if ('config' not in params) or (params['config'] is None):
            raise ValueError("Missing the required parameter `config` when calling `create_experiment`")
        # verify the required parameter 'authorization' is set
        if ('authorization' not in params) or (params['authorization'] is None):
            raise ValueError("Missing the required parameter `authorization` when calling `create_experiment`")

        resource_path = '/{arm_scope}/runs'.replace('{format}', 'json')
        path_params = {}
        if 'arm_scope' in params:
            path_params['arm_scope'] = params['arm_scope']

        query_params = {}

        header_params = {}
        if 'authorization' in params:
            header_params['Authorization'] = params['authorization']

        form_params = []
        local_var_files = {}
        if 'config' in params:
            local_var_files['config'] = params['config']

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['multipart/form-data'])

        # Authentication setting
        auth_settings = []

        return self.api_client.call_api(resource_path, 'POST',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='ExperimentResponseDto',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'),
                                            _return_http_data_only=params.get('_return_http_data_only'))
