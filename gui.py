import bpy
from bpy.types import Context

from .operators import get_active_action, is_anim_data_exist
from .prefs import prefs


# SIDE PANEL

class ACTMAN_PT_stat_panel(bpy.types.Panel):
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


class ACTMAN_PT_action_manager_panel(bpy.types.Panel):
    bl_label = "Action Management"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "ActionMana"
    bl_order = 1

    def draw(self, context):

        layout = self.layout

        side_panel_pin_buttons_layout(layout)
        side_panel_nav_button_layout(layout)
        action_list_toggle_layout(layout)
        action_list_layout(layout)


class ACTMAN_PT_nla_manager_panel(bpy.types.Panel):
    bl_label = "Export manager"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "ActionMana"
    bl_order = 2

    @classmethod
    def poll(cls, context):

        return prefs().use_export

    def draw(self, context):

        layout = self.layout

        row1 = layout.row(align=True)

        if bpy.context.active_object is not None and is_anim_data_exist()[0]:
            row1.prop(bpy.context.active_object.animation_data,
                      'use_nla',
                      text='Use NLA',
                      icon='NLA',
                      toggle=True
                      )
            row1.prop(prefs(),
                      'reverse_order',
                      text='Reverse',
                      icon='FILE_REFRESH',
                      toggle=True
                      )

            row2 = layout.row(align=True)

            op1 = row2.operator('actman.move_strip_in_list',
                                text='Up',
                                icon='TRIA_UP'
                                )
            op1.options = 'UP'

            op2 = row2.operator('actman.move_strip_in_list',
                                text='Down',
                                icon='TRIA_DOWN'
                                )
            op2.options = 'DOWN'

        else:
            layout.label(text='No animation data')

        if bpy.context.active_object is not None:

            layout.template_list('ACTMAN_UL_nla_list',
                                 '2',
                                 bpy.context.active_object.animation_data,
                                 'nla_tracks',
                                 bpy.context.scene.actman_settings,
                                 'export_list_index',
                                 rows=8
                                 )

# ACTION LIST


class ACTMAN_UL_actions_list(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_property, index):

        pin = [bpy.context.scene.actman_settings.pin_action_1,
               bpy.context.scene.actman_settings.pin_action_2,
               ]

        split_param = (0.1 + 0.2*prefs().layout_name_offset  # split parameter
                       if prefs().show_index
                       else 0
                       )

        split = layout.split(factor=split_param)

        if prefs().show_index:
            split.label(text=f'{index + 1}')

        # alert pinned action 1

        if item in pin:
            split.alert = True
            split.prop(item, "name", text='', emboss=True,)
        else:
            split.prop(item, "name", text='', emboss=False,)

        row = layout.row(align=True)
        row.alignment = 'LEFT'

        # show frame range

        if prefs().show_frame:
            row.label(text=f'[{int(item.frame_range[0])}-{int(item.frame_range[1])}]')

        # set active action btn

        if bpy.context.active_object is not None and is_anim_data_exist()[1]:

            if prefs().show_active:
                op = row.operator('actman.set_active_action',
                                  text='',
                                  icon=('RADIOBUT_ON'
                                        if index == get_active_action()[0]
                                        else 'RADIOBUT_OFF'
                                        ),
                                  emboss=False
                                  )
                op.options = 'IN LIST'
                op.action_index = index

        elif prefs().show_active:
            op = row.operator('actman.set_active_action',
                              text='',
                              icon=('RADIOBUT_OFF'),
                              emboss=False
                              )
            op.options = 'IN LIST'
            op.action_index = index

        # pin 1 btn

        if prefs().show_pin_1:
            op = row.operator('actman.set_pin_action',
                              text='',
                              icon=('PINNED'
                                    if item == bpy.context.scene.actman_settings.pin_action_1
                                    else 'UNPINNED'
                                    ),
                              emboss=False
                              )
            op.options = 'LIST 1'
            op.pin_action_1_index = index

        # pin 2 btn

        if prefs().show_pin_2:
            op = row.operator('actman.set_pin_action',
                              text='',
                              icon=('PINNED'
                                    if item == bpy.context.scene.actman_settings.pin_action_2
                                    else 'UNPINNED'
                                    ),
                              emboss=False,
                              )
            op.options = 'LIST 2'
            op.pin_action_2_index = index

        # push down btn

        if prefs().show_push_down:
            op = row.operator('actman.export_manager_ops',
                              text='',
                              icon='NLA_PUSHDOWN',
                              emboss=False
                              )
            op.options = 'PUSH'
            op.index = index

        # duplicate btn

        if prefs().show_duplicate:
            op = row.operator('actman.duplicate_action',
                              text='',
                              icon='DUPLICATE',
                              emboss=False
                              )
            op.action_index = index

        # remove btn

        if prefs().show_remove:
            op = row.operator('actman.remove_action',
                              text='',
                              icon='TRASH',
                              emboss=False
                              )
            op.action_index = index


