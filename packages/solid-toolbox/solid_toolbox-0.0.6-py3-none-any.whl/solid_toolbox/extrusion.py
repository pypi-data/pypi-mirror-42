#!/usr/bin/env python3

from solid import *
from solid.utils import *
from solid_toolbox.units import Vec2d, Vec
from solid_toolbox.poly import construct_polyhedron


def force_3d(vec):
    if isinstance(vec, Vec2d):
        return Vec(vec.x, vec.y, 0)
    else:
        return vec


def remove_adjacent_duplicates(items):
    total = len(items)
    if total <= 1:
        return items

    prev = items[0]
    out = [prev]
    for curr in items[1:]:
        if curr != prev:
            out.append(curr)
        prev = curr

    return out


def extrude_with_offsets(polygon_paths, extrusion_offset_paths):
    paths_3d = [force_3d(p) for p in polygon_paths]

    # We expect input paths to be given in clockwise order viewed from the
    # top-down -- so the bottom face needs to be reversed.
    bottom_face = [p + o for p, o in zip(paths_3d, extrusion_offset_paths[0])]
    faces = [list(reversed(bottom_face))]

    for offset_index in range(len(extrusion_offset_paths) - 1):
        offsets_lower = extrusion_offset_paths[offset_index]
        offsets_upper = extrusion_offset_paths[offset_index + 1]
        for i, (p1, p2) in enumerate(zip(paths_3d, paths_3d[1:])):
            lower1 = offsets_lower[i]
            lower2 = offsets_lower[i + 1]
            upper1 = offsets_upper[i]
            upper2 = offsets_upper[i + 1]

            # The face is usually a square defined by the following points:
            #
            # p2+upper2  -> p1+upper1
            #     ^             |
            #     |             V
            # p2+lower2  <-  p1+lower1
            #
            # We handle the case where two or more points coincide below.
            faces.append(
                [p1 + lower1, p2 + lower2, p2 + upper2, p1 + upper1, p1 + lower1]
            )

    faces.append([p + o for p, o in zip(paths_3d, extrusion_offset_paths[-1])])

    # Filter out any faces that are actually lines or points
    filtered_faces = []
    for face in faces:
        pruned_face = remove_adjacent_duplicates(face)
        if len(pruned_face) >= 4:
            filtered_faces.append(pruned_face)

    return construct_polyhedron(filtered_faces)
