import bpy


def prefs():
    return bpy.context.preferences.addons[__package__].preferences


class ACTMAN_prefs(bpy.types.AddonPreferences):
    bl_idname = __package__

    show_index: bpy.props.BoolProperty(
        name='Show index',
        description="Show action list index",
        default=True
    )

    layout_name_offset: bpy.props.FloatProperty(
        name='Name offset',
        description='Pos of name property relative to index property in the list',
        default=0,
        min=0,
        max=1
    )

    show_frame: bpy.props.BoolProperty(
        name='Show frame',
        description="Show action's frame range",
        default=False
    )

    show_active: bpy.props.BoolProperty(
        name='Show active',
        description="Show set active action button",
        default=True
    )

    show_pin_1: bpy.props.BoolProperty(
        name='Show pin 1',
        description="Show set pin action 1 index",
        default=True
    )

    show_pin_2: bpy.props.BoolProperty(
        name='Show pin 2',
        description="Show set pin action 2 index",
        default=False
    )

    show_remove: bpy.props.BoolProperty(
        name='Show remove',
        description="Show remove action button",
        default=False
    )

    show_push_down: bpy.props.BoolProperty(
        name='Show push down',
        description="Show push down button",
        default=False
    )

    show_duplicate: bpy.props.BoolProperty(
        name='Show duplicate',
        description="Show duplicate action button",
        default=False
    )

    match_frame: bpy.props.BoolProperty(
        name='Match frame',
        description="Match scene's frame range to active action",
        default=True
    )

    use_export: bpy.props.BoolProperty(
        name='Use export',
        description='Use export manager',
        default=True
    )

    reverse_order: bpy.props.BoolProperty(
        name='Reverse order',
        description='Reverse nla strips order (Unity order)',
        default=True
    )

    def draw(self, context):

        layout = self.layout

        layout.label(text='Layout options:')

        row = layout.row()
        row.prop(self, 'show_index')
        row.separator()
        row.prop(self, 'layout_name_offset',
                 text='Name offset', slider=True)
        row.separator()

        row = layout.row()
        col = row.column()
        col.prop(self, 'show_frame')
        col.separator()
        col.prop(self, 'show_pin_1')
        col.separator()
        col.prop(self, 'show_remove')

        col = row.column()
        col.prop(self, 'show_active')
        col.separator()
        col.prop(self, 'show_pin_2')
        col.separator()
        col.prop(self, 'show_duplicate')

        layout.label(text='Function options:')

        row = layout.row()
        col = row.column()
        col.prop(self,
                 'match_frame',
                 text='Match action frame range'
                 )
        col.separator()
        col.prop(self,
                 'reverse_order',
                 text='Reverse list order'
                 )

        col = row.column(align=True)
        col.prop(self,
                 'use_export',
                 text='Use export manager'
                 )
