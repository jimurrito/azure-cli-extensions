# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from knack.util import CLIError


def create_msrd-toolkit(cmd, resource_group_name, msrd-toolkit_name, location=None, tags=None):
    raise CLIError('TODO: Implement `msrd-toolkit create`')


def list_msrd-toolkit(cmd, resource_group_name=None):
    raise CLIError('TODO: Implement `msrd-toolkit list`')


def update_msrd-toolkit(cmd, instance, tags=None):
    with cmd.update_context(instance) as c:
        c.set_param('tags', tags)
    return instance