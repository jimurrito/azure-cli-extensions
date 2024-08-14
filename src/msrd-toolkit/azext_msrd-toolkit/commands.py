# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# pylint: disable=line-too-long
from azure.cli.core.commands import CliCommandType
from azext_msrd-toolkit._client_factory import cf_msrd-toolkit


def load_command_table(self, _):

    # TODO: Add command type here
    # msrd-toolkit_sdk = CliCommandType(
    #    operations_tmpl='<PATH>.operations#None.{}',
    #    client_factory=cf_msrd-toolkit)


    with self.command_group('msrd-toolkit') as g:
        g.custom_command('create', 'create_msrd-toolkit')
        # g.command('delete', 'delete')
        g.custom_command('list', 'list_msrd-toolkit')
        # g.show_command('show', 'get')
        # g.generic_update_command('update', setter_name='update', custom_func_name='update_msrd-toolkit')


    with self.command_group('msrd-toolkit', is_preview=True):
        pass

