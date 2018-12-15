import nibabel as nib
from mayavi import mlab
from traits.api import HasTraits, on_trait_change, Range, Instance, Str, Button
from traitsui.api import View, Item, VGroup
from tvtk.pyface.scene_editor import SceneEditor
from mayavi.core.ui.mayavi_scene import MayaviScene
from mayavi.tools.mlab_scene_model import MlabSceneModel

"""
to dos:
    arrow or enter goes to next electrode
    checked that entered name is a number and in the correct range
"""

_HEADER = ["sid", "channel", "eid", "x", "y", "z"]

def _readDBChannels(cursor, subject_id):
    cursor.execute("select * from channels where sid = %s and eid is NULL", (subject_id, ))
    return cursor.fetchall()

def _readDBBrainFile(cursor, subject_id):
    cursor.execute("select smr_path from subjects where sid = %s", (subject_id, ))
    return cursor.fetchone()["smr_path"]

def _channelDataToElectrodes(channel_data):
    electrodes = []
    for cd in channel_data:
        electrodes.append([int(cd["x"]), int(cd["y"]), int(cd["z"])])
    return electrodes

def _saveElectrodeNames(cursor, channel_data, electrode_names):
    skipped = 0
    for i in range(len(channel_data)):
        try:
            if electrode_names[i] == "":
                skipped += 1
                continue
            int_name = int(electrode_names[i])
            cursor.execute("update channels set channel = %s where sid = %s and x = %s and y = %s and z = %s", (int_name, channel_data[i]["sid"], channel_data[i]["x"], channel_data[i]["y"], channel_data[i]["z"]))
        except:
            skipped += 1
    print("Could not update %d out of %d channels" % (skipped, len(channel_data)))

def run(cursor, subject_id):
    channel_data = _readDBChannels(cursor, subject_id)
    brain_file = _readDBBrainFile(cursor, subject_id)
    electrodes = _channelDataToElectrodes(channel_data)
    electrode_names = []

    if len(electrodes) == 0:
        return

    class Visualization(HasTraits):
        scene = Instance(MlabSceneModel, ())
        view = View(Item("scene", editor=SceneEditor(scene_class=MayaviScene), height=250, width=300, show_label=False), VGroup("_", "select_electrode", "electrode_name", "confirm"))
        select_electrode = Range(0, len(electrodes) - 1, 0)
        electrode_name = Str("")
        confirm = Button(label = "Save")

        def __init__(self, electrodes):
            HasTraits.__init__(self)
            image_data = nib.load(brain_file)
            self.plot = self.scene.mlab.contour3d(image_data.get_data(), color=(1.0, .4, 0.7), opacity=0.2)
            self.last_electrode = None
            self.click_pos = None
            self.electrodes = electrodes
            self.init_names()
            self.mayavi_electrodes = []
            self.refresh_electrodes()

        def refresh_electrodes(self):
            if len(self.mayavi_electrodes) == 0:
                for i in range(len(self.electrodes)):
                    if i == self.select_electrode:
                        color = (1, 0, 0)
                    else:
                        color = (0, 0, 1)
                    coord = self.electrodes[i]
                    x = self.scene.mlab.points3d([coord[0]], [coord[1]], [coord[2]], [2], scale_factor = 2, color=color)
                    self.mayavi_electrodes.append(x)
            else:
                self.mayavi_electrodes[self.select_electrode].stop()
                self.mayavi_electrodes[self.last_electrode].stop()
    
                coord = self.electrodes[self.select_electrode]
                self.mayavi_electrodes[self.select_electrode] = self.scene.mlab.points3d([coord[0]], [coord[1]], [coord[2]], [2], scale_factor = 2, color = (1, 0, 0))
    
                coord = self.electrodes[self.last_electrode]
                self.mayavi_electrodes[self.last_electrode] = self.scene.mlab.points3d([coord[0]], [coord[1]], [coord[2]], [2], scale_factor = 2, color = (0, 0, 1))

            self.last_electrode = self.select_electrode

        def init_names(self):
            for i in range(len(self.electrodes)):
                if channel_data[i]["channel"] is not None:
                    electrode_names.append(str(channel_data[i]["channel"]))
                else:
                    electrode_names.append("")

        @on_trait_change("select_electrode")
        def update_plot(self):
            self.refresh_electrodes()
            self.electrode_name = electrode_names[self.select_electrode]

        @on_trait_change("confirm")
        def confirm_event(self):
            try:
                index_change = 1

                if len(self.electrode_name) > 0:
                    self.electrode_name = str(int(self.electrode_name))
                electrode_names[self.select_electrode] = self.electrode_name
                new_index = self.select_electrode + index_change
                if new_index >= len(self.electrodes):
                    new_index = 0
                if new_index >= 0 and new_index < len(self.electrodes):
                    self.select_electrode = new_index
            except Exception as e:
                print(e)

    visualization = Visualization(electrodes)
    visualization.configure_traits()

    _saveElectrodeNames(cursor, channel_data, electrode_names)

if __name__ == "__main__":
    brain_file = "/Users/jamesgo/Projects/python/m277a-1/data/standard-brain.bse.nii.gz"
    #brain_file = "/Users/jamesgo/Projects/python/m277a-1/data/test/T1.bse.nii.gz"
    run(1, brain_file)
