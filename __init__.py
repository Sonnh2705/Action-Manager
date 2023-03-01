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
    ACTMAN_OT_set_active_action, ACTMAN_OT_remove_action,
    ACTMAN_OT_set_pin_action_1, ACTMAN_OT_set_pin_action_2,
    ACTMAN_OT_set_active_as_pin_1, ACTMAN_OT_set_active_as_pin_2,
    ACTMAN_OT_to_pin_action_1, ACTMAN_OT_to_pin_action_2,
    ACTMAN_OT_to_next_action, ACTMAN_OT_to_prev_action,
    ACTMAN_OT_to_first_action, ACTMAN_OT_to_last_action,
)
from .gui import (
    ACTMAN_PT_sidebar_panel,
    ACTMAN_PT_stat,
    ACTMAN_UL_actions_list
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


classes = (
    ACTMAN_prefs,
    ACTMAN_OT_set_active_action,
    ACTMAN_OT_remove_action,
    ACTMAN_OT_set_pin_action_1,
    ACTMAN_OT_set_pin_action_2,
    ACTMAN_OT_set_active_as_pin_1,
    ACTMAN_OT_set_active_as_pin_2,
    ACTMAN_OT_to_pin_action_1,
    ACTMAN_OT_to_pin_action_2,
    ACTMAN_OT_to_next_action,
    ACTMAN_OT_to_prev_action,
    ACTMAN_OT_to_first_action,
    ACTMAN_OT_to_last_action,
    ACTMAN_PT_sidebar_panel,
    ACTMAN_PT_stat,
    ACTMAN_UL_actions_list,
)


def register():

    bpy.types.Scene.actman_action_list_index = bpy.props.IntProperty(
        name='Action list index',
        description='',
        default=0
    )

    bpy.types.Scene.actman_pin_action_1 = bpy.props.PointerProperty(
        type=bpy.types.Action,
        name='Pin action 1 name',
        description='',
    )

    bpy.types.Scene.actman_pin_action_2 = bpy.props.PointerProperty(
        type=bpy.types.Action,
        name='Pin action 2 name',
        description='',
    )

    bpy.types.Scene.actman_gui_param_1 = bpy.props.FloatProperty(
        name='Gui param 1',
        description='',
        default=0,
        min=0
    )

    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():

    del bpy.types.Scene.actman_action_list_index
    del bpy.types.Scene.actman_pin_action_1
    del bpy.types.Scene.actman_pin_action_2
    del bpy.types.Scene.actman_gui_param_1

    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
