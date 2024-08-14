# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.core import AzCommandsLoader

from azext_msrd-toolkit._help import helps  # pylint: disable=unused-import


class Msrd-toolkitCommandsLoader(AzCommandsLoader):

    def __init__(self, cli_ctx=None):
        from azure.cli.core.commands import CliCommandType
        from azext_msrd-toolkit._client_factory import cf_msrd-toolkit
        msrd-toolkit_custom = CliCommandType(
            operations_tmpl='azext_msrd-toolkit.custom#{}',
            client_factory=cf_msrd-toolkit)
        super(Msrd-toolkitCommandsLoader, self).__init__(cli_ctx=cli_ctx,
                                                  custom_command_type=msrd-toolkit_custom)

    def load_command_table(self, args):
        from azext_msrd-toolkit.commands import load_command_table
        load_command_table(self, args)
        return self.command_table

    def load_arguments(self, command):
        from azext_msrd-toolkit._params import load_arguments
        load_arguments(self, command)


COMMAND_LOADER_CLS = Msrd-toolkitCommandsLoader
