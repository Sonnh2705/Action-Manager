'''
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import bpy

from .prefs import ACTMAN_prefs

from .operators import (
    ACTMAN_OT_set_active_action,
    ACTMAN_OT_remove_action,
    ACTMAN_OT_duplicate_action,
    ACTMAN_OT_set_pin_action,
    ACTMAN_OT_export_manager_ops,
    ACTMAN_OT_move_nla_strip_in_list,
)
from .gui import (
    ACTMAN_PT_action_manager_panel,
    ACTMAN_PT_nla_manager_panel,
    ACTMAN_UL_actions_list,
    ACTMAN_UL_nla_list
)


bl_info = {
    "name": "Action Manager",
    "author": "SONNH",
    "version": (1, 0, 0),
    "blender": (3, 3, 0),
    "location": "Sidebar -> ActionMana",
    "category": "View3D",
    "description": "Tools for manage large amount of actions in a blend file",
}


class ACTMAN_PG_action_manager_settings(bpy.types.PropertyGroup):

    action_list_index: bpy.props.IntProperty(
        name='Action list index',
        description='',
        default=0
    )

    export_list_index: bpy.props.IntProperty(
        name='Action list index',
        description='',
        default=0
    )

    pin_action_1: bpy.props.PointerProperty(
        type=bpy.types.Action,
        name='Pin action 1',
        description='',
    )

    pin_action_2: bpy.props.PointerProperty(
        type=bpy.types.Action,
        name='Pin action 2',
        description='',
    )


classes = (
    ACTMAN_PG_action_manager_settings,
    ACTMAN_prefs,
    ACTMAN_OT_set_active_action,
    ACTMAN_OT_remove_action,
    ACTMAN_OT_duplicate_action,
    ACTMAN_OT_set_pin_action,
    ACTMAN_OT_export_manager_ops,
    ACTMAN_OT_move_nla_strip_in_list,
    ACTMAN_PT_action_manager_panel,
    ACTMAN_PT_nla_manager_panel,
    ACTMAN_UL_actions_list,
    ACTMAN_UL_nla_list
)


def register():

    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.Scene.actman_settings = bpy.props.PointerProperty(
        type=ACTMAN_PG_action_manager_settings,
        name='Action Manager settings',
    )


def unregister():

    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

    del bpy.types.Scene.actman_settings
