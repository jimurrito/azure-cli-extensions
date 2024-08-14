# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from knack.util import CLIError
from azure.cli.command_modules.vm.custom import get_vm

def run_msrd_toolkit(cmd, resource_group, vm_name):
    # debug print
    print(cmd, resource_group, vm_name)
    target_vm = get_vm(cmd, resource_group, vm_name)
    # 
    
    #raise CLIError('TODO: Implement `msrd_toolkit create`')

'''
 def update_msrd_toolkit(cmd, instance, tags=None):
    with cmd.update_context(instance) as c:
        c.set_param('tags', tags)
    return instance
'''