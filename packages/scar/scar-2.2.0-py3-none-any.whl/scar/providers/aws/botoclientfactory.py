# Copyright (C) GRyCAP - I3M - UPV
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from scar.providers.aws.clients.apigateway import APIGatewayClient
from scar.providers.aws.clients.batchfunction import BatchClient
from scar.providers.aws.clients.cloudwatchlogs import CloudWatchLogsClient
from scar.providers.aws.clients.iam import IAMClient
from scar.providers.aws.clients.lambdafunction import LambdaClient
from scar.providers.aws.clients.resourcegroups import ResourceGroupsClient
from scar.providers.aws.clients.s3 import S3Client
import scar.utils as utils

class GenericClient(object):

    def __init__(self, aws_properties):
        self.aws_properties = aws_properties

    def get_client_args(self):
        return {'client' : {'region_name' : self.aws_properties['region'] } ,
                'session' : { 'profile_name' : self.aws_properties['boto_profile'] }}
    
    @utils.lazy_property
    def client(self):
        client_name = self.__class__.__name__ + 'Client'
        client = globals()[client_name](**self.get_client_args())
        return client

