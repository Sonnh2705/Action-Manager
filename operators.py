import bpy

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
    if is_anim_exist:
        is_action_exist = obj.animation_data.action != None
    else:
        is_action_exist = False
    return is_anim_exist, is_action_exist


# create anim data for active object with no anim data

def anim_data_create():
    obj = bpy.context.view_layer.objects.active
    if not is_anim_data_exist()[0]:
        obj.animation_data_create()


def get_action_index(action):
    data = bpy.data.actions
    return data.keys().index(action)


def get_action_pointer(action):
    data = bpy.data.actions
    return data[action]

# set the active action in the action list layout to the active action of
# the active obj everytime the active action of the active obj change


def set_active_in_list():
    scene = bpy.context.scene
    is_active_sel = scene.actman_action_list_index == get_active_action()[
        0]
    if is_active_sel == False:
        scene.actman_action_list_index = get_active_action()[0]


# set the input (index or name) as active action of the active obj

def set_active_action(action_to_set):
    anim_data = bpy.context.view_layer.objects.active.animation_data
    anim_data.action = bpy.data.actions[action_to_set]
    if prefs().ACTMAN_match_frame:
        set_frame_range(action_to_set)
    set_active_in_list()
    return anim_data.action.name


# get the index of the active, the next and prev action

def get_active_action():
    data = bpy.data.actions
    active_action = bpy.context.view_layer.objects.active.animation_data.action
    index = get_action_index(active_action.name)
    prev_index = index - 1
    next_index = index + 1
    if next_index == len(data):
        next_index = 0
    return index, prev_index, next_index


def remove_action(action_to_remove):
    action_data = bpy.data.actions
    action_to_remove_name = action_data[action_to_remove].name
    action_data.remove(action_data[action_to_remove])
    return action_to_remove_name


# set the selected action as the active action of the active obj

class ACTMAN_OT_set_active_action(bpy.types.Operator):
    bl_idname = "actman.set_active_action"
    bl_label = "Set active action"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = 'Set action as active'

    action_index: bpy.props.IntProperty(
        name='Action list index',
        default=0,
        options={'HIDDEN'}
    )

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        anim_data_create()
        action_active_name = set_active_action(self.action_index)
        self.report({'INFO'},
                    message=f'Active action set to {action_active_name}'
                    )
        return {'FINISHED'}


# remove the selected action from the blend file

class ACTMAN_OT_remove_action(bpy.types.Operator):
    bl_idname = "actman.remove_action"
    bl_label = "Remove action"
    bl_options = {'REGISTER', 'UNDO'}

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


# pin the selected action in the list to pin action 1

class ACTMAN_OT_set_pin_action_1(bpy.types.Operator):
    bl_idname = "actman.set_pin_action_1"
    bl_label = "Set pin action 1"
    bl_description = 'Set action as pin action 1'
    bl_options = {'REGISTER', 'UNDO'}

    pin_action_1_index: bpy.props.IntProperty(
        name='Pin action 1 index',
        options={'HIDDEN'}
    )

    def execute(self, context):
        scene = bpy.context.scene
        index = self.pin_action_1_index
        scene.actman_pin_action_1 = get_action_pointer(index)
        return {'FINISHED'}


# pin the selected action in the list to pin action 2

class ACTMAN_OT_set_pin_action_2(bpy.types.Operator):
    bl_idname = "actman.set_pin_action_2"
    bl_label = "Set pin action 2"
    bl_description = 'Set action as pin action 2'

    pin_action_2_index: bpy.props.IntProperty(
        name='Pin action 2 index',
        options={'HIDDEN'}
    )

    def execute(self, context):
        scene = bpy.context.scene
        index = self.pin_action_2_index
        scene.actman_pin_action_2 = get_action_pointer(index)
        return {'FINISHED'}


# pin the active action to pin action 1

