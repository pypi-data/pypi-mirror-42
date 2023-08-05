# coding: utf-8

"""
    Web API Swagger specification

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

    OpenAPI spec version: 1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import sys
import os
import re

# python 2 and python 3 compatibility library
from six import iteritems

from ..configuration import Configuration
from ..api_client import ApiClient


class OAuthApi(object):
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

    def o_auth_post(self, grant_type, client_id, client_secret, **kwargs):
        """
        Get Access token
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.o_auth_post(grant_type, client_id, client_secret, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str grant_type: Grant Type (required)
        :param str client_id: App SID (required)
        :param str client_secret: App Key (required)
        :return: AccessTokenResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.o_auth_post_with_http_info(grant_type, client_id, client_secret, **kwargs)
        else:
            (data) = self.o_auth_post_with_http_info(grant_type, client_id, client_secret, **kwargs)
            return data

    def o_auth_post_with_http_info(self, grant_type, client_id, client_secret, **kwargs):
        """
        Get Access token
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.o_auth_post_with_http_info(grant_type, client_id, client_secret, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str grant_type: Grant Type (required)
        :param str client_id: App SID (required)
        :param str client_secret: App Key (required)
        :return: AccessTokenResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['grant_type', 'client_id', 'client_secret']
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method o_auth_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'grant_type' is set
        if ('grant_type' not in params) or (params['grant_type'] is None):
            raise ValueError("Missing the required parameter `grant_type` when calling `o_auth_post`")
        # verify the required parameter 'client_id' is set
        if ('client_id' not in params) or (params['client_id'] is None):
            raise ValueError("Missing the required parameter `client_id` when calling `o_auth_post`")
        # verify the required parameter 'client_secret' is set
        if ('client_secret' not in params) or (params['client_secret'] is None):
            raise ValueError("Missing the required parameter `client_secret` when calling `o_auth_post`")


        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'grant_type' in params:
            form_params.append(('grant_type', params['grant_type']))
        if 'client_id' in params:
            form_params.append(('client_id', params['client_id']))
        if 'client_secret' in params:
            form_params.append(('client_secret', params['client_secret']))

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/x-www-form-urlencoded'])

        # Authentication setting
        auth_settings = []

        return self.api_client.call_api('/oauth2/token', 'POST',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='AccessTokenResponse',
                                        auth_settings=auth_settings,
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)
