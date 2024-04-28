# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#
# Code generated by aaz-dev-tools
# --------------------------------------------------------------------------------------------

# pylint: disable=too-many-lines
# pylint: disable=too-many-statements
# pylint: disable=line-too-long
# pylint: disable=too-many-locals

import os
import sys
import json
import yaml
import requests
from knack.log import get_logger
import chardet
from azure.cli.core.aaz._arg import AAZStrArg
from .command_patches import ImportAPIDefinitionExtension
from .command_patches import ExportAPIDefinitionExtension
from .command_patches import CreateMetadataExtension
from .command_patches import ExportMetadataExtension
from .aaz.latest.apic.metadata import Update as UpdateMetadataSchema

logger = get_logger(__name__)


class ImportSpecificationExtension(ImportAPIDefinitionExtension):
    @classmethod
    def _build_arguments_schema(cls, *args, **kwargs):
        args_schema = super()._build_arguments_schema(*args, **kwargs)
        args_schema.source_profile = AAZStrArg(
            options=["--file-name"],
            help='Name of the file from where to import the spec from.',
            required=False,
            registered=True
        )
        return args_schema

    def pre_operations(self):
        super().pre_operations()
        args = self.ctx.args
        data = None
        value = None

        # Load the JSON file
        if args.source_profile:
            with open(str(args.source_profile), 'rb') as f:
                data = f.read()
                result = chardet.detect(data)
                encoding = result['encoding']

            if str(args.source_profile).endswith('.yaml') or str(args.source_profile).endswith('.yml'):
                with open(str(args.source_profile), 'r', encoding=encoding) as f:
                    content = f.read()
                    data = yaml.safe_load(content)
                    if data:
                        value = content

            if (str(args.source_profile).endswith('.json')):
                with open(str(args.source_profile), 'r', encoding=encoding) as f:
                    content = f.read()
                    data = json.loads(content)
                    if data:
                        value = content

        # If any of the fields are None, get them from self.args
        if value is None:
            value = args.value

        # Reassign the values to self.args
        args.value = value

        # Check the size of 'value' if format is inline and raise error if value is greater than 3 mb
        if args.format == 'inline':
            value_size_bytes = sys.getsizeof(args.value)
            value_size_mb = value_size_bytes / (1024 * 1024)  # Convert bytes to megabytes
            if value_size_mb > 3:
                logger.error('The size of "value" is greater than 3 MB. '
                             'Please use --format "url" to import the specification from a URL for size greater than 3 mb.')


class ExportSpecificationExtension(ExportAPIDefinitionExtension):

    @classmethod
    def _build_arguments_schema(cls, *args, **kwargs):
        args_schema = super()._build_arguments_schema(*args, **kwargs)
        args_schema.source_profile = AAZStrArg(
            options=["--file-name"],
            help='Name of the file where to export the spec to.',
            required=True,
            registered=True
        )
        return args_schema

    def _output(self, *args, **kwargs):
        result = self.deserialize_output(self.ctx.vars.instance, client_flatten=True)
        arguments = self.ctx.args

        if result:
            response_format = result['format']
            exportedResults = result['value']

            if response_format == 'link':
                logger.warning('Fetching specification from: %s', exportedResults)
                getReponse = requests.get(exportedResults, timeout=10)
                if getReponse.status_code == 200:
                    exportedResults = getReponse.content.decode()
                else:
                    logger.error('Error while fetching the results from the link.'
                                 'Status code: %s', getReponse.status_code)

            if arguments.source_profile:
                try:
                    self.writeResultsToFile(results=exportedResults, file_name=str(arguments.source_profile))
                    logger.warning('Results exported to %s', arguments.source_profile)
                except Exception as e:  # pylint: disable=broad-except
                    logger.error('Error while writing the results to the file. Error: %s', e)
            else:
                logger.error('Please provide the --file-name to exports the results to.')
        else:
            logger.error('No results found.')

    def writeResultsToFile(self, results, file_name):
        if file_name:
            with open(file_name, 'w', encoding='utf-8') as f:
                if os.path.splitext(file_name)[1] == '.json':
                    if isinstance(results, str):
                        results = json.loads(results)
                    json.dump(results, f, indent=4, separators=(',', ':'))
                else:
                    f.write(results)


