from typing import Set
import bpy
from bpy.types import Context

from .prefs import prefs


# set active action frame range as scene frame range

def set_frame_range(action):
    data = bpy.data
    scene = bpy.context.scene.name
    frame_start = int(data.actions[action].frame_range[0])
    frame_end = int(data.actions[action].frame_range[1])
    data.scenes[f'{scene}'].frame_start = frame_start  # set scene frame start
    data.scenes[f'{scene}'].frame_end = frame_end  # set scene frame end


# check if active obj has active action or anim data

def is_anim_data_exist():
    obj = bpy.context.view_layer.objects.active
    is_anim_exist = obj.animation_data != None
    is_action_exist = obj.animation_data.action != None if is_anim_exist else False
    return is_anim_exist, is_action_exist


# create anim data for active object with no anim data

def anim_data_create():
    obj = bpy.context.view_layer.objects.active
    if not is_anim_data_exist()[0]:
        obj.animation_data_create()


# set the active action in the action list layout to the active action of
# the active obj everytime the active action of the active obj change

def set_active_in_list():
    scene = bpy.context.scene
    is_active_sel = scene.actman_settings.action_list_index == get_active_action()[0]
    if not is_active_sel:
        scene.actman_settings.action_list_index = get_active_action()[0]


# set the input (index or name) as active action of the active obj

def set_active_action(action_to_set):
    anim_data = bpy.context.view_layer.objects.active.animation_data
    anim_data.action = bpy.data.actions[action_to_set]
    if prefs().match_frame:
        set_frame_range(action_to_set)
    set_active_in_list()
    return anim_data.action.name


# get the index of the active, the next and prev action

def get_active_action():
    data = bpy.data.actions
    active_action = bpy.context.active_object.animation_data.action
    index = bpy.data.actions.keys().index(active_action.name)
    prev_index = index - 1
    next_index = index + 1
    if next_index == len(data):
        next_index = 0
    return index, prev_index, next_index


# remove action

def remove_action(action_to_remove):
    action_data = bpy.data.actions
    action_to_remove_name = action_data[action_to_remove].name
    action_data.remove(action_data[action_to_remove])
    return action_to_remove_name


# swap strip between 2 nla track

def swap_strip(current_index, target_index):

    nla = bpy.context.active_object.animation_data.nla_tracks
    current_strip = nla[current_index].strips[0].action
    target_strip = nla[target_index].strips[0].action

    nla[current_index].strips.remove(nla[current_index].strips[0])
    nla[target_index].strips.remove(nla[target_index].strips[0])

    nla[target_index].name = current_strip.name
    strip = nla[target_index].strips.new(current_strip.name, 0, current_strip)
    strip.select = False

    nla[current_index].name = target_strip.name
    strip = nla[current_index].strips.new(target_strip.name, 0, target_strip)
    strip.select = False


# set the selected action as the active action of the active obj

class ACTMAN_OT_set_active_action(bpy.types.Operator):
    bl_idname = "actman.set_active_action"
    bl_label = "Set active action"
    bl_description = 'Set action as active'

    action_index: bpy.props.IntProperty(
        name='Action list index',
        default=0,
        options={'HIDDEN'}
    )

    options: bpy.props.EnumProperty(
        name='Options',
        items=[
            ('IN LIST', 'In list', 'Set active in list'),
            ('NEXT', 'Next', 'Set next action as active'),
            ('PREV', 'Prev', 'Set prev action as active'),
            ('FIRST', 'First', 'Set first action as active'),
            ('LAST', 'Last', 'Set last action as active'),
            ('PIN 1', 'Pin 1', 'Set pin 1 action as active'),
            ('PIN 2', 'Pin 2', 'Set pin 2 action as active'),
        ]
    )

    @classmethod
    def poll(cls, context):

        return len(bpy.data.actions) > 0

    def execute(self, context):

        anim_data_create()

        match self.options:
            case 'IN LIST':
                index = self.action_index
            case 'NEXT':
                index = (bpy.context.scene.actman_action_list_index + 1
                         if bpy.context.scene.actman_action_list_index < len(bpy.data.actions) - 1
                         else 0
                         )
            case 'PREV':
                index = bpy.context.scene.actman_action_list_index - 1
            case 'FIRST':
                index = 0
            case 'LAST':
                index = len(bpy.data.actions) - 1
            case 'PIN 1':
                index = bpy.context.scene.actman_settings.pin_action_1.name
            case 'PIN 2':
                index = bpy.context.scene.actman_settings.pin_action_2.name

        active_action = set_active_action(index)

        self.report({'INFO'},
                    message=f'Active action set to {active_action}'
                    )

        return {'FINISHED'}


