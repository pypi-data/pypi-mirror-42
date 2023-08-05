# coding: utf-8

# -----------------------------------------------------------------------------------
# <copyright company="Aspose">
#   Copyright (c) 2018 Aspose.Slides for Cloud
# </copyright>
# <summary>
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
# </summary>
# -----------------------------------------------------------------------------------

from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from asposeslidescloud.apis.api_base import ApiBase
from asposeslidescloud.api_client import ApiClient

class NotesSlideShapesApi(ApiBase):

    def __init__(self, configuration = None, app_sid = None, app_key = None):
        super(NotesSlideShapesApi, self).__init__(configuration, app_sid, app_key)

    def delete_notes_slide_paragraph(self, request, **kwargs):  # noqa: E501
        """Removes a shape, specified shapes or all shapes.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.delete_notes_slide_paragraph(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param delete_notes_slide_paragraphRequest request: delete_notes_slide_paragraph request object
        :return: ParagraphListResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('is_async'):
            return self.delete_notes_slide_paragraph_with_http_info(request, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_notes_slide_paragraph_with_http_info(request, **kwargs)  # noqa: E501
            return data

    def delete_notes_slide_paragraph_with_http_info(self, request, **kwargs):  # noqa: E501
        """Removes a shape, specified shapes or all shapes.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.delete_notes_slide_paragraph_with_http_info(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param delete_notes_slide_paragraphRequest request: delete_notes_slide_paragraph request object
        :return: ParagraphListResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = []  # noqa: E501
        all_params.append('is_async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_notes_slide_paragraph" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if not request.name:
            raise ValueError("Missing the required parameter `request.name` when calling `delete_notes_slide_paragraph`")  # noqa: E501
        # verify the required parameter 'slide_index' is set
        if not request.slide_index:
            raise ValueError("Missing the required parameter `request.slide_index` when calling `delete_notes_slide_paragraph`")  # noqa: E501
        # verify the required parameter 'shape_index' is set
        if not request.shape_index:
            raise ValueError("Missing the required parameter `request.shape_index` when calling `delete_notes_slide_paragraph`")  # noqa: E501
        # verify the required parameter 'paragraph_index' is set
        if not request.paragraph_index:
            raise ValueError("Missing the required parameter `request.paragraph_index` when calling `delete_notes_slide_paragraph`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        path_params['name'] = request.name  # noqa: E501
        path_params['slideIndex'] = request.slide_index  # noqa: E501
        path_params['path'] = request.path  # noqa: E501
        path_params['shapeIndex'] = request.shape_index  # noqa: E501
        path_params['paragraphIndex'] = request.paragraph_index  # noqa: E501

        query_params = []
        if request.password:
            query_params.append(('password', request.password))  # noqa: E501
        if request.folder:
            query_params.append(('folder', request.folder))  # noqa: E501
        if request.storage:
            query_params.append(('storage', request.storage))  # noqa: E501

        header_params = {}

        form_params = []

        body_params = None

        files = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/slides/{name}/slides/{slideIndex}/notesSlide/shapes/{path}/{shapeIndex}/paragraphs/{paragraphIndex}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=files,
            response_type='ParagraphListResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def delete_notes_slide_paragraphs(self, request, **kwargs):  # noqa: E501
        """Removes a shape, specified shapes or all shapes.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.delete_notes_slide_paragraphs(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param delete_notes_slide_paragraphsRequest request: delete_notes_slide_paragraphs request object
        :return: ParagraphListResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('is_async'):
            return self.delete_notes_slide_paragraphs_with_http_info(request, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_notes_slide_paragraphs_with_http_info(request, **kwargs)  # noqa: E501
            return data

    def delete_notes_slide_paragraphs_with_http_info(self, request, **kwargs):  # noqa: E501
        """Removes a shape, specified shapes or all shapes.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.delete_notes_slide_paragraphs_with_http_info(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param delete_notes_slide_paragraphsRequest request: delete_notes_slide_paragraphs request object
        :return: ParagraphListResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = []  # noqa: E501
        all_params.append('is_async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_notes_slide_paragraphs" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if not request.name:
            raise ValueError("Missing the required parameter `request.name` when calling `delete_notes_slide_paragraphs`")  # noqa: E501
        # verify the required parameter 'slide_index' is set
        if not request.slide_index:
            raise ValueError("Missing the required parameter `request.slide_index` when calling `delete_notes_slide_paragraphs`")  # noqa: E501
        # verify the required parameter 'shape_index' is set
        if not request.shape_index:
            raise ValueError("Missing the required parameter `request.shape_index` when calling `delete_notes_slide_paragraphs`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        path_params['name'] = request.name  # noqa: E501
        path_params['slideIndex'] = request.slide_index  # noqa: E501
        path_params['path'] = request.path  # noqa: E501
        path_params['shapeIndex'] = request.shape_index  # noqa: E501

        query_params = []
        if request.paragraphs:
            query_params.append(('paragraphs', request.paragraphs))  # noqa: E501
            collection_formats['paragraphs'] = ''  # noqa: E501
        if request.password:
            query_params.append(('password', request.password))  # noqa: E501
        if request.folder:
            query_params.append(('folder', request.folder))  # noqa: E501
        if request.storage:
            query_params.append(('storage', request.storage))  # noqa: E501

        header_params = {}

        form_params = []

        body_params = None

        files = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/slides/{name}/slides/{slideIndex}/notesSlide/shapes/{path}/{shapeIndex}/paragraphs', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=files,
            response_type='ParagraphListResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def delete_notes_slide_portion(self, request, **kwargs):  # noqa: E501
        """Removes a shape, specified shapes or all shapes.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.delete_notes_slide_portion(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param delete_notes_slide_portionRequest request: delete_notes_slide_portion request object
        :return: PortionListResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('is_async'):
            return self.delete_notes_slide_portion_with_http_info(request, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_notes_slide_portion_with_http_info(request, **kwargs)  # noqa: E501
            return data

    def delete_notes_slide_portion_with_http_info(self, request, **kwargs):  # noqa: E501
        """Removes a shape, specified shapes or all shapes.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.delete_notes_slide_portion_with_http_info(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param delete_notes_slide_portionRequest request: delete_notes_slide_portion request object
        :return: PortionListResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = []  # noqa: E501
        all_params.append('is_async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_notes_slide_portion" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if not request.name:
            raise ValueError("Missing the required parameter `request.name` when calling `delete_notes_slide_portion`")  # noqa: E501
        # verify the required parameter 'slide_index' is set
        if not request.slide_index:
            raise ValueError("Missing the required parameter `request.slide_index` when calling `delete_notes_slide_portion`")  # noqa: E501
        # verify the required parameter 'shape_index' is set
        if not request.shape_index:
            raise ValueError("Missing the required parameter `request.shape_index` when calling `delete_notes_slide_portion`")  # noqa: E501
        # verify the required parameter 'paragraph_index' is set
        if not request.paragraph_index:
            raise ValueError("Missing the required parameter `request.paragraph_index` when calling `delete_notes_slide_portion`")  # noqa: E501
        # verify the required parameter 'portion_index' is set
        if not request.portion_index:
            raise ValueError("Missing the required parameter `request.portion_index` when calling `delete_notes_slide_portion`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        path_params['name'] = request.name  # noqa: E501
        path_params['slideIndex'] = request.slide_index  # noqa: E501
        path_params['path'] = request.path  # noqa: E501
        path_params['shapeIndex'] = request.shape_index  # noqa: E501
        path_params['paragraphIndex'] = request.paragraph_index  # noqa: E501
        path_params['portionIndex'] = request.portion_index  # noqa: E501

        query_params = []
        if request.password:
            query_params.append(('password', request.password))  # noqa: E501
        if request.folder:
            query_params.append(('folder', request.folder))  # noqa: E501
        if request.storage:
            query_params.append(('storage', request.storage))  # noqa: E501

        header_params = {}

        form_params = []

        body_params = None

        files = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/slides/{name}/slides/{slideIndex}/notesSlide/shapes/{path}/{shapeIndex}/paragraphs/{paragraphIndex}/portions/{portionIndex}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=files,
            response_type='PortionListResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def delete_notes_slide_portions(self, request, **kwargs):  # noqa: E501
        """Removes a shape, specified shapes or all shapes.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.delete_notes_slide_portions(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param delete_notes_slide_portionsRequest request: delete_notes_slide_portions request object
        :return: PortionListResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('is_async'):
            return self.delete_notes_slide_portions_with_http_info(request, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_notes_slide_portions_with_http_info(request, **kwargs)  # noqa: E501
            return data

    def delete_notes_slide_portions_with_http_info(self, request, **kwargs):  # noqa: E501
        """Removes a shape, specified shapes or all shapes.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.delete_notes_slide_portions_with_http_info(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param delete_notes_slide_portionsRequest request: delete_notes_slide_portions request object
        :return: PortionListResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = []  # noqa: E501
        all_params.append('is_async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_notes_slide_portions" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if not request.name:
            raise ValueError("Missing the required parameter `request.name` when calling `delete_notes_slide_portions`")  # noqa: E501
        # verify the required parameter 'slide_index' is set
        if not request.slide_index:
            raise ValueError("Missing the required parameter `request.slide_index` when calling `delete_notes_slide_portions`")  # noqa: E501
        # verify the required parameter 'shape_index' is set
        if not request.shape_index:
            raise ValueError("Missing the required parameter `request.shape_index` when calling `delete_notes_slide_portions`")  # noqa: E501
        # verify the required parameter 'paragraph_index' is set
        if not request.paragraph_index:
            raise ValueError("Missing the required parameter `request.paragraph_index` when calling `delete_notes_slide_portions`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        path_params['name'] = request.name  # noqa: E501
        path_params['slideIndex'] = request.slide_index  # noqa: E501
        path_params['path'] = request.path  # noqa: E501
        path_params['shapeIndex'] = request.shape_index  # noqa: E501
        path_params['paragraphIndex'] = request.paragraph_index  # noqa: E501

        query_params = []
        if request.portions:
            query_params.append(('portions', request.portions))  # noqa: E501
            collection_formats['portions'] = ''  # noqa: E501
        if request.password:
            query_params.append(('password', request.password))  # noqa: E501
        if request.folder:
            query_params.append(('folder', request.folder))  # noqa: E501
        if request.storage:
            query_params.append(('storage', request.storage))  # noqa: E501

        header_params = {}

        form_params = []

        body_params = None

        files = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/slides/{name}/slides/{slideIndex}/notesSlide/shapes/{path}/{shapeIndex}/paragraphs/{paragraphIndex}/portions', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=files,
            response_type='PortionListResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def delete_notes_slide_shape(self, request, **kwargs):  # noqa: E501
        """Removes a shape, specified shapes or all shapes.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.delete_notes_slide_shape(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param delete_notes_slide_shapeRequest request: delete_notes_slide_shape request object
        :return: ShapeListResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('is_async'):
            return self.delete_notes_slide_shape_with_http_info(request, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_notes_slide_shape_with_http_info(request, **kwargs)  # noqa: E501
            return data

    def delete_notes_slide_shape_with_http_info(self, request, **kwargs):  # noqa: E501
        """Removes a shape, specified shapes or all shapes.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.delete_notes_slide_shape_with_http_info(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param delete_notes_slide_shapeRequest request: delete_notes_slide_shape request object
        :return: ShapeListResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = []  # noqa: E501
        all_params.append('is_async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_notes_slide_shape" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if not request.name:
            raise ValueError("Missing the required parameter `request.name` when calling `delete_notes_slide_shape`")  # noqa: E501
        # verify the required parameter 'slide_index' is set
        if not request.slide_index:
            raise ValueError("Missing the required parameter `request.slide_index` when calling `delete_notes_slide_shape`")  # noqa: E501
        # verify the required parameter 'shape_index' is set
        if not request.shape_index:
            raise ValueError("Missing the required parameter `request.shape_index` when calling `delete_notes_slide_shape`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        path_params['name'] = request.name  # noqa: E501
        path_params['slideIndex'] = request.slide_index  # noqa: E501
        path_params['path'] = request.path  # noqa: E501
        path_params['shapeIndex'] = request.shape_index  # noqa: E501

        query_params = []
        if request.password:
            query_params.append(('password', request.password))  # noqa: E501
        if request.folder:
            query_params.append(('folder', request.folder))  # noqa: E501
        if request.storage:
            query_params.append(('storage', request.storage))  # noqa: E501

        header_params = {}

        form_params = []

        body_params = None

        files = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/slides/{name}/slides/{slideIndex}/notesSlide/shapes/{path}/{shapeIndex}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=files,
            response_type='ShapeListResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def delete_notes_slide_shapes(self, request, **kwargs):  # noqa: E501
        """Removes a shape, specified shapes or all shapes.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.delete_notes_slide_shapes(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param delete_notes_slide_shapesRequest request: delete_notes_slide_shapes request object
        :return: ShapeListResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('is_async'):
            return self.delete_notes_slide_shapes_with_http_info(request, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_notes_slide_shapes_with_http_info(request, **kwargs)  # noqa: E501
            return data

    def delete_notes_slide_shapes_with_http_info(self, request, **kwargs):  # noqa: E501
        """Removes a shape, specified shapes or all shapes.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.delete_notes_slide_shapes_with_http_info(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param delete_notes_slide_shapesRequest request: delete_notes_slide_shapes request object
        :return: ShapeListResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = []  # noqa: E501
        all_params.append('is_async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_notes_slide_shapes" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if not request.name:
            raise ValueError("Missing the required parameter `request.name` when calling `delete_notes_slide_shapes`")  # noqa: E501
        # verify the required parameter 'slide_index' is set
        if not request.slide_index:
            raise ValueError("Missing the required parameter `request.slide_index` when calling `delete_notes_slide_shapes`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        path_params['name'] = request.name  # noqa: E501
        path_params['slideIndex'] = request.slide_index  # noqa: E501
        path_params['path'] = request.path  # noqa: E501

        query_params = []
        if request.shapes:
            query_params.append(('shapes', request.shapes))  # noqa: E501
            collection_formats['shapes'] = ''  # noqa: E501
        if request.password:
            query_params.append(('password', request.password))  # noqa: E501
        if request.folder:
            query_params.append(('folder', request.folder))  # noqa: E501
        if request.storage:
            query_params.append(('storage', request.storage))  # noqa: E501

        header_params = {}

        form_params = []

        body_params = None

        files = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/slides/{name}/slides/{slideIndex}/notesSlide/shapes/{path}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=files,
            response_type='ShapeListResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_notes_slide_shape(self, request, **kwargs):  # noqa: E501
        """Read slide shapes or shape info.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.get_notes_slide_shape(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param get_notes_slide_shapeRequest request: get_notes_slide_shape request object
        :return: ShapeResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('is_async'):
            return self.get_notes_slide_shape_with_http_info(request, **kwargs)  # noqa: E501
        else:
            (data) = self.get_notes_slide_shape_with_http_info(request, **kwargs)  # noqa: E501
            return data

    def get_notes_slide_shape_with_http_info(self, request, **kwargs):  # noqa: E501
        """Read slide shapes or shape info.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.get_notes_slide_shape_with_http_info(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param get_notes_slide_shapeRequest request: get_notes_slide_shape request object
        :return: ShapeResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = []  # noqa: E501
        all_params.append('is_async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_notes_slide_shape" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if not request.name:
            raise ValueError("Missing the required parameter `request.name` when calling `get_notes_slide_shape`")  # noqa: E501
        # verify the required parameter 'slide_index' is set
        if not request.slide_index:
            raise ValueError("Missing the required parameter `request.slide_index` when calling `get_notes_slide_shape`")  # noqa: E501
        # verify the required parameter 'shape_index' is set
        if not request.shape_index:
            raise ValueError("Missing the required parameter `request.shape_index` when calling `get_notes_slide_shape`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        path_params['name'] = request.name  # noqa: E501
        path_params['slideIndex'] = request.slide_index  # noqa: E501
        path_params['path'] = request.path  # noqa: E501
        path_params['shapeIndex'] = request.shape_index  # noqa: E501

        query_params = []
        if request.password:
            query_params.append(('password', request.password))  # noqa: E501
        if request.folder:
            query_params.append(('folder', request.folder))  # noqa: E501
        if request.storage:
            query_params.append(('storage', request.storage))  # noqa: E501

        header_params = {}

        form_params = []

        body_params = None

        files = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['multipart/form-data'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/slides/{name}/slides/{slideIndex}/notesSlide/shapes/{path}/{shapeIndex}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=files,
            response_type='ShapeResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_notes_slide_shape_paragraph(self, request, **kwargs):  # noqa: E501
        """Read slide shapes or shape info.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.get_notes_slide_shape_paragraph(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param get_notes_slide_shape_paragraphRequest request: get_notes_slide_shape_paragraph request object
        :return: ParagraphResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('is_async'):
            return self.get_notes_slide_shape_paragraph_with_http_info(request, **kwargs)  # noqa: E501
        else:
            (data) = self.get_notes_slide_shape_paragraph_with_http_info(request, **kwargs)  # noqa: E501
            return data

    def get_notes_slide_shape_paragraph_with_http_info(self, request, **kwargs):  # noqa: E501
        """Read slide shapes or shape info.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.get_notes_slide_shape_paragraph_with_http_info(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param get_notes_slide_shape_paragraphRequest request: get_notes_slide_shape_paragraph request object
        :return: ParagraphResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = []  # noqa: E501
        all_params.append('is_async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_notes_slide_shape_paragraph" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if not request.name:
            raise ValueError("Missing the required parameter `request.name` when calling `get_notes_slide_shape_paragraph`")  # noqa: E501
        # verify the required parameter 'slide_index' is set
        if not request.slide_index:
            raise ValueError("Missing the required parameter `request.slide_index` when calling `get_notes_slide_shape_paragraph`")  # noqa: E501
        # verify the required parameter 'shape_index' is set
        if not request.shape_index:
            raise ValueError("Missing the required parameter `request.shape_index` when calling `get_notes_slide_shape_paragraph`")  # noqa: E501
        # verify the required parameter 'paragraph_index' is set
        if not request.paragraph_index:
            raise ValueError("Missing the required parameter `request.paragraph_index` when calling `get_notes_slide_shape_paragraph`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        path_params['name'] = request.name  # noqa: E501
        path_params['slideIndex'] = request.slide_index  # noqa: E501
        path_params['path'] = request.path  # noqa: E501
        path_params['shapeIndex'] = request.shape_index  # noqa: E501
        path_params['paragraphIndex'] = request.paragraph_index  # noqa: E501

        query_params = []
        if request.password:
            query_params.append(('password', request.password))  # noqa: E501
        if request.folder:
            query_params.append(('folder', request.folder))  # noqa: E501
        if request.storage:
            query_params.append(('storage', request.storage))  # noqa: E501

        header_params = {}

        form_params = []

        body_params = None

        files = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/slides/{name}/slides/{slideIndex}/notesSlide/shapes/{path}/{shapeIndex}/paragraphs/{paragraphIndex}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=files,
            response_type='ParagraphResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_notes_slide_shape_paragraphs(self, request, **kwargs):  # noqa: E501
        """Read slide shapes or shape info.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.get_notes_slide_shape_paragraphs(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param get_notes_slide_shape_paragraphsRequest request: get_notes_slide_shape_paragraphs request object
        :return: ParagraphListResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('is_async'):
            return self.get_notes_slide_shape_paragraphs_with_http_info(request, **kwargs)  # noqa: E501
        else:
            (data) = self.get_notes_slide_shape_paragraphs_with_http_info(request, **kwargs)  # noqa: E501
            return data

    def get_notes_slide_shape_paragraphs_with_http_info(self, request, **kwargs):  # noqa: E501
        """Read slide shapes or shape info.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.get_notes_slide_shape_paragraphs_with_http_info(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param get_notes_slide_shape_paragraphsRequest request: get_notes_slide_shape_paragraphs request object
        :return: ParagraphListResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = []  # noqa: E501
        all_params.append('is_async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_notes_slide_shape_paragraphs" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if not request.name:
            raise ValueError("Missing the required parameter `request.name` when calling `get_notes_slide_shape_paragraphs`")  # noqa: E501
        # verify the required parameter 'slide_index' is set
        if not request.slide_index:
            raise ValueError("Missing the required parameter `request.slide_index` when calling `get_notes_slide_shape_paragraphs`")  # noqa: E501
        # verify the required parameter 'shape_index' is set
        if not request.shape_index:
            raise ValueError("Missing the required parameter `request.shape_index` when calling `get_notes_slide_shape_paragraphs`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        path_params['name'] = request.name  # noqa: E501
        path_params['slideIndex'] = request.slide_index  # noqa: E501
        path_params['path'] = request.path  # noqa: E501
        path_params['shapeIndex'] = request.shape_index  # noqa: E501

        query_params = []
        if request.password:
            query_params.append(('password', request.password))  # noqa: E501
        if request.folder:
            query_params.append(('folder', request.folder))  # noqa: E501
        if request.storage:
            query_params.append(('storage', request.storage))  # noqa: E501

        header_params = {}

        form_params = []

        body_params = None

        files = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/slides/{name}/slides/{slideIndex}/notesSlide/shapes/{path}/{shapeIndex}/paragraphs', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=files,
            response_type='ParagraphListResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_notes_slide_shape_portion(self, request, **kwargs):  # noqa: E501
        """Read slide shapes or shape info.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.get_notes_slide_shape_portion(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param get_notes_slide_shape_portionRequest request: get_notes_slide_shape_portion request object
        :return: PortionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('is_async'):
            return self.get_notes_slide_shape_portion_with_http_info(request, **kwargs)  # noqa: E501
        else:
            (data) = self.get_notes_slide_shape_portion_with_http_info(request, **kwargs)  # noqa: E501
            return data

    def get_notes_slide_shape_portion_with_http_info(self, request, **kwargs):  # noqa: E501
        """Read slide shapes or shape info.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.get_notes_slide_shape_portion_with_http_info(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param get_notes_slide_shape_portionRequest request: get_notes_slide_shape_portion request object
        :return: PortionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = []  # noqa: E501
        all_params.append('is_async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_notes_slide_shape_portion" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if not request.name:
            raise ValueError("Missing the required parameter `request.name` when calling `get_notes_slide_shape_portion`")  # noqa: E501
        # verify the required parameter 'slide_index' is set
        if not request.slide_index:
            raise ValueError("Missing the required parameter `request.slide_index` when calling `get_notes_slide_shape_portion`")  # noqa: E501
        # verify the required parameter 'shape_index' is set
        if not request.shape_index:
            raise ValueError("Missing the required parameter `request.shape_index` when calling `get_notes_slide_shape_portion`")  # noqa: E501
        # verify the required parameter 'paragraph_index' is set
        if not request.paragraph_index:
            raise ValueError("Missing the required parameter `request.paragraph_index` when calling `get_notes_slide_shape_portion`")  # noqa: E501
        # verify the required parameter 'portion_index' is set
        if not request.portion_index:
            raise ValueError("Missing the required parameter `request.portion_index` when calling `get_notes_slide_shape_portion`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        path_params['name'] = request.name  # noqa: E501
        path_params['slideIndex'] = request.slide_index  # noqa: E501
        path_params['path'] = request.path  # noqa: E501
        path_params['shapeIndex'] = request.shape_index  # noqa: E501
        path_params['paragraphIndex'] = request.paragraph_index  # noqa: E501
        path_params['portionIndex'] = request.portion_index  # noqa: E501

        query_params = []
        if request.password:
            query_params.append(('password', request.password))  # noqa: E501
        if request.folder:
            query_params.append(('folder', request.folder))  # noqa: E501
        if request.storage:
            query_params.append(('storage', request.storage))  # noqa: E501

        header_params = {}

        form_params = []

        body_params = None

        files = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/slides/{name}/slides/{slideIndex}/notesSlide/shapes/{path}/{shapeIndex}/paragraphs/{paragraphIndex}/portions/{portionIndex}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=files,
            response_type='PortionResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_notes_slide_shape_portions(self, request, **kwargs):  # noqa: E501
        """Read slide shapes or shape info.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.get_notes_slide_shape_portions(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param get_notes_slide_shape_portionsRequest request: get_notes_slide_shape_portions request object
        :return: PortionListResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('is_async'):
            return self.get_notes_slide_shape_portions_with_http_info(request, **kwargs)  # noqa: E501
        else:
            (data) = self.get_notes_slide_shape_portions_with_http_info(request, **kwargs)  # noqa: E501
            return data

    def get_notes_slide_shape_portions_with_http_info(self, request, **kwargs):  # noqa: E501
        """Read slide shapes or shape info.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.get_notes_slide_shape_portions_with_http_info(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param get_notes_slide_shape_portionsRequest request: get_notes_slide_shape_portions request object
        :return: PortionListResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = []  # noqa: E501
        all_params.append('is_async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_notes_slide_shape_portions" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if not request.name:
            raise ValueError("Missing the required parameter `request.name` when calling `get_notes_slide_shape_portions`")  # noqa: E501
        # verify the required parameter 'slide_index' is set
        if not request.slide_index:
            raise ValueError("Missing the required parameter `request.slide_index` when calling `get_notes_slide_shape_portions`")  # noqa: E501
        # verify the required parameter 'shape_index' is set
        if not request.shape_index:
            raise ValueError("Missing the required parameter `request.shape_index` when calling `get_notes_slide_shape_portions`")  # noqa: E501
        # verify the required parameter 'paragraph_index' is set
        if not request.paragraph_index:
            raise ValueError("Missing the required parameter `request.paragraph_index` when calling `get_notes_slide_shape_portions`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        path_params['name'] = request.name  # noqa: E501
        path_params['slideIndex'] = request.slide_index  # noqa: E501
        path_params['path'] = request.path  # noqa: E501
        path_params['shapeIndex'] = request.shape_index  # noqa: E501
        path_params['paragraphIndex'] = request.paragraph_index  # noqa: E501

        query_params = []
        if request.password:
            query_params.append(('password', request.password))  # noqa: E501
        if request.folder:
            query_params.append(('folder', request.folder))  # noqa: E501
        if request.storage:
            query_params.append(('storage', request.storage))  # noqa: E501

        header_params = {}

        form_params = []

        body_params = None

        files = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/slides/{name}/slides/{slideIndex}/notesSlide/shapes/{path}/{shapeIndex}/paragraphs/{paragraphIndex}/portions', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=files,
            response_type='PortionListResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_notes_slide_shape_with_format(self, request, **kwargs):  # noqa: E501
        """Render shape to specified picture format.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.get_notes_slide_shape_with_format(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param get_notes_slide_shape_with_formatRequest request: get_notes_slide_shape_with_format request object
        :return: file
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('is_async'):
            return self.get_notes_slide_shape_with_format_with_http_info(request, **kwargs)  # noqa: E501
        else:
            (data) = self.get_notes_slide_shape_with_format_with_http_info(request, **kwargs)  # noqa: E501
            return data

    def get_notes_slide_shape_with_format_with_http_info(self, request, **kwargs):  # noqa: E501
        """Render shape to specified picture format.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.get_notes_slide_shape_with_format_with_http_info(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param get_notes_slide_shape_with_formatRequest request: get_notes_slide_shape_with_format request object
        :return: file
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = []  # noqa: E501
        all_params.append('is_async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_notes_slide_shape_with_format" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if not request.name:
            raise ValueError("Missing the required parameter `request.name` when calling `get_notes_slide_shape_with_format`")  # noqa: E501
        # verify the required parameter 'slide_index' is set
        if not request.slide_index:
            raise ValueError("Missing the required parameter `request.slide_index` when calling `get_notes_slide_shape_with_format`")  # noqa: E501
        # verify the required parameter 'shape_index' is set
        if not request.shape_index:
            raise ValueError("Missing the required parameter `request.shape_index` when calling `get_notes_slide_shape_with_format`")  # noqa: E501
        # verify the required parameter 'format' is set
        if not request.format:
            raise ValueError("Missing the required parameter `request.format` when calling `get_notes_slide_shape_with_format`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        path_params['name'] = request.name  # noqa: E501
        path_params['slideIndex'] = request.slide_index  # noqa: E501
        path_params['shapeIndex'] = request.shape_index  # noqa: E501
        path_params['format'] = request.format  # noqa: E501

        query_params = []
        if request.password:
            query_params.append(('password', request.password))  # noqa: E501
        if request.folder:
            query_params.append(('folder', request.folder))  # noqa: E501
        if request.storage:
            query_params.append(('storage', request.storage))  # noqa: E501
        if request.scale_x:
            query_params.append(('scaleX', request.scale_x))  # noqa: E501
        if request.scale_y:
            query_params.append(('scaleY', request.scale_y))  # noqa: E501
        if request.bounds:
            query_params.append(('bounds', request.bounds))  # noqa: E501
        if request.out_path:
            query_params.append(('outPath', request.out_path))  # noqa: E501
        if request.fonts_folder:
            query_params.append(('fontsFolder', request.fonts_folder))  # noqa: E501

        header_params = {}

        form_params = []

        body_params = None

        files = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['multipart/form-data'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/slides/{name}/slides/{slideIndex}/notesSlide/shapes/{shapeIndex}/saveAs/{format}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=files,
            response_type='file',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_notes_slide_shapes(self, request, **kwargs):  # noqa: E501
        """Read slide shapes or shape info.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.get_notes_slide_shapes(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param get_notes_slide_shapesRequest request: get_notes_slide_shapes request object
        :return: ShapeListResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('is_async'):
            return self.get_notes_slide_shapes_with_http_info(request, **kwargs)  # noqa: E501
        else:
            (data) = self.get_notes_slide_shapes_with_http_info(request, **kwargs)  # noqa: E501
            return data

    def get_notes_slide_shapes_with_http_info(self, request, **kwargs):  # noqa: E501
        """Read slide shapes or shape info.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.get_notes_slide_shapes_with_http_info(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param get_notes_slide_shapesRequest request: get_notes_slide_shapes request object
        :return: ShapeListResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = []  # noqa: E501
        all_params.append('is_async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_notes_slide_shapes" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if not request.name:
            raise ValueError("Missing the required parameter `request.name` when calling `get_notes_slide_shapes`")  # noqa: E501
        # verify the required parameter 'slide_index' is set
        if not request.slide_index:
            raise ValueError("Missing the required parameter `request.slide_index` when calling `get_notes_slide_shapes`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        path_params['name'] = request.name  # noqa: E501
        path_params['slideIndex'] = request.slide_index  # noqa: E501
        path_params['path'] = request.path  # noqa: E501

        query_params = []
        if request.password:
            query_params.append(('password', request.password))  # noqa: E501
        if request.folder:
            query_params.append(('folder', request.folder))  # noqa: E501
        if request.storage:
            query_params.append(('storage', request.storage))  # noqa: E501

        header_params = {}

        form_params = []

        body_params = None

        files = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/slides/{name}/slides/{slideIndex}/notesSlide/shapes/{path}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=files,
            response_type='ShapeListResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def post_notes_slide_add_new_paragraph(self, request, **kwargs):  # noqa: E501
        """Creates new paragraph.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.post_notes_slide_add_new_paragraph(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param post_notes_slide_add_new_paragraphRequest request: post_notes_slide_add_new_paragraph request object
        :return: ParagraphResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('is_async'):
            return self.post_notes_slide_add_new_paragraph_with_http_info(request, **kwargs)  # noqa: E501
        else:
            (data) = self.post_notes_slide_add_new_paragraph_with_http_info(request, **kwargs)  # noqa: E501
            return data

    def post_notes_slide_add_new_paragraph_with_http_info(self, request, **kwargs):  # noqa: E501
        """Creates new paragraph.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.post_notes_slide_add_new_paragraph_with_http_info(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param post_notes_slide_add_new_paragraphRequest request: post_notes_slide_add_new_paragraph request object
        :return: ParagraphResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = []  # noqa: E501
        all_params.append('is_async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_notes_slide_add_new_paragraph" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if not request.name:
            raise ValueError("Missing the required parameter `request.name` when calling `post_notes_slide_add_new_paragraph`")  # noqa: E501
        # verify the required parameter 'slide_index' is set
        if not request.slide_index:
            raise ValueError("Missing the required parameter `request.slide_index` when calling `post_notes_slide_add_new_paragraph`")  # noqa: E501
        # verify the required parameter 'shape_index' is set
        if not request.shape_index:
            raise ValueError("Missing the required parameter `request.shape_index` when calling `post_notes_slide_add_new_paragraph`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        path_params['name'] = request.name  # noqa: E501
        path_params['slideIndex'] = request.slide_index  # noqa: E501
        path_params['path'] = request.path  # noqa: E501
        path_params['shapeIndex'] = request.shape_index  # noqa: E501

        query_params = []
        if request.password:
            query_params.append(('password', request.password))  # noqa: E501
        if request.folder:
            query_params.append(('folder', request.folder))  # noqa: E501
        if request.storage:
            query_params.append(('storage', request.storage))  # noqa: E501
        if request.position:
            query_params.append(('position', request.position))  # noqa: E501

        header_params = {}

        form_params = []

        body_params = None
        if request.dto:
            body_params = request.dto

        files = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/slides/{name}/slides/{slideIndex}/notesSlide/shapes/{path}/{shapeIndex}/paragraphs', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=files,
            response_type='ParagraphResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def post_notes_slide_add_new_portion(self, request, **kwargs):  # noqa: E501
        """Creates new portion.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.post_notes_slide_add_new_portion(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param post_notes_slide_add_new_portionRequest request: post_notes_slide_add_new_portion request object
        :return: PortionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('is_async'):
            return self.post_notes_slide_add_new_portion_with_http_info(request, **kwargs)  # noqa: E501
        else:
            (data) = self.post_notes_slide_add_new_portion_with_http_info(request, **kwargs)  # noqa: E501
            return data

    def post_notes_slide_add_new_portion_with_http_info(self, request, **kwargs):  # noqa: E501
        """Creates new portion.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.post_notes_slide_add_new_portion_with_http_info(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param post_notes_slide_add_new_portionRequest request: post_notes_slide_add_new_portion request object
        :return: PortionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = []  # noqa: E501
        all_params.append('is_async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_notes_slide_add_new_portion" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if not request.name:
            raise ValueError("Missing the required parameter `request.name` when calling `post_notes_slide_add_new_portion`")  # noqa: E501
        # verify the required parameter 'slide_index' is set
        if not request.slide_index:
            raise ValueError("Missing the required parameter `request.slide_index` when calling `post_notes_slide_add_new_portion`")  # noqa: E501
        # verify the required parameter 'shape_index' is set
        if not request.shape_index:
            raise ValueError("Missing the required parameter `request.shape_index` when calling `post_notes_slide_add_new_portion`")  # noqa: E501
        # verify the required parameter 'paragraph_index' is set
        if not request.paragraph_index:
            raise ValueError("Missing the required parameter `request.paragraph_index` when calling `post_notes_slide_add_new_portion`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        path_params['name'] = request.name  # noqa: E501
        path_params['slideIndex'] = request.slide_index  # noqa: E501
        path_params['path'] = request.path  # noqa: E501
        path_params['shapeIndex'] = request.shape_index  # noqa: E501
        path_params['paragraphIndex'] = request.paragraph_index  # noqa: E501

        query_params = []
        if request.password:
            query_params.append(('password', request.password))  # noqa: E501
        if request.folder:
            query_params.append(('folder', request.folder))  # noqa: E501
        if request.storage:
            query_params.append(('storage', request.storage))  # noqa: E501
        if request.position:
            query_params.append(('position', request.position))  # noqa: E501

        header_params = {}

        form_params = []

        body_params = None
        if request.dto:
            body_params = request.dto

        files = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/slides/{name}/slides/{slideIndex}/notesSlide/shapes/{path}/{shapeIndex}/paragraphs/{paragraphIndex}/portions', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=files,
            response_type='PortionResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def post_notes_slide_add_new_shape(self, request, **kwargs):  # noqa: E501
        """Creates new shape.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.post_notes_slide_add_new_shape(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param post_notes_slide_add_new_shapeRequest request: post_notes_slide_add_new_shape request object
        :return: ShapeResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('is_async'):
            return self.post_notes_slide_add_new_shape_with_http_info(request, **kwargs)  # noqa: E501
        else:
            (data) = self.post_notes_slide_add_new_shape_with_http_info(request, **kwargs)  # noqa: E501
            return data

    def post_notes_slide_add_new_shape_with_http_info(self, request, **kwargs):  # noqa: E501
        """Creates new shape.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.post_notes_slide_add_new_shape_with_http_info(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param post_notes_slide_add_new_shapeRequest request: post_notes_slide_add_new_shape request object
        :return: ShapeResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = []  # noqa: E501
        all_params.append('is_async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_notes_slide_add_new_shape" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if not request.name:
            raise ValueError("Missing the required parameter `request.name` when calling `post_notes_slide_add_new_shape`")  # noqa: E501
        # verify the required parameter 'slide_index' is set
        if not request.slide_index:
            raise ValueError("Missing the required parameter `request.slide_index` when calling `post_notes_slide_add_new_shape`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        path_params['name'] = request.name  # noqa: E501
        path_params['slideIndex'] = request.slide_index  # noqa: E501
        path_params['path'] = request.path  # noqa: E501

        query_params = []
        if request.password:
            query_params.append(('password', request.password))  # noqa: E501
        if request.folder:
            query_params.append(('folder', request.folder))  # noqa: E501
        if request.storage:
            query_params.append(('storage', request.storage))  # noqa: E501
        if request.shape_to_clone:
            query_params.append(('shapeToClone', request.shape_to_clone))  # noqa: E501
        if request.position:
            query_params.append(('position', request.position))  # noqa: E501

        header_params = {}

        form_params = []

        body_params = None
        if request.dto:
            body_params = request.dto

        files = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/slides/{name}/slides/{slideIndex}/notesSlide/shapes/{path}', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=files,
            response_type='ShapeResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def post_notes_slide_shape_save_as(self, request, **kwargs):  # noqa: E501
        """Render shape to specified picture format.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.post_notes_slide_shape_save_as(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param post_notes_slide_shape_save_asRequest request: post_notes_slide_shape_save_as request object
        :return: file
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('is_async'):
            return self.post_notes_slide_shape_save_as_with_http_info(request, **kwargs)  # noqa: E501
        else:
            (data) = self.post_notes_slide_shape_save_as_with_http_info(request, **kwargs)  # noqa: E501
            return data

    def post_notes_slide_shape_save_as_with_http_info(self, request, **kwargs):  # noqa: E501
        """Render shape to specified picture format.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.post_notes_slide_shape_save_as_with_http_info(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param post_notes_slide_shape_save_asRequest request: post_notes_slide_shape_save_as request object
        :return: file
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = []  # noqa: E501
        all_params.append('is_async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_notes_slide_shape_save_as" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if not request.name:
            raise ValueError("Missing the required parameter `request.name` when calling `post_notes_slide_shape_save_as`")  # noqa: E501
        # verify the required parameter 'slide_index' is set
        if not request.slide_index:
            raise ValueError("Missing the required parameter `request.slide_index` when calling `post_notes_slide_shape_save_as`")  # noqa: E501
        # verify the required parameter 'shape_index' is set
        if not request.shape_index:
            raise ValueError("Missing the required parameter `request.shape_index` when calling `post_notes_slide_shape_save_as`")  # noqa: E501
        # verify the required parameter 'format' is set
        if not request.format:
            raise ValueError("Missing the required parameter `request.format` when calling `post_notes_slide_shape_save_as`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        path_params['name'] = request.name  # noqa: E501
        path_params['slideIndex'] = request.slide_index  # noqa: E501
        path_params['shapeIndex'] = request.shape_index  # noqa: E501
        path_params['format'] = request.format  # noqa: E501

        query_params = []
        if request.password:
            query_params.append(('password', request.password))  # noqa: E501
        if request.folder:
            query_params.append(('folder', request.folder))  # noqa: E501
        if request.storage:
            query_params.append(('storage', request.storage))  # noqa: E501
        if request.scale_x:
            query_params.append(('scaleX', request.scale_x))  # noqa: E501
        if request.scale_y:
            query_params.append(('scaleY', request.scale_y))  # noqa: E501
        if request.bounds:
            query_params.append(('bounds', request.bounds))  # noqa: E501
        if request.out_path:
            query_params.append(('outPath', request.out_path))  # noqa: E501
        if request.fonts_folder:
            query_params.append(('fontsFolder', request.fonts_folder))  # noqa: E501

        header_params = {}

        form_params = []

        body_params = None
        if request.options:
            body_params = request.options

        files = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['multipart/form-data'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/slides/{name}/slides/{slideIndex}/notesSlide/shapes/{shapeIndex}/saveAs/{format}', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=files,
            response_type='file',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def put_update_notes_slide_shape(self, request, **kwargs):  # noqa: E501
        """Updates shape properties.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.put_update_notes_slide_shape(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param put_update_notes_slide_shapeRequest request: put_update_notes_slide_shape request object
        :return: ShapeResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('is_async'):
            return self.put_update_notes_slide_shape_with_http_info(request, **kwargs)  # noqa: E501
        else:
            (data) = self.put_update_notes_slide_shape_with_http_info(request, **kwargs)  # noqa: E501
            return data

    def put_update_notes_slide_shape_with_http_info(self, request, **kwargs):  # noqa: E501
        """Updates shape properties.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.put_update_notes_slide_shape_with_http_info(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param put_update_notes_slide_shapeRequest request: put_update_notes_slide_shape request object
        :return: ShapeResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = []  # noqa: E501
        all_params.append('is_async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method put_update_notes_slide_shape" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if not request.name:
            raise ValueError("Missing the required parameter `request.name` when calling `put_update_notes_slide_shape`")  # noqa: E501
        # verify the required parameter 'slide_index' is set
        if not request.slide_index:
            raise ValueError("Missing the required parameter `request.slide_index` when calling `put_update_notes_slide_shape`")  # noqa: E501
        # verify the required parameter 'shape_index' is set
        if not request.shape_index:
            raise ValueError("Missing the required parameter `request.shape_index` when calling `put_update_notes_slide_shape`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        path_params['name'] = request.name  # noqa: E501
        path_params['slideIndex'] = request.slide_index  # noqa: E501
        path_params['path'] = request.path  # noqa: E501
        path_params['shapeIndex'] = request.shape_index  # noqa: E501

        query_params = []
        if request.password:
            query_params.append(('password', request.password))  # noqa: E501
        if request.folder:
            query_params.append(('folder', request.folder))  # noqa: E501
        if request.storage:
            query_params.append(('storage', request.storage))  # noqa: E501

        header_params = {}

        form_params = []

        body_params = None
        if request.dto:
            body_params = request.dto

        files = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/slides/{name}/slides/{slideIndex}/notesSlide/shapes/{path}/{shapeIndex}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=files,
            response_type='ShapeResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def put_update_notes_slide_shape_paragraph(self, request, **kwargs):  # noqa: E501
        """Updates shape properties.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.put_update_notes_slide_shape_paragraph(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param put_update_notes_slide_shape_paragraphRequest request: put_update_notes_slide_shape_paragraph request object
        :return: ParagraphResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('is_async'):
            return self.put_update_notes_slide_shape_paragraph_with_http_info(request, **kwargs)  # noqa: E501
        else:
            (data) = self.put_update_notes_slide_shape_paragraph_with_http_info(request, **kwargs)  # noqa: E501
            return data

    def put_update_notes_slide_shape_paragraph_with_http_info(self, request, **kwargs):  # noqa: E501
        """Updates shape properties.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.put_update_notes_slide_shape_paragraph_with_http_info(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param put_update_notes_slide_shape_paragraphRequest request: put_update_notes_slide_shape_paragraph request object
        :return: ParagraphResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = []  # noqa: E501
        all_params.append('is_async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method put_update_notes_slide_shape_paragraph" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if not request.name:
            raise ValueError("Missing the required parameter `request.name` when calling `put_update_notes_slide_shape_paragraph`")  # noqa: E501
        # verify the required parameter 'slide_index' is set
        if not request.slide_index:
            raise ValueError("Missing the required parameter `request.slide_index` when calling `put_update_notes_slide_shape_paragraph`")  # noqa: E501
        # verify the required parameter 'shape_index' is set
        if not request.shape_index:
            raise ValueError("Missing the required parameter `request.shape_index` when calling `put_update_notes_slide_shape_paragraph`")  # noqa: E501
        # verify the required parameter 'paragraph_index' is set
        if not request.paragraph_index:
            raise ValueError("Missing the required parameter `request.paragraph_index` when calling `put_update_notes_slide_shape_paragraph`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        path_params['name'] = request.name  # noqa: E501
        path_params['slideIndex'] = request.slide_index  # noqa: E501
        path_params['path'] = request.path  # noqa: E501
        path_params['shapeIndex'] = request.shape_index  # noqa: E501
        path_params['paragraphIndex'] = request.paragraph_index  # noqa: E501

        query_params = []
        if request.password:
            query_params.append(('password', request.password))  # noqa: E501
        if request.folder:
            query_params.append(('folder', request.folder))  # noqa: E501
        if request.storage:
            query_params.append(('storage', request.storage))  # noqa: E501

        header_params = {}

        form_params = []

        body_params = None
        if request.dto:
            body_params = request.dto

        files = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/slides/{name}/slides/{slideIndex}/notesSlide/shapes/{path}/{shapeIndex}/paragraphs/{paragraphIndex}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=files,
            response_type='ParagraphResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def put_update_notes_slide_shape_portion(self, request, **kwargs):  # noqa: E501
        """Updates shape properties.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.put_update_notes_slide_shape_portion(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param put_update_notes_slide_shape_portionRequest request: put_update_notes_slide_shape_portion request object
        :return: PortionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('is_async'):
            return self.put_update_notes_slide_shape_portion_with_http_info(request, **kwargs)  # noqa: E501
        else:
            (data) = self.put_update_notes_slide_shape_portion_with_http_info(request, **kwargs)  # noqa: E501
            return data

    def put_update_notes_slide_shape_portion_with_http_info(self, request, **kwargs):  # noqa: E501
        """Updates shape properties.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass is_async=True
        >>> thread = api.put_update_notes_slide_shape_portion_with_http_info(request, is_async=True)
        >>> result = thread.get()

        :param is_async bool
        :param put_update_notes_slide_shape_portionRequest request: put_update_notes_slide_shape_portion request object
        :return: PortionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = []  # noqa: E501
        all_params.append('is_async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method put_update_notes_slide_shape_portion" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if not request.name:
            raise ValueError("Missing the required parameter `request.name` when calling `put_update_notes_slide_shape_portion`")  # noqa: E501
        # verify the required parameter 'slide_index' is set
        if not request.slide_index:
            raise ValueError("Missing the required parameter `request.slide_index` when calling `put_update_notes_slide_shape_portion`")  # noqa: E501
        # verify the required parameter 'shape_index' is set
        if not request.shape_index:
            raise ValueError("Missing the required parameter `request.shape_index` when calling `put_update_notes_slide_shape_portion`")  # noqa: E501
        # verify the required parameter 'paragraph_index' is set
        if not request.paragraph_index:
            raise ValueError("Missing the required parameter `request.paragraph_index` when calling `put_update_notes_slide_shape_portion`")  # noqa: E501
        # verify the required parameter 'portion_index' is set
        if not request.portion_index:
            raise ValueError("Missing the required parameter `request.portion_index` when calling `put_update_notes_slide_shape_portion`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        path_params['name'] = request.name  # noqa: E501
        path_params['slideIndex'] = request.slide_index  # noqa: E501
        path_params['path'] = request.path  # noqa: E501
        path_params['shapeIndex'] = request.shape_index  # noqa: E501
        path_params['paragraphIndex'] = request.paragraph_index  # noqa: E501
        path_params['portionIndex'] = request.portion_index  # noqa: E501

        query_params = []
        if request.password:
            query_params.append(('password', request.password))  # noqa: E501
        if request.folder:
            query_params.append(('folder', request.folder))  # noqa: E501
        if request.storage:
            query_params.append(('storage', request.storage))  # noqa: E501

        header_params = {}

        form_params = []

        body_params = None
        if request.dto:
            body_params = request.dto

        files = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/slides/{name}/slides/{slideIndex}/notesSlide/shapes/{path}/{shapeIndex}/paragraphs/{paragraphIndex}/portions/{portionIndex}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=files,
            response_type='PortionResponse',  # noqa: E501
            auth_settings=auth_settings,
            is_async=params.get('is_async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