class ACTMAN_OT_set_active_as_pin_1(bpy.types.Operator):
    bl_idname = "actman.set_active_as_pin_action_1"
    bl_label = "Set active as pin action 1"
    bl_description = 'Set active action as pin action 1'

    @classmethod
    def poll(cls, context):
        return is_anim_data_exist()[1]

    def execute(self, context):
        scene = bpy.context.scene
        obj = bpy.context.view_layer.objects.active
        scene.actman_pin_action_1 = obj.animation_data.action
        return {'FINISHED'}


# pin the active action to pin action 1

class ACTMAN_OT_set_active_as_pin_2(bpy.types.Operator):
    bl_idname = "actman.set_active_as_pin_action_2"
    bl_label = "Set active as pin action 2"
    bl_description = 'Set active action as pin action 2'

    @classmethod
    def poll(cls, context):
        return is_anim_data_exist()[1]

    def execute(self, context):
        scene = bpy.context.scene
        obj = bpy.context.view_layer.objects.active
        scene.actman_pin_action_2 = obj.animation_data.action
        return {'FINISHED'}


# set pin action 1 as the active action of the active obj

class ACTMAN_OT_to_pin_action_1(bpy.types.Operator):
    bl_idname = "actman.to_pin_action_1"
    bl_label = "To pin action 1"
    bl_description = 'Set pin action 1 as active'

    @classmethod
    def poll(cls, context):
        return len(bpy.data.actions) != 0

    def execute(self, context):
        pin = bpy.context.scene.actman_pin_action_1
        anim_data_create()
        set_active_action(pin.name)
        return {'FINISHED'}


# set pin action 2 as the active action of the active obj

class ACTMAN_OT_to_pin_action_2(bpy.types.Operator):
    bl_idname = "actman.to_pin_action_2"
    bl_label = "To pin action 2"
    bl_description = 'Set pin action 2 as active'

    @classmethod
    def poll(cls, context):
        return len(bpy.data.actions) != 0

    def execute(self, context):
        pin = bpy.context.scene.actman_pin_action_2
        anim_data_create()
        set_active_action(pin.name)
        return {'FINISHED'}


# set the next action in the action list as the active action of the active obj

class ACTMAN_OT_to_next_action(bpy.types.Operator):
    bl_idname = "actman.next_action"
    bl_label = "Next action"
    bl_description = 'Set next action as active'

    @classmethod
    def poll(cls, context):
        return is_anim_data_exist()[1]

    def execute(self, context):
        next_action = get_active_action()[2]
        set_active_action(next_action)
        set_active_in_list()
        return {'FINISHED'}


# set the prev action in the action list as the active action of the active obj

class ACTMAN_OT_to_prev_action(bpy.types.Operator):
    bl_idname = "actman.prev_action"
    bl_label = "Prev action"
    bl_description = 'Set prev action as active'

    @classmethod
    def poll(cls, context):
        return is_anim_data_exist()[1]

    def execute(self, context):
        prev_action = get_active_action()[1]
        set_active_action(prev_action)
        return {'FINISHED'}


# set the first action in the list as the active action of the active obj

class ACTMAN_OT_to_first_action(bpy.types.Operator):
    bl_idname = "actman.first_action"
    bl_label = "First action"
    bl_description = 'Set first action as active'

    @classmethod
    def poll(cls, context):
        return len(bpy.data.actions) != 0

    def execute(self, context):
        anim_data_create()
        set_active_action(0)
        return {'FINISHED'}


# set the last action in the list as the active action of the active obj

class ACTMAN_OT_to_last_action(bpy.types.Operator):
    bl_idname = "actman.last_action"
    bl_label = "Last action"
    bl_description = 'Set last action as active'

    @classmethod
    def poll(cls, context):
        return len(bpy.data.actions) != 0

    def execute(self, context):
        last_action = len(bpy.data.actions)-1
        anim_data_create()
        set_active_action(last_action)
        return {'FINISHED'}
