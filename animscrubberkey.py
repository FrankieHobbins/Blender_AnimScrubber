import bpy

bl_info = {
"name": "F Scrub Timeline",
"author": "Frankie",
"version": (0,2),
"blender": (2, 77, 0),
"location": "3d view",
"description": "press ALT left click and move mouse in 3d view to change time. Will loop at end frame",
"warning": "",
"wiki_url": "",
"category": "Animation",
}

class ScrubTimelineKey(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "anim.scrubberkey"
    bl_label = "Scrub timeline"
    bl_options = {'REGISTER', 'UNDO'}
    
    def __init__(self):
        print("Start")

    def __del__(self):
        print("End")
    
    Scale = bpy.props.FloatProperty(name="Sensitivity Scale", default=1)
    ScaleBySceneLength = bpy.props.BoolProperty(name="Adjust Sensitivity With Scene Length", default=False)
    StandardSceneLength = bpy.props.FloatProperty(name="Standard Scene Length", default=100)
    LengthScale = bpy.props.FloatProperty(name="Length Scale", default=1)
    
    def modal(self, context, event):
        self.startingvalue = event.mouse_x / 10 * self.Scale * ((((bpy.context.scene.frame_end / self.StandardSceneLength)*self.LengthScale) * self.ScaleBySceneLength) + 1)
        if event.type == 'MOUSEMOVE':  #move frames
            if bpy.context.scene.frame_current > bpy.context.scene.frame_end:
                bpy.context.scene.frame_set(bpy.context.scene.frame_start)
                self.looped += 1
            elif bpy.context.scene.frame_current < bpy.context.scene.frame_start:
                bpy.context.scene.frame_set(bpy.context.scene.frame_end)
                self.looped -= 1
            else:
                bpy.context.scene.frame_set(self.startingvalue - self.dampedvalue + self.sframe - (bpy.context.scene.frame_end*self.looped))
        elif event.type == 'LEFTMOUSE' and event.value == "RELEASE":  # Confirm
            return {'FINISHED'}
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        self.sframe = bpy.context.scene.frame_current 
        self.dampedvalue = event.mouse_x / 10 * self.Scale * ((((bpy.context.scene.frame_end / self.StandardSceneLength)*self.LengthScale) * self.ScaleBySceneLength) + 1)
        self.looped = 0
    
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

def register():
    bpy.utils.register_class(ScrubTimelineKey)
    
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D', region_type='WINDOW', modal=False)
    kmi = km.keymap_items.new('anim.scrubberkey', 'LEFTMOUSE', 'PRESS', alt=True)     

def unregister():
    bpy.utils.unregister_class(ScrubTimelineKey)
    
    
# This allows you to run the script directly from blenders text editor
# to test the addon without having to install it.
#if __name__ == "__main__":
#    register()