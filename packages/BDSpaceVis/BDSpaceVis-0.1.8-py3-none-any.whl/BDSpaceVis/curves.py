import numpy as np
from mayavi import mlab
from BDSpace.Curve import ParametricCurve

from BDSpaceVis.space import SpaceView


class CurveView(SpaceView):

    def __init__(self, fig, curve, scale=1, color=None, opacity=None, edge_visible=False,
                 cs_visible=True, surface_visible=True, wireframe=False, resolution=20, thickness=None):
        assert isinstance(curve, ParametricCurve)
        self.resolution = resolution
        self.edge_visible = edge_visible
        self.thickness = None
        points, dims = generate_points(curve, self.resolution)
        super(CurveView, self).__init__(fig, curve, scale=scale, color=color, opacity=opacity,
                                        points=points, dims=dims,
                                        cs_visible=cs_visible, surface_visible=surface_visible, wireframe=wireframe)

    def set_resolution(self, resolution):
        self.resolution = resolution
        points, dims = generate_points(self.space, resolution)
        self.set_points(points, dims)
        self.draw()

    def get_thickness(self):
        if self.surface is not None:
            return self.surface.parent.parent.filter.radius

    def set_thickness(self, thickness):
        """
        Sets the thickness of the curve line changing mayavi tube radius
        :param thickness: float number between 0.0 and 1e299
        """
        if isinstance(thickness, (float, int)):
            self.thickness = float(thickness)
            try:
                self.surface.parent.parent.filter.radius = self.thickness
                self.draw()
            except AttributeError:
                pass

    def set_edge_visible(self, edge_visible=True):
        self.edge_visible = edge_visible
        self.draw()

    def draw_surface(self):
        if self.surface_visible:
            if self.points is not None:
                coordinate_system = self.space.basis_in_global_coordinate_system()
                curve_points = np.asarray(coordinate_system.to_parent(self.points))
                if self.surface is None:
                    mlab.figure(self.fig, bgcolor=self.fig.scene.background)
                    if self.thickness is None:
                        self.surface = mlab.plot3d(curve_points[:, 0], curve_points[:, 1], curve_points[:, 2],
                                                   color=self.color)
                        self.thickness = self.get_thickness()
                    else:
                        self.surface = mlab.plot3d(curve_points[:, 0], curve_points[:, 1], curve_points[:, 2],
                                                   color=self.color, tube_radius=self.thickness)
                else:
                    n_pts = len(curve_points) - 1
                    lines = np.zeros((n_pts, 2), 'l')
                    lines[:, 0] = np.arange(0, n_pts - 0.5, 1, 'l')
                    lines[:, 1] = np.arange(1, n_pts + 0.5, 1, 'l')
                    data = self.surface.parent.parent.parent.parent.data
                    data.set(lines=None)
                    data.set(points=curve_points)
                    data.set(lines=lines)
                self.surface.parent.parent.parent.parent.name = self.space.name
                self.surface.parent.parent.filter.radius = self.thickness
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


def generate_points(curve, resolution=20):
    assert isinstance(curve, ParametricCurve)
    dims = None
    num_points = angular_resolution(abs(curve.stop - curve.start), resolution)
    t = np.linspace(curve.start, curve.stop, num=num_points, endpoint=True, dtype=np.float)
    points = curve.generate_points(t)
    return points, dims


def angular_resolution(angle, resolution):
    points_num = int(angle / np.pi * resolution)
    if points_num < 2:
        points_num = 2
    return points_num