# NLA LIST


class ACTMAN_UL_nla_list(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_property, index):

        split_param = (0.1 + 0.2*prefs().layout_name_offset  # split parameter
                       if prefs().show_index
                       else 0
                       )

        layout.enabled = bpy.context.active_object.animation_data.use_nla

        split = layout.split(factor=split_param)

        # index and name prop

        if prefs().show_index:
            split.label(text=f'{index+1}')

        name = split.row(align=True)

        if len(item.strips) > 0 and len(item.strips) < 2:
            name.prop(item.strips[0], 'name', text='', emboss=False)

        elif len(item.strips) > 1:
            name.alert = True
            name.label(text='', icon='ERROR')
            name.prop(item.strips[0], 'name', text='', emboss=False)

        elif len(item.strips) < 1:
            name.alert = True
            name.label(text='[Slot empty]', icon='ERROR')

        btn = layout.row(align=True)
        btn.alignment = 'RIGHT'

        if prefs().show_frame and len(item.strips) > 0:
            btn.label(text=f'[{int(item.strips[0].frame_start)}-{int(item.strips[0].frame_end)}]')

        elif prefs().show_frame and len(item.strips) == 0:
            btn.label(text='[0-0]')

        # mute prop
        if prefs().show_active:
            btn = layout.row(align=True)
            btn.prop(item, 'mute', text='', invert_checkbox=True)

        # delete operator

        if prefs().show_remove:
            op = btn.operator('actman.export_manager_ops',
                              text='',
                              icon='TRASH',
                              emboss=False,
                              )
            op.options = 'DEL'
            op.index = index

    def filter_items(self, context, data, property):

        # reverse order

        item = getattr(data, property)

        flter = bpy.types.UI_UL_list.filter_items_by_name(self.filter_name,
                                                          self.bitflag_filter_item,
                                                          item,
                                                          "name",
                                                          reverse=False
                                                          )

        order = [index for index, item in enumerate(item)]

        self.use_filter_sort_reverse = bool(prefs().reverse_order)

        return flter, order


# LAYOUT FUNCTION


# statistic layout func

def side_panel_stat(layout):

    action_count = len(bpy.data.actions)

    box = layout.box()

    box.prop(prefs(), 'match_frame',
             text='Match action frame range',
             toggle=True,
             icon=('SOLO_ON'
                      if prefs().match_frame
                      else 'SOLO_OFF'
                   )
             )
    row = box.row(align=True)
    split = row.split(factor=0.34)

    # left column

    left = split.column(align=True)
    left.label(text='FPS:', icon='GP_MULTIFRAME_EDITING')
    left.label(text='Count:', icon='ACTION')
    left.separator()

    # right column

    right = split.column(align=True)
    right.alignment = 'EXPAND'
    right.prop(bpy.context.scene.render, 'fps', text='')
    right.label(text=f'{action_count} actions')
    right.separator()


# buttons layout func