class CreateMetadataSchemaExtension(CreateMetadataExtension):
    @classmethod
    def _build_arguments_schema(cls, *args, **kwargs):
        args_schema = super()._build_arguments_schema(*args, **kwargs)
        args_schema.source_profile = AAZStrArg(
            options=["--file-name"],
            help='Name of the file from that contains the metadata schema.',
            required=False,
            registered=True
        )
        return args_schema

    def pre_operations(self):
        args = self.ctx.args
        data = None
        value = args.schema

        # Load the JSON file
        if args.source_profile:
            with open(str(args.source_profile), 'rb') as f:
                data = f.read()
                result = chardet.detect(data)
                encoding = result['encoding']

            if os.stat(str(args.source_profile)).st_size == 0:
                raise ValueError('Metadtata schema file is empty. Please provide a valid metadata schema file.')

            with open(str(args.source_profile), 'r', encoding=encoding) as f:
                data = json.load(f)
                if data:
                    value = json.dumps(data)

        # If any of the fields are None, get them from self.args
        if value is None:
            logger.error('Please provide the schema to create the metadata schema'
                         'through --schema option or through --file-name option via a file.')

        # Reassign the values to self.args
        self.ctx.args.schema = value


class UpdateMetadataSchemaExtension(UpdateMetadataSchema):
    @classmethod
    def _build_arguments_schema(cls, *args, **kwargs):
        args_schema = super()._build_arguments_schema(*args, **kwargs)
        args_schema.source_profile = AAZStrArg(
            options=["--file-name"],
            help='Name of the file from that contains the metadata schema.',
            required=False,
            registered=True
        )
        return args_schema

    def pre_operations(self):
        args = self.ctx.args
        data = None
        value = args.schema

        # Load the JSON file
        if args.source_profile:
            with open(str(args.source_profile), 'rb') as f:
                rawdata = f.read()
                result = chardet.detect(rawdata)
                encoding = result['encoding']

            if os.stat(str(args.source_profile)).st_size == 0:
                raise ValueError('Metadtata schema file is empty. Please provide a valid metadata schema file.')

            with open(str(args.source_profile), 'r', encoding=encoding) as f:
                data = json.load(f)
                if data:
                    value = json.dumps(data)

        # If any of the fields are None, get them from self.args
        if value is None:
            logger.error('Please provide the schema to update the metadata schema '
                         'through --schema option or through --file-name option via a file.')

        # Reassign the values to self.args
        self.ctx.args.schema = value


class ExportMetadataSchemaExtension(ExportMetadataExtension):

    @classmethod
    def _build_arguments_schema(cls, *args, **kwargs):
        args_schema = super()._build_arguments_schema(*args, **kwargs)
        args_schema.source_profile = AAZStrArg(
            options=["--file-name"],
            help='Name of the file where to export the metadata schema to.',
            required=True,
            registered=True
        )
        return args_schema

    def _output(self, *args, **kwargs):
        result = self.deserialize_output(self.ctx.vars.instance, client_flatten=True)
        arguments = self.ctx.args

        if result:
            response_format = result['format']
            exportedResults = result['value']

            if response_format == 'link':
                getReponse = requests.get(exportedResults, timeout=10)
                if getReponse.status_code == 200:
                    exportedResults = getReponse.content.decode()
                else:
                    logger.error('Error while fetching the results from the link. Status code: %s', getReponse.status_code)

            if arguments.source_profile:
                try:
                    self.writeResultsToFile(results=exportedResults, file_name=str(arguments.source_profile))
                    logger.warning('Results exported to %s', arguments.source_profile)

                except Exception as e:  # pylint: disable=broad-except
                    logger.error('Error while writing the results to the file. Error: %s', e)
            else:
                logger.error('Please provide the --file-name to exports the results to.')
        else:
            logger.error('No results found.')

    def writeResultsToFile(self, results, file_name):
        if file_name:
            with open(file_name, 'w', encoding='utf-8') as f:
                if os.path.splitext(file_name)[1] == '.json':
                    if isinstance(results, str):
                        results = json.loads(results)
                    json.dump(results, f, indent=4, separators=(',', ':'))
                else:
                    f.write(results)


