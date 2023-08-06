from BDSpace import Space
from BDSpace.Figure import Figure
from BDSpace.Curve import ParametricCurve
from BDSpaceVis.space import SpaceView
from BDSpaceVis.figures import FigureView
from BDSpaceVis.curves import CurveView


def gen_space_views(fig, space, scale=1):
    if not isinstance(space, Space):
        raise ValueError('argument has to be of Space class')
    if isinstance(space, Figure):
        view = FigureView(fig, space, scale=scale)
    elif isinstance(space, ParametricCurve):
        view = CurveView(fig, space, scale=scale)
    else:
        view = SpaceView(fig, space, scale=scale)
    views = {space.name: view}
    for key in space.elements.keys():
        views.update(gen_space_views(fig, space.elements[key], scale=scale/2))
    return views


def draw_space(views):
    for key in views.keys():
        views[key].draw()
