# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# pylint: disable=line-too-long
# from azure.cli.core.commands import CliCommandType
from azext_msrd_toolkit._client_factory import cf_msrd_toolkit


def load_command_table(self, _):

    # TODO: Add command type here
    # msrd_toolkit_sdk = CliCommandType(
    #    operations_tmpl='<PATH>.operations#None.{}',
    #    client_factory=cf_msrd_toolkit)


    with self.command_group('msrd-collect') as g:
        g.custom_command('run', 'run_msrd_toolkit')


    # with self.command_group('msrd-collect', is_preview=True):
    #    pass