# Quick Import
def register_apic(cmd, api_location, resource_group, service_name, environment_name=None):

    # Load the JSON file
    if api_location:

        # TODO Future Confirm its a file and not link
        with open(str(api_location), 'rb') as f:
            rawdata = f.read()
            result = chardet.detect(rawdata)
            encoding = result['encoding']

        # TODO - read other file types later
        if str(api_location).endswith('.yaml') or str(api_location).endswith('.yml'):
            with open(str(api_location), 'r', encoding=encoding) as f:
                content = f.read()
                data = yaml.safe_load(content)
                if data:
                    value = content
        if (str(api_location).endswith('.json')):
            with open(str(api_location), 'r', encoding=encoding) as f:
                content = f.read()
                data = json.loads(content)
                if data:
                    value = content

        # If we could not read the file, return error
        if value is None:
            logger.error('Could not load spec file')
            return

        # Check if the first field is 'swagger', 'openapi', or something else and get the definition name and version
        first_key, first_value = list(data.items())[0]
        if first_key in ['swagger', 'openapi']:
            extracted_definition_name = 'openapi'
            extracted_definition_version = first_value.replace(".", "-").lower()
            extracted_api_kind = 'rest'  # TODO determine kind from spec
        else:
            extracted_definition_name = 'default'
            extracted_definition_version = 'v1'
            extracted_api_kind = 'rest'
            # TODO how to determine other kinds - enum={"graphql": "graphql", "grpc": "grpc", "rest": "rest", "soap": "soap", "webhook": "webhook", "websocket": "websocket"}

        # Create API and Create API Version
        info = data['info']
        if info:
            # Create API and Create API Version
            extracted_api_name = _generate_api_id(info.get('title', 'Default-API')).lower()
            extracted_api_description = info.get('description', 'API Description')
            extracted_api_summary = info.get('summary', str(extracted_api_description)[:200])
            extracted_api_title = info.get('title', 'API Title').replace(" ", "-").lower()
            extracted_api_version = info.get('version', 'v1').replace(".", "-").lower()
            extracted_api_version_title = info.get('version', 'v1').replace(".", "-").lower()
            # TODO -Create API Version lifecycle_stage

            # Create API - Get the contact details from info in spec
            contact = info.get('contact')
            if contact:
                extracted_api_contact_email = contact.get('email')
                extracted_api_contact_name = contact.get('name')
                extracted_api_contact_url = contact.get('url')
                contacts = [{'email': extracted_api_contact_email, 'name': extracted_api_contact_name, 'url': extracted_api_contact_url}]
            else:
                contacts = None

            # Create API - Get the license details from info in spec
            licenseDetails = info.get('license')
            if licenseDetails:
                extracted_api_license_identifier = licenseDetails.get('identifier')
                extracted_api_license_name = licenseDetails.get('name')
                extracted_api_license_url = licenseDetails.get('url')
                extracted_api_license = {'identifier': extracted_api_license_identifier, 'name': extracted_api_license_name, 'url': extracted_api_license_url}
            else:
                extracted_api_license = None

            # Create API - Get the terms of service from info in spec
            extracted_api_terms_of_service_value = info.get('termsOfService')
            if extracted_api_terms_of_service_value:
                extracted_api_terms_of_service = {'url': extracted_api_terms_of_service_value}
            else:
                extracted_api_terms_of_service = {'url': None}

            # Create API - Get the external documentation from info in spec
            extracted_api_external_documentation = None
            external_documentation = info.get('externalDocumentation')
            if external_documentation:
                extracted_api_external_documentation_description = external_documentation.get('description')
                extracted_api_external_documentation_title = external_documentation.get('title')
                extracted_api_external_documentation_url = external_documentation.get('url')
                extracted_api_external_documentation = {'description': extracted_api_external_documentation_description, 'title': extracted_api_external_documentation_title, 'url': extracted_api_external_documentation_url}
            else:
                extracted_api_external_documentation = None

            # TODO: Create API - custom-properties
            # "The custom metadata defined for API catalog entities. #1

            # Create API -------------------------------------------------------------------------------------
            from .aaz.latest.apic.api import Create as CreateAPI

            api_args = {
                'api_id': extracted_api_name,
                'resource_group': resource_group,
                'service_name': service_name,
                'workspace_name': 'default',
                'title': extracted_api_title,
                'summary': extracted_api_summary,
                'type': extracted_api_kind,
                'contacts': contacts,
                'license': extracted_api_license,
                'terms_of_service': extracted_api_terms_of_service,
                'external_documentation': extracted_api_external_documentation,
                'description': extracted_api_description,
            }

            CreateAPI(cli_ctx=cmd.cli_ctx)(command_args=api_args)
            logger.warning('API was created successfully')

            # Create API Version -----------------------------------------------------------------------------
            from .aaz.latest.apic.api.version import Create as CreateAPIVersion

            api_version_args = {
                'api_id': extracted_api_name,
                'resource_group': resource_group,
                'service_name': service_name,
                'version_id': extracted_api_version,
                'workspace_name': 'default',
                'lifecycle_stage': 'design',  # TODO: Extract from spec or not pass. was it required?
                'title': extracted_api_version_title
            }

            CreateAPIVersion(cli_ctx=cmd.cli_ctx)(command_args=api_version_args)
            logger.warning('API version was created successfully')

            # Create API Definition -----------------------------------------------------------------------------
            from .aaz.latest.apic.api.definition import Create as CreateAPIDefinition

            api_definition_args = {
                'api_id': extracted_api_name,
                'resource_group': resource_group,
                'service_name': service_name,
                'version_id': extracted_api_version,
                'workspace_name': 'default',
                'definition_id': extracted_definition_name,
                'title': extracted_definition_name,  # TODO Extract from spec
                'description': extracted_api_description,  # TODO Extract from spec
            }

            CreateAPIDefinition(cli_ctx=cmd.cli_ctx)(command_args=api_definition_args)
            logger.warning('API definition was created successfully')

            # Import Specification -----------------------------------------------------------------------------
            from azure.cli.core.commands import LongRunningOperation

            # uses customized ImportSpecificationExtension class
            specification_details = {'name': extracted_definition_name, 'version': extracted_definition_version}
            # TODO format - Link - what if the link is just pasted in the value?
            # TODO format - inline - what if spec is just pasted in the value?
            # TODO - other non json spec formats

            api_specification_args = {
                'resource_group': resource_group,
                'service_name': service_name,
                'workspace_name': 'default',
                'api_id': extracted_api_name,
                'version_id': extracted_api_version,
                'definition_id': extracted_definition_name,
                'format': 'inline',
                'specification': specification_details,  # TODO write the correct spec object
                'source_profile': api_location
            }

            importAPISpecificationResults = ImportSpecificationExtension(cli_ctx=cmd.cli_ctx)(command_args=api_specification_args)
            LongRunningOperation(cmd.cli_ctx)(importAPISpecificationResults)
            logger.warning('API specification was created successfully')

            # Create API Deployment -----------------------------------------------------------------------------
            from .aaz.latest.apic.api.deployment import Create as CreateAPIDeployment
            from .aaz.latest.apic.environment import Show as GetEnvironment

            environment_id = None
            if environment_name:
                # GET Environment ID
                environment_args = {
                    'resource_group': resource_group,
                    'service_name': service_name,
                    'workspace_name': 'default',
                    'environment_id': environment_name
                }

                getEnvironmentResults = GetEnvironment(cli_ctx=cmd.cli_ctx)(command_args=environment_args)
                environment_id = getEnvironmentResults['id']
                # full envId, extract actual envId if to be used later

            servers = data.get('servers')
            if environment_id and servers:
                for server in servers:
                    default_deployment_title = (extracted_api_name + "deployment").replace("-", "")
                    extracted_deployment_name = server.get('name', default_deployment_title).replace(" ", "-")
                    extracted_deployment_title = server.get('title', default_deployment_title).replace(" ", "-")
                    extracted_deployment_description = server.get('description', default_deployment_title)
                    extracted_definition_id = '/workspaces/default/apis/' + extracted_api_name + '/versions/' + extracted_api_version + '/definitions/' + extracted_definition_name
                    extracted_environment_id = '/workspaces/default/environments/' + environment_name
                    extracted_state = server.get('state', 'active')

                    extracted_server_urls = []
                    extracted_server_url = server.get('url')
                    extracted_server_urls.append(extracted_server_url)
                    extracted_server = {'runtime_uri': extracted_server_urls}

                    api_deployment_args = {
                        'resource_group': resource_group,
                        'service_name': service_name,
                        'workspace_name': 'default',
                        'api_id': extracted_api_name,
                        'deployment_id': extracted_deployment_name,
                        'description': extracted_deployment_description,
                        'title': extracted_deployment_title,
                        'definition_id': extracted_definition_id,
                        'environment_id': extracted_environment_id,
                        'server': extracted_server,
                        'state': extracted_state
                        # TODO custom properties
                    }

                    CreateAPIDeployment(cli_ctx=cmd.cli_ctx)(command_args=api_deployment_args)
                    logger.warning('API deployment was created successfully')


def _generate_api_id(title: str) -> str:
    import re
    # Remove invalid characters
    api_id = re.sub('[^a-zA-Z0-9-]', '', title)
    # Remove leading and trailing hyphens
    api_id = api_id.strip('-')
    return api_id
