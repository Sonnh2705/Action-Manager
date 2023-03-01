import bpy


def prefs():
    return bpy.context.preferences.addons[__package__].preferences


class ACTMAN_prefs(bpy.types.AddonPreferences):
    bl_idname = __package__

    ACTMAN_show_index: bpy.props.BoolProperty(
        name="Show action list index",
        default=True
    )

    ACTMAN_show_active: bpy.props.BoolProperty(
        name="Show set active action button",
        default=True
    )

    ACTMAN_show_pin_1: bpy.props.BoolProperty(
        name="Show set pin action 1 index",
        default=True
    )

    ACTMAN_show_pin_2: bpy.props.BoolProperty(
        name="Show set pin action 2 index",
        default=False
    )

    ACTMAN_show_remove: bpy.props.BoolProperty(
        name="Show remove action button",
        default=False
    )

    ACTMAN_match_frame: bpy.props.BoolProperty(
        name="Match the frame range of the active scene to active action",
        default=True
    )

    ACTMAN_layout_name_offset: bpy.props.FloatProperty(
        name="Pos of name property relative to index property in the list",
        default=0,
        min=0,
        max=1
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text='Layout options:')

        row = layout.row()
        row.prop(self, 'ACTMAN_show_index')
        row.separator()
        row.prop(self, 'ACTMAN_layout_name_offset',
                 text='Name offset', slider=True)
        row.separator()

        row = layout.row()
        col = row.column()
        col.prop(self, 'ACTMAN_show_active')
        col.separator()
        col.prop(self, 'ACTMAN_show_remove')

        col = row.column()
        col.prop(self, 'ACTMAN_show_pin_1')
        col.separator()
        col.prop(self, 'ACTMAN_show_pin_2')

        layout.label(text='Function options:')
        layout.prop(self,
                    'ACTMAN_match_frame',
                    text='Match action frame range'
                    )
