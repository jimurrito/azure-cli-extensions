# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
# pylint: disable=line-too-long

from knack.arguments import CLIArgumentType


def load_arguments(self, _):

    from azure.cli.core.commands.parameters import tags_type
    from azure.cli.core.commands.validators import get_default_location_from_resource_group

    with self.argument_context('msrd-collect run') as c:
        c.argument('vm_name', options_list=['--vm-name', '-n'], help='The name of the virtual machine we want to run MSRD-Collect on.')
        c.argument('resource_group', options_list=['--resource-group', '-g'])
        
        

    # with self.argument_context('msrd_toolkit list') as c:
    #     c.argument('msrd_toolkit_name', msrd_toolkit_name_type, id_part=None)
