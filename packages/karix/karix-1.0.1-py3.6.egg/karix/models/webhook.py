# coding: utf-8

"""
    karix api

    # Overview  Karix API lets you interact with the Karix platform. It allows you to query your account, set up webhooks, send messages and buy phone numbers.  # API and Clients Versioning  Karix APIs are versioned using the format vX.Y where X is the major version number and Y is minor. All minor version changes are backwards compatible but major releases are not. Please be careful when upgrading.  A new user account is pinned to the latest version at the time of first request. By default every request sent Karix is processed using that version, even if there have been subsequent breaking changes. This is done to prevent existing user applications from breaking. You can change the pinned version for your account using the account dashboard. The default API version can be overridden by specifying the header `api-version`. Note: Specifying this value will not change your pinned version for other calls.  Karix also provides HTTP API clients for all major languages. Release versions of these clients correspond to their API Version supported. Client version vX.Y.Z supports API version vX.Y. HTTP Clients are configured to use `api-version` header for that client version. When using official Karix HTTP Clients only, you dont need to concern yourself with pinned version. To upgrade your API version simply update the client.  # Common Request Structures  All Karix APIs follow a common REST format with the following resources:   - account   - message   - webhook   - number  ## Creating a resource To create a resource send a `POST` request with the desired parameters in a JSON object to `/<resource>/` url. A successful response will contain the details of the single resource created with HTTP status code `201 Created`. Note: An exception to this is the `Create Message` API which is a bulk API and returns       a list of message records.  ## Fetching a resource To fetch a resource by its Unique ID send a `GET` request to `/<resource>/<uid>/` where `uid` is the Alphanumeric Unique ID of the resource. A successful response will contain the details of the single resource fetched with HTTP status code `200 OK`  ## Editing a resource To edit certain parameters of a resource send a `PATCH` request to `/<resource>/<uid>/` where `uid` is the Alphanumeric Unique ID of the resource, with a JSON object containing only the parameters which need to be updated. Edit resource APIs generally have no required parameters. A successful response will contain all the details of the single resource after editing.  ## Deleting a resource To delete a resource send a `DELETE` request to `/<resource>/<uid>/` where `uid` is the Alphanumeric Unique ID of the resource. A successful response will return HTTP status code `204 No Content` with no body.  ## Fetching a list of resources To fetch a list of resources send a `GET` request to `/<resource>/` with filters as GET parameters. A successful response will contain a list of filtered paginated objects with HTTP status code `200 OK`.  ### Pagination Pagination for list APIs are controlled using GET parameters:   - `limit`: Number of objects to be returned   - `offset`: Number of objects to skip before collecting the output list.  # Common Response Structures  All Karix APIs follow some common respose structures.  ## Success Responses  ### Single Resource Response  Responses returning a single object will have the following keys | Key           | Child Key     | Description                               | |:------------- |:------------- |:----------------------------------------- | | meta          |               | Meta Details about request and response   | |               | request_uuid  | Unique request identifier                 | | data          |               | Details of the object                     |  ### List Resource Response  Responses returning a list of objects will have the following keys | Key           | Child Key     | Description                               | |:------------- |:------------- |:----------------------------------------- | | meta          |               | Meta Details about request and response   | |               | request_uuid  | Unique request identifier                 | |               | previous      | Link to the previous page of the list     | |               | next          | Link to the next page of the list         | |               | count         | Total number of objects over all pages    | |               | limit         | Limit the API was requested with          | |               | offset        | Page Offset the API was requested with    | | objects       |               | List of objects with details              |  ## Error Responses  ### Validation Error Response  Responses for requests which failed due to validation errors will have the follwing keys: | Key           | Child Key     | Description                                | |:------------- |:------------- |:------------------------------------------ | | meta          |               | Meta Details about request and response    | |               | request_uuid  | Unique request identifier                  | | error         |               | Details for the error                      | |               | message       | Error message                              | |               | param         | (Optional) parameter this error relates to |  Validation error responses will return HTTP Status Code `400 Bad Request`  ### Insufficient Balance Response  Some requests will require to consume account credits. In case of insufficient balance the following keys will be returned: | Key           | Child Key     | Description                               | |:------------- |:------------- |:----------------------------------------- | | meta          |               | Meta Details about request and response   | |               | request_uuid  | Unique request identifier                 | | error         |               | Details for the error                     | |               | message       | `Insufficient Balance`                    |  Insufficient balance response will return HTTP Status Code `402 Payment Required`   # noqa: E501

    OpenAPI spec version: 1.0
    Contact: support@karix.io
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from karix.models.edit_webhook import EditWebhook  # noqa: F401,E501


class Webhook(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'sms_notification_url': 'str',
        'sms_notification_method': 'str',
        'sms_notification_fallback_url': 'str',
        'sms_notification_fallback_method': 'str',
        'name': 'str',
        'uid': 'str',
        'created_time': 'datetime',
        'updated_time': 'datetime',
        'account_uid': 'str'
    }

    attribute_map = {
        'sms_notification_url': 'sms_notification_url',
        'sms_notification_method': 'sms_notification_method',
        'sms_notification_fallback_url': 'sms_notification_fallback_url',
        'sms_notification_fallback_method': 'sms_notification_fallback_method',
        'name': 'name',
        'uid': 'uid',
        'created_time': 'created_time',
        'updated_time': 'updated_time',
        'account_uid': 'account_uid'
    }

    def __init__(self, sms_notification_url=None, sms_notification_method=None, sms_notification_fallback_url=None, sms_notification_fallback_method=None, name=None, uid=None, created_time=None, updated_time=None, account_uid=None):  # noqa: E501
        """Webhook - a model defined in Swagger"""  # noqa: E501

        self._sms_notification_url = None
        self._sms_notification_method = None
        self._sms_notification_fallback_url = None
        self._sms_notification_fallback_method = None
        self._name = None
        self._uid = None
        self._created_time = None
        self._updated_time = None
        self._account_uid = None
        self.discriminator = None

        if sms_notification_url is not None:
            self.sms_notification_url = sms_notification_url
        if sms_notification_method is not None:
            self.sms_notification_method = sms_notification_method
        if sms_notification_fallback_url is not None:
            self.sms_notification_fallback_url = sms_notification_fallback_url
        if sms_notification_fallback_method is not None:
            self.sms_notification_fallback_method = sms_notification_fallback_method
        if name is not None:
            self.name = name
        if uid is not None:
            self.uid = uid
        if created_time is not None:
            self.created_time = created_time
        if updated_time is not None:
            self.updated_time = updated_time
        if account_uid is not None:
            self.account_uid = account_uid

    @property
    def sms_notification_url(self):
        """Gets the sms_notification_url of this Webhook.  # noqa: E501

        API url to notify in case of inbound message  # noqa: E501

        :return: The sms_notification_url of this Webhook.  # noqa: E501
        :rtype: str
        """
        return self._sms_notification_url

    @sms_notification_url.setter
    def sms_notification_url(self, sms_notification_url):
        """Sets the sms_notification_url of this Webhook.

        API url to notify in case of inbound message  # noqa: E501

        :param sms_notification_url: The sms_notification_url of this Webhook.  # noqa: E501
        :type: str
        """

        self._sms_notification_url = sms_notification_url

    @property
    def sms_notification_method(self):
        """Gets the sms_notification_method of this Webhook.  # noqa: E501

        HTTP method to use for notifying API url in case of inbound message  # noqa: E501

        :return: The sms_notification_method of this Webhook.  # noqa: E501
        :rtype: str
        """
        return self._sms_notification_method

    @sms_notification_method.setter
    def sms_notification_method(self, sms_notification_method):
        """Sets the sms_notification_method of this Webhook.

        HTTP method to use for notifying API url in case of inbound message  # noqa: E501

        :param sms_notification_method: The sms_notification_method of this Webhook.  # noqa: E501
        :type: str
        """

        self._sms_notification_method = sms_notification_method

    @property
    def sms_notification_fallback_url(self):
        """Gets the sms_notification_fallback_url of this Webhook.  # noqa: E501

        In case the service for `sms_notification_url` is down Karix will hit the fallback url with the incoming message details   # noqa: E501

        :return: The sms_notification_fallback_url of this Webhook.  # noqa: E501
        :rtype: str
        """
        return self._sms_notification_fallback_url

    @sms_notification_fallback_url.setter
    def sms_notification_fallback_url(self, sms_notification_fallback_url):
        """Sets the sms_notification_fallback_url of this Webhook.

        In case the service for `sms_notification_url` is down Karix will hit the fallback url with the incoming message details   # noqa: E501

        :param sms_notification_fallback_url: The sms_notification_fallback_url of this Webhook.  # noqa: E501
        :type: str
        """

        self._sms_notification_fallback_url = sms_notification_fallback_url

    @property
    def sms_notification_fallback_method(self):
        """Gets the sms_notification_fallback_method of this Webhook.  # noqa: E501

        HTTP method to use for fallback notification url  # noqa: E501

        :return: The sms_notification_fallback_method of this Webhook.  # noqa: E501
        :rtype: str
        """
        return self._sms_notification_fallback_method

    @sms_notification_fallback_method.setter
    def sms_notification_fallback_method(self, sms_notification_fallback_method):
        """Sets the sms_notification_fallback_method of this Webhook.

        HTTP method to use for fallback notification url  # noqa: E501

        :param sms_notification_fallback_method: The sms_notification_fallback_method of this Webhook.  # noqa: E501
        :type: str
        """

        self._sms_notification_fallback_method = sms_notification_fallback_method

    @property
    def name(self):
        """Gets the name of this Webhook.  # noqa: E501

        Display name of the webhook  # noqa: E501

        :return: The name of this Webhook.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Webhook.

        Display name of the webhook  # noqa: E501

        :param name: The name of this Webhook.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def uid(self):
        """Gets the uid of this Webhook.  # noqa: E501

        Unique ID of the webhook  # noqa: E501

        :return: The uid of this Webhook.  # noqa: E501
        :rtype: str
        """
        return self._uid

    @uid.setter
    def uid(self, uid):
        """Sets the uid of this Webhook.

        Unique ID of the webhook  # noqa: E501

        :param uid: The uid of this Webhook.  # noqa: E501
        :type: str
        """

        self._uid = uid

    @property
    def created_time(self):
        """Gets the created_time of this Webhook.  # noqa: E501

        Date when this webhook was created  # noqa: E501

        :return: The created_time of this Webhook.  # noqa: E501
        :rtype: datetime
        """
        return self._created_time

    @created_time.setter
    def created_time(self, created_time):
        """Sets the created_time of this Webhook.

        Date when this webhook was created  # noqa: E501

        :param created_time: The created_time of this Webhook.  # noqa: E501
        :type: datetime
        """

        self._created_time = created_time

    @property
    def updated_time(self):
        """Gets the updated_time of this Webhook.  # noqa: E501

        Date when this webhook was last updated  # noqa: E501

        :return: The updated_time of this Webhook.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_time

    @updated_time.setter
    def updated_time(self, updated_time):
        """Sets the updated_time of this Webhook.

        Date when this webhook was last updated  # noqa: E501

        :param updated_time: The updated_time of this Webhook.  # noqa: E501
        :type: datetime
        """

        self._updated_time = updated_time

    @property
    def account_uid(self):
        """Gets the account_uid of this Webhook.  # noqa: E501

        UID of Account which created this webhook  # noqa: E501

        :return: The account_uid of this Webhook.  # noqa: E501
        :rtype: str
        """
        return self._account_uid

    @account_uid.setter
    def account_uid(self, account_uid):
        """Sets the account_uid of this Webhook.

        UID of Account which created this webhook  # noqa: E501

        :param account_uid: The account_uid of this Webhook.  # noqa: E501
        :type: str
        """

        self._account_uid = account_uid

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(Webhook, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Webhook):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
