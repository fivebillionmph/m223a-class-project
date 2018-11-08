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

electrodes = [
	[210, 60, 136],
	[210, 120, 136],
	[210, 180, 136],
	[210, 240, 136],
	[105, 60, 136],
	[105, 120, 136],
	[105, 180, 136],
	[105, 240, 136],
]

class Visualization(HasTraits):
	scene = Instance(MlabSceneModel, ())
	view = View(Item("scene", editor=SceneEditor(scene_class=MayaviScene), height=250, width=300, show_label=False), VGroup("_", "select_electrode", "electrode_name", "confirm"))
	select_electrode = Range(0, len(electrodes) - 1, 0)
	electrode_name = Str("")
	confirm = Button(label = "Save")

	def __init__(self, electrodes):
		HasTraits.__init__(self)
		#image_data = nib.load("/Users/jamesgo/Projects/python/m277a-1/data/test/T1.bse.nii.gz")
		image_data = nib.load("/Users/jamesgo/Projects/python/m277a-1/data/standard-brain.bse.nii.gz")
		self.plot = self.scene.mlab.contour3d(image_data.get_data(), color=(1.0, .4, 0.7), opacity=0.2)
		self.click_pos = None
		self.electrodes = electrodes
		self.electrode_names = []
		self.init_names()
		self.mayavi_electrodes = set()
		self.refresh_electrodes()

	def refresh_electrodes(self):
		for x in self.mayavi_electrodes:
			x.stop()
		self.mayavi_electrodes.clear()
		for i in range(len(self.electrodes)):
			if i == self.select_electrode:
				color = (1, 0, 0)
			else:
				color = (0, 0, 1)
			coord = self.electrodes[i]
			x = self.scene.mlab.points3d([coord[0]], [coord[1]], [coord[2]], [2], scale_factor = 5, color=color)
			self.mayavi_electrodes.add(x)

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
				self.update_plot()
		except Exception as e:
			print(e)

visualization = Visualization(electrodes)
visualization.configure_traits()
