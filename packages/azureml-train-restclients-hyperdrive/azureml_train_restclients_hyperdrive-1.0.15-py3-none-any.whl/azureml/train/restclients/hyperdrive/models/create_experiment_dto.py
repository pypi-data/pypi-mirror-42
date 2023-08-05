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

from pprint import pformat
from six import iteritems
import re


class CreateExperimentDto(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, description=None, generator_config=None, max_concurrent_jobs=None, max_duration_minutes=None, max_total_jobs=None, name=None, platform=None, platform_config=None, policy_config=None, primary_metric_config=None, study_id=None, user=None):
        """
        CreateExperimentDto - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'description': 'str',
            'generator_config': 'ExperimentDtoGeneratorConfig',
            'max_concurrent_jobs': 'int',
            'max_duration_minutes': 'int',
            'max_total_jobs': 'int',
            'name': 'str',
            'platform': 'str',
            'platform_config': 'object',
            'policy_config': 'ExperimentDtoPolicyConfig',
            'primary_metric_config': 'ExperimentDtoPrimaryMetricConfig',
            'study_id': 'int',
            'user': 'str'
        }

        self.attribute_map = {
            'description': 'description',
            'generator_config': 'generator_config',
            'max_concurrent_jobs': 'max_concurrent_jobs',
            'max_duration_minutes': 'max_duration_minutes',
            'max_total_jobs': 'max_total_jobs',
            'name': 'name',
            'platform': 'platform',
            'platform_config': 'platform_config',
            'policy_config': 'policy_config',
            'primary_metric_config': 'primary_metric_config',
            'study_id': 'study_id',
            'user': 'user'
        }

        self._description = description
        self._generator_config = generator_config
        self._max_concurrent_jobs = max_concurrent_jobs
        self._max_duration_minutes = max_duration_minutes
        self._max_total_jobs = max_total_jobs
        self._name = name
        self._platform = platform
        self._platform_config = platform_config
        self._policy_config = policy_config
        self._primary_metric_config = primary_metric_config
        self._study_id = study_id
        self._user = user

    @property
    def description(self):
        """
        Gets the description of this CreateExperimentDto.


        :return: The description of this CreateExperimentDto.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this CreateExperimentDto.


        :param description: The description of this CreateExperimentDto.
        :type: str
        """

        if not description:
            raise ValueError("Invalid value for `description`, must not be `None`")
        if len(description) > 511:
            raise ValueError("Invalid value for `description`, length must be less than `511`")

        self._description = description

    @property
    def generator_config(self):
        """
        Gets the generator_config of this CreateExperimentDto.


        :return: The generator_config of this CreateExperimentDto.
        :rtype: ExperimentDtoGeneratorConfig
        """
        return self._generator_config

    @generator_config.setter
    def generator_config(self, generator_config):
        """
        Sets the generator_config of this CreateExperimentDto.


        :param generator_config: The generator_config of this CreateExperimentDto.
        :type: ExperimentDtoGeneratorConfig
        """

        self._generator_config = generator_config

    @property
    def max_concurrent_jobs(self):
        """
        Gets the max_concurrent_jobs of this CreateExperimentDto.


        :return: The max_concurrent_jobs of this CreateExperimentDto.
        :rtype: int
        """
        return self._max_concurrent_jobs

    @max_concurrent_jobs.setter
    def max_concurrent_jobs(self, max_concurrent_jobs):
        """
        Sets the max_concurrent_jobs of this CreateExperimentDto.


        :param max_concurrent_jobs: The max_concurrent_jobs of this CreateExperimentDto.
        :type: int
        """

        if not max_concurrent_jobs:
            raise ValueError("Invalid value for `max_concurrent_jobs`, must not be `None`")
        if max_concurrent_jobs > 100.0:
            raise ValueError("Invalid value for `max_concurrent_jobs`, must be a value less than or equal to `100.0`")
        if max_concurrent_jobs < 1.0:
            raise ValueError("Invalid value for `max_concurrent_jobs`, must be a value greater than or equal to `1.0`")

        self._max_concurrent_jobs = max_concurrent_jobs

    @property
    def max_duration_minutes(self):
        """
        Gets the max_duration_minutes of this CreateExperimentDto.


        :return: The max_duration_minutes of this CreateExperimentDto.
        :rtype: int
        """
        return self._max_duration_minutes

    @max_duration_minutes.setter
    def max_duration_minutes(self, max_duration_minutes):
        """
        Sets the max_duration_minutes of this CreateExperimentDto.


        :param max_duration_minutes: The max_duration_minutes of this CreateExperimentDto.
        :type: int
        """

        if not max_duration_minutes:
            raise ValueError("Invalid value for `max_duration_minutes`, must not be `None`")
        if max_duration_minutes > 43200.0:
            raise ValueError("Invalid value for `max_duration_minutes`, must be a value less than or equal to `43200.0`")
        if max_duration_minutes < 1.0:
            raise ValueError("Invalid value for `max_duration_minutes`, must be a value greater than or equal to `1.0`")

        self._max_duration_minutes = max_duration_minutes

    @property
    def max_total_jobs(self):
        """
        Gets the max_total_jobs of this CreateExperimentDto.


        :return: The max_total_jobs of this CreateExperimentDto.
        :rtype: int
        """
        return self._max_total_jobs

    @max_total_jobs.setter
    def max_total_jobs(self, max_total_jobs):
        """
        Sets the max_total_jobs of this CreateExperimentDto.


        :param max_total_jobs: The max_total_jobs of this CreateExperimentDto.
        :type: int
        """

        if not max_total_jobs:
            raise ValueError("Invalid value for `max_total_jobs`, must not be `None`")
        if max_total_jobs > 1000.0:
            raise ValueError("Invalid value for `max_total_jobs`, must be a value less than or equal to `1000.0`")
        if max_total_jobs < 1.0:
            raise ValueError("Invalid value for `max_total_jobs`, must be a value greater than or equal to `1.0`")

        self._max_total_jobs = max_total_jobs

    @property
    def name(self):
        """
        Gets the name of this CreateExperimentDto.


        :return: The name of this CreateExperimentDto.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this CreateExperimentDto.


        :param name: The name of this CreateExperimentDto.
        :type: str
        """

        if not name:
            raise ValueError("Invalid value for `name`, must not be `None`")
        if len(name) > 255:
            raise ValueError("Invalid value for `name`, length must be less than `255`")

        self._name = name

    @property
    def platform(self):
        """
        Gets the platform of this CreateExperimentDto.


        :return: The platform of this CreateExperimentDto.
        :rtype: str
        """
        return self._platform

    @platform.setter
    def platform(self, platform):
        """
        Sets the platform of this CreateExperimentDto.


        :param platform: The platform of this CreateExperimentDto.
        :type: str
        """

        self._platform = platform

    @property
    def platform_config(self):
        """
        Gets the platform_config of this CreateExperimentDto.


        :return: The platform_config of this CreateExperimentDto.
        :rtype: object
        """
        return self._platform_config

    @platform_config.setter
    def platform_config(self, platform_config):
        """
        Sets the platform_config of this CreateExperimentDto.


        :param platform_config: The platform_config of this CreateExperimentDto.
        :type: object
        """

        self._platform_config = platform_config

    @property
    def policy_config(self):
        """
        Gets the policy_config of this CreateExperimentDto.


        :return: The policy_config of this CreateExperimentDto.
        :rtype: ExperimentDtoPolicyConfig
        """
        return self._policy_config

    @policy_config.setter
    def policy_config(self, policy_config):
        """
        Sets the policy_config of this CreateExperimentDto.


        :param policy_config: The policy_config of this CreateExperimentDto.
        :type: ExperimentDtoPolicyConfig
        """

        self._policy_config = policy_config

    @property
    def primary_metric_config(self):
        """
        Gets the primary_metric_config of this CreateExperimentDto.


        :return: The primary_metric_config of this CreateExperimentDto.
        :rtype: ExperimentDtoPrimaryMetricConfig
        """
        return self._primary_metric_config

    @primary_metric_config.setter
    def primary_metric_config(self, primary_metric_config):
        """
        Sets the primary_metric_config of this CreateExperimentDto.


        :param primary_metric_config: The primary_metric_config of this CreateExperimentDto.
        :type: ExperimentDtoPrimaryMetricConfig
        """

        self._primary_metric_config = primary_metric_config

    @property
    def study_id(self):
        """
        Gets the study_id of this CreateExperimentDto.


        :return: The study_id of this CreateExperimentDto.
        :rtype: int
        """
        return self._study_id

    @study_id.setter
    def study_id(self, study_id):
        """
        Sets the study_id of this CreateExperimentDto.


        :param study_id: The study_id of this CreateExperimentDto.
        :type: int
        """

        if not study_id:
            raise ValueError("Invalid value for `study_id`, must not be `None`")
        if study_id < 0.0:
            raise ValueError("Invalid value for `study_id`, must be a value greater than or equal to `0.0`")

        self._study_id = study_id

    @property
    def user(self):
        """
        Gets the user of this CreateExperimentDto.


        :return: The user of this CreateExperimentDto.
        :rtype: str
        """
        return self._user

    @user.setter
    def user(self, user):
        """
        Sets the user of this CreateExperimentDto.


        :param user: The user of this CreateExperimentDto.
        :type: str
        """

        if not user:
            raise ValueError("Invalid value for `user`, must not be `None`")
        if len(user) > 255:
            raise ValueError("Invalid value for `user`, length must be less than `255`")

        self._user = user

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
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

        return result

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
