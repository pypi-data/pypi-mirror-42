import numpy as np

from mayavi import mlab
from tvtk.api import tvtk

from BDSpace import Space
from BDSpaceVis.coordinate_system import draw_coordinate_system_axes, update_coordinate_system_axes


class SpaceView(object):

    def __init__(self, fig, space, scale=1, color=None, opacity=None, points=None, dims=None,
                 cs_visible=True, surface_visible=True, wireframe=False):
        self.fig = fig
        if not isinstance(space, Space):
            raise ValueError('Only Space class objects supported')
        self.space = space
        self.scale = scale
        self.cs_visible = cs_visible
        self.cs_arrows = None
        self.cs_labels = None
        self.surface_visible = surface_visible
        self.edge_visible = False
        self.wireframe = wireframe
        self.surface = None

        self.points = None
        self.dims = None
        self.set_points(points, dims)

        self.color = None
        self.opacity = None
        self.set_color(color, opacity)

    def set_points(self, points=None, dims=None):
        if points is None:
            self.points = None
            self.dims = None
        else:
            self.points = np.array(points, dtype=np.float)
            self.dims = dims

    def set_color(self, color=None, opacity=None):
        if color is None:
            self.color = (1, 0, 0)
        elif isinstance(color, (list, tuple, np.array)):
            self.color = color
        else:
            raise ValueError('color must be an iterable of three color values')
        if opacity is None:
            self.opacity = 1.0
        elif isinstance(opacity, (float, int)):
            self.opacity = float(opacity)
            if self.opacity < 0.0:
                self.opacity = 0.0
            elif self.opacity > 1.0:
                self.opacity = 1.0
        else:
            raise ValueError('opacity must be a number between 0 and 1')

    def set_cs_visible(self, cs_visible=True):
        self.cs_visible = cs_visible
        self.draw()

    def set_surface_visible(self, surface_visible=True):
        self.surface_visible = surface_visible
        self.draw()

    def set_wireframe(self, wireframe=True):
        self.wireframe = wireframe
        self.draw()

    def draw_cs(self):
        if self.cs_visible:
            coordinate_system = self.space.basis_in_global_coordinate_system()
            if self.cs_arrows is None:
                self.cs_arrows, self.cs_labels = draw_coordinate_system_axes(self.fig, coordinate_system,
                                                                             offset=0, scale=self.scale)
            else:
                self.cs_arrows, self.cs_labels = update_coordinate_system_axes(coordinate_system, self.cs_arrows,
                                                                               self.cs_labels,
                                                                               offset=0, scale=self.scale)
        else:
            if self.cs_labels is not None:
                for cs_label in self.cs_labels:
                    cs_label.remove()
            if self.cs_arrows is not None:
                self.cs_arrows.remove()
            self.cs_arrows = None
            self.cs_labels = None

    def draw_surface(self):
        if self.surface_visible:
            if self.points is not None:
                coordinate_system = self.space.basis_in_global_coordinate_system()
                if self.surface is None:
                    grid = tvtk.StructuredGrid(dimensions=self.dims)
                    grid.points = np.asarray(coordinate_system.to_parent(self.points))
                    mlab.figure(self.fig, bgcolor=self.fig.scene.background)
                    data_set = mlab.pipeline.add_dataset(grid, self.space.name)
                    self.surface = mlab.pipeline.surface(data_set)
                else:
                    self.surface.parent.parent.data.set(dimensions=self.dims)
                    self.surface.parent.parent.data.set(points=np.asarray(coordinate_system.to_parent(self.points)))
                self.surface.parent.parent.name = self.space.name
                self.surface.actor.property.color = self.color
                self.surface.actor.property.edge_visibility = self.edge_visible
                self.surface.actor.property.edge_color = self.color
                if self.wireframe:
                    self.surface.actor.property.representation = 'wireframe'
                else:
                    self.surface.actor.property.representation = 'surface'
                if self.opacity is not None:
                    self.surface.actor.property.opacity = self.opacity
        else:
            if self.surface is not None:
                self.surface.remove()
            self.surface = None

    def draw_volume(self):
        """
        empty interface stub
        """

    def draw(self):
        self.draw_cs()
        self.draw_surface()
        self.draw_volume()