# remove the selected action from the blend file

class ACTMAN_OT_remove_action(bpy.types.Operator):
    bl_idname = "actman.remove_action"
    bl_label = "Remove action"

    action_index: bpy.props.IntProperty(
        name='Action list index',
        options={'HIDDEN'}
    )

    def execute(self, context):

        action_remove = remove_action(self.action_index)
        self.report({'INFO'},
                    message=f'Removed action {action_remove}'
                    )

        return {'FINISHED'}


# duplicate selected action

class ACTMAN_OT_duplicate_action(bpy.types.Operator):
    bl_idname = "actman.duplicate_action"
    bl_label = "Duplicate action"

    action_index: bpy.props.IntProperty(
        name='Action list index',
        options={'HIDDEN'}
    )

    use_active: bpy.props.BoolProperty(
        name='Duplicate active action',
        default=False,
    )

    def execute(self, context):

        if not self.use_active:
            bpy.data.actions[self.action_index].copy()
        else:
            action = bpy.context.active_object.animation_data.action.copy()
            bpy.context.active_object.animation_data.action = action

        return {'FINISHED'}


# pin the selected action

class ACTMAN_OT_set_pin_action(bpy.types.Operator):
    bl_idname = "actman.set_pin_action"
    bl_label = "Set pin action"
    bl_description = 'Set action as pin action'

    options: bpy.props.EnumProperty(
        name='Options',
        items=[
            ('LIST 1', 'List 1', 'Set action at index in list as pin action 1'),
            ('LIST 2', 'List 2', 'Set action at index in list as pin action 2'),
            ('ACTIVE 1', 'Active 1', 'Set active action as pin action 1'),
            ('ACTIVE 2', 'Active 2', 'Set active action as pin action 1')
        ]
    )

    pin_action_1_index: bpy.props.IntProperty(
        name='Pin action 1 index',
        options={'HIDDEN'}
    )

    pin_action_2_index: bpy.props.IntProperty(
        name='Pin action 2 index',
        options={'HIDDEN'}
    )

    def execute(self, context):

        scene = bpy.context.scene

        match self.options:
            case 'LIST 1':
                scene.actman_settings.pin_action_1 = bpy.data.actions[self.pin_action_1_index]
            case 'LIST 2':
                scene.actman_settings.pin_action_2 = bpy.data.actions[self.pin_action_2_index]
            case 'ACTIVE 1':
                scene.actman_settings.pin_action_1 = bpy.context.active_object.animation_data.action
            case 'ACTIVE 2':
                scene.actman_settings.pin_action_2 = bpy.context.active_object.animation_data.action

        return {'FINISHED'}


# operators on for export action

class ACTMAN_OT_export_manager_ops(bpy.types.Operator):
    bl_idname = "actman.export_manager_ops"
    bl_label = "Export manager operators"
    bl_description = 'Operators for export manager'
    bl_options = {'REGISTER'}

    options: bpy.props.EnumProperty(
        name='options',
        items=[
            ('PUSH', 'Push', 'Push action to export slot'),
            ('DEL', 'Delete', 'Delete export slot'),
        ]
    )

    index: bpy.props.IntProperty(
        name='Index',
    )

    def execute(self, context):

        obj = bpy.context.active_object
        action = bpy.data.actions[self.index]

        match self.options:
            case 'DEL':
                obj.animation_data.nla_tracks.remove(obj.animation_data.nla_tracks[self.index])
            case 'PUSH':
                track = obj.animation_data.nla_tracks.new()
                track.name = action.name
                track.strips.new(action.name, 0, action)

        return {'FINISHED'}


class ACTMAN_OT_move_nla_strip_in_list(bpy.types.Operator):
    bl_idname = 'actman.move_strip_in_list'
    bl_label = 'Move strip in list'
    bl_description = 'Move strip in list'
    bl_options = {'UNDO'}

    options: bpy.props.EnumProperty(
        name='Options',
        items=[
            ('UP', 'Up', 'Move strip up'),
            ('DOWN', 'Down', 'Move strip down'),
        ]
    )

    @classmethod
    def poll(cls, context):

        return len(bpy.context.active_object.animation_data.nla_tracks) > 0

    def execute(self, context):

        index = bpy.context.scene.actman_settings.export_list_index

        match self.options:
            case 'UP':
                new_index = index + 1
            case 'DOWN':
                new_index = index - 1

        swap_strip(index, new_index)

        bpy.context.scene.actman_settings.export_list_index = new_index

        return {'FINISHED'}
