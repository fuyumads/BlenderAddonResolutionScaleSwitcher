import bpy

bl_info = {
    "name": "UI Scale Toggle",
    "description": "Addon for seamless Blender UI resolution toggling.",
    "author": "fuyumads",
    "version": "0.5",
    "blender": (2, 93, 0),
    "location": "VIEW > UI Scale Toggle",
    "category": "Interface",
}

def nowUiScale():
    return round(bpy.context.preferences.view.ui_scale, 2)


class UiScaleToggleOperator(bpy.types.Operator):

    bl_idname = "wm.ui_scale_toggle_operator"
    bl_label = ""
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        _pref = bpy.context.preferences.addons[__name__].preferences
        _newFlag = not _pref.ui_scale_bool
        _pref.ui_scale_bool = _newFlag

        _currentUiScale = int(round(nowUiScale()*100))
        _s1 = int(round(_pref.ui_scale_1*100))
        _s2 = int(round(_pref.ui_scale_2*100))

        _setNewScale = float(_s2)*0.01 if _newFlag else float(_s1)*0.01
        bpy.context.preferences.view.ui_scale = _setNewScale

        # If the resolution value is other than small or large scale, keep the previous resolution value
        # (manually adjust as needed).
        if _currentUiScale not in [_s1, _s2]:
            if _currentUiScale != int(round(_pref.ui_scale_0 * 100)):
                _FBScale = round(float(_currentUiScale)*0.01, 2)
                self.report({'INFO'}, "Changed DEFAULT FallBack SCALE = %f" % (_FBScale))
                _pref.ui_scale_0 = _FBScale

        return {"FINISHED"}

def menu_func(self, context):
    self.layout.separator()
    self.layout.operator(UiScaleToggleOperator.bl_idname, text="UI ScaleToggle")

def draw_header_func(self, context):
    layout = self.layout
    _pref = bpy.context.preferences.addons[__name__].preferences
    layout.operator(UiScaleToggleOperator.bl_idname, icon='ZOOM_IN', depress=_pref.ui_scale_bool)


class VIEW3D_PT_ui_scale_preferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    
    ui_scale_1: bpy.props.FloatProperty(name="UI_scale_NORMAL", default=1.00, min=0.5, max=2.0, step=1)
    ui_scale_2: bpy.props.FloatProperty(name="UI_scale_ZOOM_Active", default=1.15, min=0.5, max=2.5, step=1)
    
    _currentUiScale = nowUiScale()
    
    ui_scale_0: bpy.props.FloatProperty(name="UI_scale_FallBackValue", default=_currentUiScale)
    
    ui_scale_bool: bpy.props.BoolProperty(name = 'UI_scale_Bool', default = False)
    
    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        
        _currentUiScaleCHK = nowUiScale()
        _pref = bpy.context.preferences.addons[__name__].preferences
        if (abs(_currentUiScaleCHK - _pref.ui_scale_1) < 0.001) or (abs(_currentUiScaleCHK - _pref.ui_scale_2) < 0.001):
            _currentUiScaleCHK = round(_pref.ui_scale_0, 2)

        col.label(text="UI Scale Toggle Preferences  (FallBack_Value: {} ) ".format(_currentUiScaleCHK))
        
        row = col.row(align=True)
        
        row.prop(self, "ui_scale_1")
        row.prop(self, "ui_scale_2")


def register():
    bpy.utils.register_class(VIEW3D_PT_ui_scale_preferences)
    bpy.utils.register_class(UiScaleToggleOperator)
    bpy.types.VIEW3D_MT_view.append(menu_func)
    bpy.types.VIEW3D_HT_header.append(draw_header_func)


def unregister():
    bpy.utils.unregister_class(UiScaleToggleOperator)
    bpy.utils.unregister_class(VIEW3D_PT_ui_scale_preferences)
    bpy.types.VIEW3D_MT_view.remove(menu_func)
    bpy.types.VIEW3D_HT_header.remove(draw_header_func)

if __name__ == "__main__":
    register()

