import numpy as np

from mayavi import mlab
from tvtk.api import tvtk

from BDSpaceVis import generators


def euler_color(euler_angles):
    r = (euler_angles.euler_angles[0] + np.pi) / (2 * np.pi)
    g = euler_angles.euler_angles[1] / np.pi
    b = (euler_angles.euler_angles[2] + np.pi) / (2 * np.pi)
    if np.allclose(r, 0):
        r = 0
    if np.allclose(g, 0):
        g = 0
    if np.allclose(b, 0):
        b = 0
    return r, g, b


def coordinate_system_arrows(coordinate_system, offset=0.0, scale=1.0):
    points = []
    lengths = []
    for i in range(3):
        points.append(coordinate_system.origin + scale * np.asarray(coordinate_system.basis[i]) * offset)
        lengths.append(np.asarray(coordinate_system.basis[:, i]) * scale)
    points = np.array(points)
    lengths = np.array(lengths)
    return points, lengths


def draw_coordinate_system_axes(fig, coordinate_system, offset=0.0, scale=1.0, draw_labels=True):
    points, lengths = coordinate_system_arrows(coordinate_system, offset=offset, scale=scale)
    mlab.figure(fig, bgcolor=fig.scene.background)
    arrows = mlab.quiver3d(points[:, 0], points[:, 1], points[:, 2],
                           lengths[0, :], lengths[1, :], lengths[2, :],
                           scalars=np.array([3, 2, 1]), mode='arrow')
    arrows.glyph.color_mode = 'color_by_scalar'
    arrows.glyph.glyph.scale_factor = scale
    data = arrows.parent.parent
    data.name = coordinate_system.name
    glyph_scale = arrows.glyph.glyph.scale_factor * 1.1
    label_col = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    labels = []
    if draw_labels:
        for i in range(3):
            labels.append(mlab.text3d(points[i, 0] + glyph_scale * coordinate_system.basis[i, 0],
                                      points[i, 1] + glyph_scale * coordinate_system.basis[i, 1],
                                      points[i, 2] + glyph_scale * coordinate_system.basis[i, 2],
                                      coordinate_system.labels[i],
                                      color=label_col[i],
                                      scale=0.1 * glyph_scale))
    return arrows, labels


def draw_coordinate_system_box(fig, coordinate_system, offset=0.5, scale=1.0, draw_axes=True, draw_labels=True):
    mlab.figure(fig, bgcolor=fig.scene.background)
    cube_points, dims = generators.generate_cuboid(scale, scale, scale,
                                                   origin=np.array([scale/2, scale/2, scale/2]))
    cube = tvtk.StructuredGrid(dimensions=dims)
    cube.points = np.asarray(coordinate_system.to_parent(cube_points))
    color = euler_color(coordinate_system.euler_angles)
    cube_surface = mlab.pipeline.surface(cube, color=color)
    cube_surface.parent.parent.name = 'Euler colored box: ' + coordinate_system.name
    cube_surface.actor.property.edge_visibility = 1
    cube_surface.actor.property.edge_color = color
    arrows, labels = None, None
    if draw_axes:
        arrows, labels = draw_coordinate_system_axes(fig, coordinate_system, offset=offset, scale=scale,
                                                     draw_labels=draw_labels)
    return cube_surface, arrows, labels


def update_coordinate_system_axes(coordinate_system, arrows, labels, offset=0.0, scale=1.0):
    points, lengths = coordinate_system_arrows(coordinate_system, offset=offset, scale=scale)
    data = arrows.parent.parent
    data.mlab_source.points = points
    data.mlab_source.u = lengths[0, :]
    data.mlab_source.v = lengths[1, :]
    data.mlab_source.w = lengths[2, :]
    glyph_scale = arrows.glyph.glyph.scale_factor * 1.1
    for i in range(len(labels)):
        labels[i].position = points[i, :] + glyph_scale * np.asarray(coordinate_system.basis[i, :])
        labels[i].scale = np.ones(3) * 0.1 * glyph_scale
    return arrows, labels


def update_coordinate_system_box(coordinate_system, cube_surface, arrows, labels, offset=0.5, scale=1.0):
    cube_points, dims = generators.generate_cuboid(scale, scale, scale,
                                                   origin=np.array([scale/2, scale/2, scale/2]))
    color = euler_color(coordinate_system.euler_angles)
    cube_surface.parent.parent.data.set(points=np.asarray(coordinate_system.to_parent(cube_points)))
    cube_surface.actor.property.edge_visibility = 1
    cube_surface.actor.property.edge_color = color
    cube_surface.actor.property.color = color
    if arrows is None:
        return cube_surface, arrows, labels
    else:
        arrows, labels = update_coordinate_system_axes(coordinate_system, arrows, labels, offset=offset, scale=scale)
    return cube_surface, arrows, labels
