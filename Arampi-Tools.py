# Roque Tools vol.1 - First Addon for Blender 2.7x by Miguel Ángel Roque
# Arampi Tools v0.1 - Develop Addon for 3d reconstruction from background images- Blender 2.7x
#
# THIS SCRIPT IS LICENSED UNDER GPL, 
# please read the license block.


bl_info = {
    "name": "ARAMPI Tools",
    "author": "Roque, Miguel Ángel",
    "version": (0, 1),
    "blender": (2, 76, 0),
    "location": "View3D > Tool Shelf > ARAMPI - RoqueTools",
    "description": "Addon con las herramientas principales utilizadas durante el proyecto ARAMPI",
    "warning": "",
    "wiki_url": "[Soon]",
    "tracker_url": "[Soon]",
    "category": "Arampi Tools"}

# import the basic library
import bpy

# main class of this toolbar
class VIEW3D_PT_3dnavigationPanel(bpy.types.Panel):
    bl_label = "Arampi Tools!"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_label = "ARAMPI - Tools"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        view = context.space_data

        # Ajuste del punto de vista        
        row = layout.row(align=True)
        #col.operator("view3d.viewnumpad", text="View Camera", icon='CAMERA_DATA').type='CAMERA'
        row.operator("view3d.localview", text="View Global/Local" , icon="OUTLINER_OB_CAMERA")
        row.operator("view3d.view_persportho", text="View Persp/Ortho" , icon="OUTLINER_DATA_CAMERA")  

        # define el objeto que se mira
        col = layout.column(align=True)
        col.label(text="View to Object:")
        col.prop(view, "lock_object", text="")
        col.operator("view3d.view_selected", text="View to Selected", icon="VIEWZOOM") 

        #Ajustes del cursor
        col.label(text="Cursor:")
        row=col.row(align=True)
        row.operator("view3d.snap_cursor_to_center", text="Cursor to Center")
        row.operator("view3d.snap_cursor_to_selected", text="Cursor to Selected")
        row.operator("view3d.snap_selected_to_cursor", text="Selected to cursor")
        row = layout.row(align=True)
        row.operator("view3d.view_center_cursor", text="View")
        
        #Alinear viewport3D
        split = layout.split()
        #columna 1
        col = split.column(align=True)
        col.label(text="Align view from:")
        row = col.row(align=True)
        row.scale_y = 2.05
        row.operator("view3d.viewnumpad", text="Front").type='FRONT'
        row.operator("view3d.viewnumpad", text="Back").type='BACK'
        row = col.row(align=True)
        row.scale_y = 2.05
        row.operator("view3d.viewnumpad", text="Left").type='LEFT'
        row.operator("view3d.viewnumpad", text="Right").type='RIGHT'
        row = col.row(align=True)
        row.scale_y = 2.05
        row.operator("view3d.viewnumpad", text="Top").type='TOP'
        row.operator("view3d.viewnumpad", text="Bottom").type='BOTTOM'
        
        #columna 2
        col = split.column()
        col.label(text="sombreado")

        col.prop(context.space_data, "viewport_shade", expand=True)
        
        col = layout.column(align=True)
        col.label(text="selección")
        
        row = col.row()
        row = layout.row(align=True)
        row.operator("object.select_all", text="seleccionar objeto" , icon="OBJECT_DATA")
        row.operator("mesh.select_all", text="seleccionar malla", icon="MESH_DATA")

        row = layout.row(align=True)
        
        row.operator("view3d.select_circle", icon="MESH_CIRCLE")
        row.operator("view3d.select_border", icon="MESH_PLANE")
        
        col = layout.column(align=True)
        col.label(text="manipulación")
        row = layout.row(align=True)
        row.operator("transform.translate", icon="MAN_TRANS")
        row.operator("transform.rotate", icon="MAN_ROT")
        row.operator("transform.resize", icon="MAN_SCALE")
        
        
        col = layout.column(align=True)
        col.label(text="modo")
        row = col.row()
        row = layout.row(align=True)
        row.scale_y = 2.0
        row.scale_x = 4.0 
        row.operator("object.editmode_toggle" , icon ='EDIT', text="")
        row.operator("sculpt.sculptmode_toggle", icon ='SCULPTMODE_HLT', text="")
        row.operator("paint.vertex_paint_toggle", icon ='VPAINT_HLT', text="")
        row.operator("paint.weight_paint_toggle" , icon ='WPAINT_HLT', text="")
        row.operator("paint.texture_paint_toggle", icon ='TPAINT_HLT', text="")
        #
        #
        #
        #
        col = layout.column(align=True)
        col.label(text="fondo")
        row = layout.row(align=True)
        row.operator("view3d.background_image_add", text="Add Image", icon="IMAGE_DATA")
        row.operator("view3d.background_image_remove", text="Remove Image" , icon ="X")

        for i, bg in enumerate(view.background_images):
            layout.active = view.show_background_images
            box = layout.box()
            row = box.row(align=True)
            row.prop(bg, "show_expanded", text="", emboss=False)
            if bg.source == 'IMAGE' and bg.image:
                row.prop(bg.image, "name", text="", emboss=False)
            elif bg.source == 'MOVIE_CLIP' and bg.clip:
                row.prop(bg.clip, "name", text="", emboss=False)
            else:
                row.label(text="Not Set")

            if bg.show_background_image:
                row.prop(bg, "show_background_image", text="", emboss=False, icon='RESTRICT_VIEW_OFF')
            else:
                row.prop(bg, "show_background_image", text="", emboss=False, icon='RESTRICT_VIEW_ON')

            row.operator("view3d.background_image_remove", text="", emboss=False, icon='X').index = i

            box.prop(bg, "view_axis", text="Axis")

            if bg.show_expanded:
                row = box.row()
                row.prop(bg, "source", expand=True)

                has_bg = False
                if bg.source == 'IMAGE':
                    row = box.row()
                    row.template_ID(bg, "image", open="image.open")
                    if bg.image is not None:
                        box.template_image(bg, "image", bg.image_user, compact=True)
                        has_bg = True

                        if use_multiview and bg.view_axis in {'CAMERA', 'ALL'}:
                            box.prop(bg.image, "use_multiview")

                            column = box.column()
                            column.active = bg.image.use_multiview

                            column.label(text="Views Format:")
                            column.row().prop(bg.image, "views_format", expand=True)

                            sub = column.box()
                            sub.active = bg.image.views_format == 'STEREO_3D'
                            sub.template_image_stereo_3d(bg.image.stereo_3d_format)

                elif bg.source == 'MOVIE_CLIP':
                    box.prop(bg, "use_camera_clip")

                    column = box.column()
                    column.active = not bg.use_camera_clip
                    column.template_ID(bg, "clip", open="clip.open")

                    if bg.clip:
                        column.template_movieclip(bg, "clip", compact=True)

                    if bg.use_camera_clip or bg.clip:
                        has_bg = True

                    column = box.column()
                    column.active = has_bg
                    column.prop(bg.clip_user, "proxy_render_size", text="")
                    column.prop(bg.clip_user, "use_render_undistorted")

                if has_bg:
                    col = box.column()
                    col.prop(bg, "opacity", slider=True)
                    col.row().prop(bg, "draw_depth", expand=True)

                    if bg.view_axis in {'CAMERA', 'ALL'}:
                        col.row().prop(bg, "frame_method", expand=True)

                    box = col.box()
                    row = box.row()
                    row.prop(bg, "offset_x", text="X")
                    row.prop(bg, "offset_y", text="Y")

                    row = box.row()
                    row.prop(bg, "use_flip_x")
                    row.prop(bg, "use_flip_y")

                    row = box.row()
                    if bg.view_axis != 'CAMERA':
                        row.prop(bg, "rotation")
                        row.prop(bg, "size")
        #


# register the class
def register():
    bpy.utils.register_module(__name__)
 
    pass 

def unregister():
    bpy.utils.unregister_module(__name__)
 
    pass 

if __name__ == "__main__": 
    register()