def side_panel_pin_buttons_layout(layout):

    row = layout.row(align=True)
    split = row.split(factor=0.35, align=True)

    # left split

    left = split.column(align=True)
    row1 = left.row(align=True)
    row1.label(text='Active:', icon='RADIOBUT_ON')

    row2 = left.row(align=True)
    pin1 = row2.operator('actman.set_pin_action',
                         text='Pin active', icon='PINNED', emboss=True
                         )
    pin1.options = 'ACTIVE 1'

    row3 = left.row(align=True)
    pin2 = row3.operator('actman.set_pin_action',
                         text='Pin active', icon='PINNED', emboss=True
                         )
    pin2.options = 'ACTIVE 2'

    # right split

    right = split.column(align=True)

    if (bpy.context.active_object is None
            or (bpy.context.active_object is not None and not is_anim_data_exist()[0])
            ):
        row = right.row(align=True)
        box = row.box()
        box.label(text='None')
        box.scale_y = 0.5

    else:
        active = right.row(align=True)
        active.scale_x = 1.3
        active.prop(bpy.context.active_object.animation_data, 'action', text='')

        dup = active.row()
        dup.enabled = bpy.context.active_object.animation_data.action != None
        dup.operator('actman.duplicate_action',
                     text='',
                     icon='DUPLICATE'
                     )

    pin1 = right.row(align=True)
    pin1.scale_x = 1.3
    pin1.prop(bpy.context.scene.actman_settings, 'pin_action_1', text=''
              )

    pin1_btn = pin1.row()
    op = pin1_btn.operator('actman.set_active_action',
                           text='', icon='PIVOT_CURSOR', emboss=True
                           )
    op.options = 'PIN 1'

    pin2 = right.row(align=True)
    pin2.scale_x = 1.3
    pin2.prop(bpy.context.scene.actman_settings, 'pin_action_2', text=''
              )

    pin2_btn = pin2.row()
    op = pin2_btn.operator('actman.set_active_action',
                           text='', icon='PIVOT_CURSOR', emboss=True
                           )
    op.options = 'PIN 2'


def side_panel_nav_button_layout(layout):

    row = layout.row()

    prv = row.operator('actman.set_active_action',
                       text='Prev',
                       icon='TRIA_UP_BAR',
                       emboss=True,
                       )
    prv.options = 'PREV'

    nxt = row.operator('actman.set_active_action',
                       text='Next', icon='TRIA_DOWN_BAR', emboss=True
                       )
    nxt.options = 'NEXT'

    fst = row.operator('actman.set_active_action',
                       text='First', icon='ANCHOR_TOP', emboss=True
                       )
    fst.options = 'FIRST'

    lst = row.operator('actman.set_active_action',
                       text='Last', icon='ANCHOR_BOTTOM', emboss=True
                       )
    lst.options = 'LAST'


# action list layout func

def action_list_layout(layout):

    layout.template_list('ACTMAN_UL_actions_list',
                         '',
                         bpy.data,
                         'actions',
                         bpy.context.scene.actman_settings,
                         'action_list_index',
                         rows=8
                         )


def action_list_toggle_layout(layout):

    row = layout.row(align=True)

    left = row.column()
    left.alignment = 'LEFT'
    left.prop(prefs(), 'show_index',
              emboss=True, icon='LINENUMBERS_ON', icon_only=True
              )
    if prefs().show_index:
        row.prop(prefs(), 'layout_name_offset',
                 text='Name offset', emboss=True)

    right = row.column()
    right.alignment = 'RIGHT'

    toggle = right.row(align=True)

    toggle.prop(prefs(), 'show_frame',
                emboss=True, icon='DRIVER_DISTANCE', icon_only=True
                )
    toggle.prop(prefs(), 'show_active',
                emboss=True, icon='RADIOBUT_ON', icon_only=True
                )
    toggle.prop(prefs(), 'show_pin_1',
                emboss=True, icon='PINNED', icon_only=True
                )
    toggle.prop(prefs(), 'show_pin_2',
                emboss=True, icon='PINNED', icon_only=True
                )
    toggle.prop(prefs(), 'show_push_down',
                emboss=True, icon='NLA_PUSHDOWN', icon_only=True
                )
    toggle.prop(prefs(), 'show_duplicate',
                emboss=True, icon='DUPLICATE', icon_only=True
                )
    toggle.prop(prefs(), 'show_remove',
                emboss=True, icon='TRASH', icon_only=True
                )
