import csv
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

def _readfile(subject_id, filename):
	results = []
	with open(filename, "r") as f:
		reader = csv.reader(f)
		for row in reader:
			row = list(row)
			result = {}
			for i in range(len(_HEADER)):
				if i < len(row):
					result[_HEADER[i]] = row[i]
				else:
					result[_HEADER[i]] = ""
			try:
				if int(result["sid"]) == subject_id:
					results.append(result)
			except:
				pass
	return results

def _channelDataToElectrodes(channel_data):
	electrodes = []
	for cd in channel_data:
		electrodes.append([int(cd["x"]), int(cd["y"]), int(cd["z"])])
	return electrodes

def run(subject_id, filename, brain_file):
	channel_data = _readfile(subject_id, filename)
	electrodes = _channelDataToElectrodes(channel_data)

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
			self.electrode_names = []
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
				self.electrode_names.append("")

		@on_trait_change("select_electrode")
		def update_plot(self):
			self.refresh_electrodes()
			self.electrode_name = self.electrode_names[self.select_electrode]

		@on_trait_change("confirm")
		def confirm_event(self):
			try:
				index_change = 1

				if len(self.electrode_name) > 0:
					self.electrode_name = str(int(self.electrode_name))
				self.electrode_names[self.select_electrode] = self.electrode_name
				new_index = self.select_electrode + index_change
				if new_index >= len(self.electrodes):
					new_index = 0
				if new_index >= 0 and new_index < len(self.electrodes):
					self.select_electrode = new_index
			except Exception as e:
				print(e)

	visualization = Visualization(electrodes)
	visualization.configure_traits()

if __name__ == "__main__":
	csv_file = "../data/test_file.csv"
	brain_file = "/Users/jamesgo/Projects/python/m277a-1/data/standard-brain.bse.nii.gz"
	#brain_file = "/Users/jamesgo/Projects/python/m277a-1/data/test/T1.bse.nii.gz"
	run(1, csv_file, brain_file)
