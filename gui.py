import bpy

from .operators import get_active_action, is_anim_data_exist
from .prefs import prefs


# SIDE PANEL


# statistic panel

class ACTMAN_PT_stat(bpy.types.Panel):
    bl_label = "Statistic"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "ActionMana"
    bl_order = 0

    def draw(self, context):

        layout = self.layout
        if len(bpy.data.actions) == 0:
            box = layout.box()
            box.label(text='Animation data empty')
        else:
            side_panel_stat(layout)


# action list and operators panel

class ACTMAN_PT_sidebar_panel(bpy.types.Panel):
    bl_label = "Action Management"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "ActionMana"
    bl_order = 1

    def draw(self, context):
        layout = self.layout
        layout.prop(prefs(), 'ACTMAN_match_frame',
                    text='Match action frame range',
                    toggle=True,
                    icon=('SOLO_ON'
                          if prefs().ACTMAN_match_frame
                          else 'SOLO_OFF'
                          )
                    )
        side_panel_pin_buttons_layout(layout)
        side_panel_nav_button_layout(layout)
        action_list_layout(layout)
        action_list_toggle_layout(layout)


# LAYOUT FUNCTION


# statistic layout func

def side_panel_stat(layout):

    box = layout.box()

    anim_data = bpy.context.view_layer.objects.active.animation_data

    action_count = len(bpy.data.actions)

    row = box.row(align=True)
    split = row.split(factor=0.3)

    col = split.column(align=True)
    if is_anim_data_exist()[1]:
        col.label(text='Active:', icon='RADIOBUT_ON')
    else:
        col.label(text='Active:', icon='RADIOBUT_OFF')
    col.label(text='Pin 1:', icon='PINNED')
    col.label(text='Pin 2:', icon='PINNED')
    col.separator()
    col.label(text='FPS:', icon='GP_MULTIFRAME_EDITING')
    col.label(text='Count:', icon='ACTION')

    col = split.column(align=True)
    col.alignment = 'EXPAND'
    if is_anim_data_exist()[1]:
        col.prop(anim_data, 'action', text='')
    else:
        col.label(text='None')
    col.prop(bpy.context.scene, 'actman_pin_action_1', text='')
    col.prop(bpy.context.scene, 'actman_pin_action_2', text='')
    col.separator()
    col.prop(bpy.context.scene.render, 'fps', text='')
    col.label(text=f'{action_count} actions')


# buttons layout func

def side_panel_pin_buttons_layout(layout):

    col = layout.row()
    col.operator('actman.set_active_as_pin_action_1',
                 text='Active as pin 1', icon='PINNED', emboss=True
                 )
    col.operator('actman.to_pin_action_1',
                 text='To pin 1', icon='PINNED', emboss=True
                 )
    col = layout.row()
    col.operator('actman.set_active_as_pin_action_2',
                 text='Active as pin 2', icon='PINNED', emboss=True
                 )
    col.operator('actman.to_pin_action_2',
                 text='To pin 2', icon='PINNED', emboss=True
                 )


def side_panel_nav_button_layout(layout):

    row = layout.row()
    row.operator('actman.prev_action',
                 text='Prev', icon='TRIA_UP_BAR', emboss=True
                 )
    row.operator('actman.next_action',
                 text='Next', icon='TRIA_DOWN_BAR', emboss=True
                 )
    row.operator('actman.first_action',
                 text='First', icon='ANCHOR_TOP', emboss=True
                 )
    row.operator('actman.last_action',
                 text='Last', icon='ANCHOR_BOTTOM', emboss=True
                 )


# action list layout func

def action_list_layout(layout):

    layout.template_list('ACTMAN_UL_actions_list', '',
                         bpy.data, 'actions', bpy.context.scene,
                         'actman_action_list_index'
                         )


def action_list_toggle_layout(layout):

    row = layout.row(align=True)

    col = row.column()
    col.alignment = 'LEFT'
    col.prop(prefs(), 'ACTMAN_show_index',
             emboss=True, icon='LINENUMBERS_ON', icon_only=True
             )

    col = row.column()
    col = row.column()

    col = row.column()
    col.alignment = 'RIGHT'

    row = col.row(align=True)

    row.prop(prefs(), 'ACTMAN_show_active',
             emboss=True, icon='RADIOBUT_ON', icon_only=True
             )
    row.prop(prefs(), 'ACTMAN_show_pin_1',
             emboss=True, icon='PINNED', icon_only=True
             )
    row.prop(prefs(), 'ACTMAN_show_pin_2',
             emboss=True, icon='PINNED', icon_only=True
             )
    row.prop(prefs(), 'ACTMAN_show_remove',
             emboss=True, icon='TRASH', icon_only=True
             )

    if prefs().ACTMAN_show_index:
        layout.prop(prefs(), 'ACTMAN_layout_name_offset',
                    text='Name offset', emboss=True)


# ACTION LIST


class ACTMAN_UL_actions_list(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_property, index):

        show_index = prefs().ACTMAN_show_index
        show_active = prefs().ACTMAN_show_active
        show_pin_1 = prefs().ACTMAN_show_pin_1
        show_pin_2 = prefs().ACTMAN_show_pin_2
        show_remove = prefs().ACTMAN_show_remove

        gui_param = (0.1 + 0.2*prefs().ACTMAN_layout_name_offset #split parameter
                     if show_index
                     else 0
                     )

        split = layout.split(factor=gui_param)

        if show_index:
            split.label(text=f'{index + 1}')

        if item == bpy.context.scene.actman_pin_action_1 or item == bpy.context.scene.actman_pin_action_2:
            split.alert=True
            split.prop(item, "name", text='', emboss=True,)
        else:
            split.prop(item, "name", text='', emboss=False,)

        row = layout.row(align=True)

        if is_anim_data_exist()[1]:
            if show_active:
                op = row.operator('actman.set_active_action',
                                  text='',
                                  icon=('RADIOBUT_ON'
                                        if index == get_active_action()[0]
                                        else 'RADIOBUT_OFF'
                                        ),
                                  emboss=False
                                  )
                op.action_index = index

        elif show_active:
            op = row.operator('actman.set_active_action',
                              text='',
                              icon=('RADIOBUT_OFF'),
                              emboss=False
                              )
            op.action_index = index

        if show_pin_1:
            op = row.operator('actman.set_pin_action_1',
                              text='',
                              icon=('PINNED'
                                    if item == bpy.context.scene.actman_pin_action_1
                                    else 'UNPINNED'
                                    ),
                              emboss=False
                              )
            op.pin_action_1_index = index
        

        if show_pin_2:
            op = row.operator('actman.set_pin_action_2',
                              text='',
                              icon=('PINNED'
                                    if item == bpy.context.scene.actman_pin_action_2
                                    else 'UNPINNED'
                                    ),
                              emboss=False,
                              )
            op.pin_action_2_index = index

        if show_remove:
            op = row.operator('actman.remove_action',
                              text='', icon='TRASH', emboss=False
                              )
            op.action_index = index
