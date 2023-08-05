"""
.. module:: operations
    :platform: Unix, Windows
    :synopsis: Provides geometric operations for spline geometry classes

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

import math
import copy
import warnings
from . import abstract
from . import multi
from . import helpers
from . import evaluators
from . import linalg
from . import compatibility
from . import _operations
from .exceptions import GeomdlException


def insert_knot(obj, param, num, **kwargs):
    """ Inserts knots n-times to a spline geometry.

    :param obj: spline geometry
    :param param: knot(s) to be inserted
    :param num: number of knot insertions
    :return: updated spline geometry
    """
    # Get keyword arguments
    check_num = kwargs.get('check_num', True)  # can be set to False when the caller checks number of insertions

    if check_num:
        # Check the validity of number of insertions
        if not isinstance(num, (list, tuple)):
            raise GeomdlException("The number of insertions must be a list or a tuple",
                                  data=dict(num=num))

        if len(num) != obj.pdimension:
            raise GeomdlException("The length of the num array must be equal to the number of parametric dimensions",
                                  data=dict(pdim=obj.pdim, num_len=len(num)))

        for idx, val in enumerate(num):
            if val < 0:
                raise GeomdlException('Number of insertions must be a positive integer value',
                                      data=dict(idx=idx, num=val))

    # Start curve knot insertion
    if isinstance(obj, abstract.Curve):
        if param[0] is not None and num[0] > 0:
            # Find knot multiplicity
            s = helpers.find_multiplicity(param[0], obj.knotvector)

            # Check if it is possible add that many number of knots
            if check_num and num[0] > obj.degree - s:
                raise GeomdlException("Knot " + str(param[0]) + " cannot be inserted " + str(num[0]) + " times",
                                      data=dict(knot=param[0], num=num[0], multiplicity=s))

            # Find knot span
            span = helpers.find_span_linear(obj.degree, obj.knotvector, obj.ctrlpts_size, param[0])

            # Compute new knot vector
            kv_new = helpers.knot_insertion_kv(obj.knotvector, param[0], span, num[0])

            # Compute new control points
            cpts = obj.ctrlptsw if obj.rational else obj.ctrlpts
            cpts_tmp = helpers.knot_insertion(obj.degree, obj.knotvector, cpts, param[0],
                                              num=num[0], s=s, span=span)

            # Update curve
            obj.set_ctrlpts(cpts_tmp)
            obj.knotvector = kv_new

    # Start surface knot insertion
    if isinstance(obj, abstract.Surface):
        # u-direction
        if param[0] is not None and num[0] > 0:
            # Find knot multiplicity
            s_u = helpers.find_multiplicity(param[0], obj.knotvector_u)

            # Check if it is possible add that many number of knots
            if check_num and num[0] > obj.degree_u - s_u:
                raise GeomdlException("Knot " + str(param[0]) + " cannot be inserted " + str(num[0]) + " times (u-dir)",
                                      data=dict(knot=param[0], num=num[0], multiplicity=s_u))

            # Find knot span
            span_u = helpers.find_span_linear(obj.degree_u, obj.knotvector_u, obj.ctrlpts_size_u, param[0])

            # Compute new knot vector
            kv_u = helpers.knot_insertion_kv(obj.knotvector_u, param[0], span_u, num[0])

            # Get curves
            cpts_tmp = []
            cpts = obj.ctrlptsw if obj.rational else obj.ctrlpts
            for v in range(obj.ctrlpts_size_v):
                ccu = [cpts[v + (obj.ctrlpts_size_v * u)] for u in range(obj.ctrlpts_size_u)]
                ctrlpts_tmp = helpers.knot_insertion(obj.degree_u, obj.knotvector_u, ccu, param[0],
                                                     num=num[0], s=s_u, span=span_u)
                cpts_tmp += ctrlpts_tmp

            # Update the surface after knot insertion
            obj.set_ctrlpts(compatibility.flip_ctrlpts_u(cpts_tmp, obj.ctrlpts_size_u + num[0], obj.ctrlpts_size_v),
                            obj.ctrlpts_size_u + num[0], obj.ctrlpts_size_v)
            obj.knotvector_u = kv_u

        # v-direction
        if param[1] is not None and num[1] > 0:
            # Find knot multiplicity
            s_v = helpers.find_multiplicity(param[1], obj.knotvector_v)

            # Check if it is possible add that many number of knots
            if check_num and num[1] > obj.degree_v - s_v:
                raise GeomdlException("Knot " + str(param[1]) + " cannot be inserted " + str(num[1]) + " times (v-dir)",
                                      data=dict(knot=param[1], num=num[1], multiplicity=s_v))

            # Find knot span
            span_v = helpers.find_span_linear(obj.degree_v, obj.knotvector_v, obj.ctrlpts_size_v, param[1])

            # Compute new knot vector
            kv_v = helpers.knot_insertion_kv(obj.knotvector_v, param[1], span_v, num[1])

            # Get curves
            cpts_tmp = []
            cpts = obj.ctrlptsw if obj.rational else obj.ctrlpts
            for u in range(obj.ctrlpts_size_u):
                ccv = [cpts[v + (obj.ctrlpts_size_v * u)] for v in range(obj.ctrlpts_size_v)]
                ctrlpts_tmp = helpers.knot_insertion(obj.degree_v, obj.knotvector_v, ccv, param[1],
                                                     num=num[1], s=s_v, span=span_v)
                cpts_tmp += ctrlpts_tmp

            # Update the surface after knot insertion
            obj.set_ctrlpts(cpts_tmp, obj.ctrlpts_size_u, obj.ctrlpts_size_v + num[1])
            obj.knotvector_v = kv_v

    # Start volume knot insertion
    if isinstance(obj, abstract.Volume):
        # u-direction
        if param[0] is not None and num[0] > 0:
            # Find knot multiplicity
            s_u = helpers.find_multiplicity(param[0], obj.knotvector_u)

            # Check if it is possible add that many number of knots
            if check_num and num[0] > obj.degree_u - s_u:
                raise GeomdlException("Knot " + str(param[0]) + " cannot be inserted " + str(num[0]) + " times (u-dir)",
                                      data=dict(knot=param[0], num=num[0], multiplicity=s_u))

            # Find knot span
            span_u = helpers.find_span_linear(obj.degree_u, obj.knotvector_u, obj.ctrlpts_size_u, param[0])

            # Compute new knot vector
            kv_u = helpers.knot_insertion_kv(obj.knotvector_u, param[0], span_u, num[0])

            # Use Pw if rational
            cpts = obj.ctrlptsw if obj.rational else obj.ctrlpts

            # Construct 2-dimensional structure
            cpt2d = []
            for u in range(obj.ctrlpts_size_u):
                temp_surf = []
                for w in range(obj.ctrlpts_size_w):
                    for v in range(obj.ctrlpts_size_v):
                        temp_pt = cpts[v + (u * obj.ctrlpts_size_v) + (w * obj.ctrlpts_size_u * obj.ctrlpts_size_v)]
                        temp_surf.append(temp_pt)
                cpt2d.append(temp_surf)

            # Compute new control points
            ctrlpts_tmp = helpers.knot_insertion(obj.degree_u, obj.knotvector_u, cpt2d, param[0],
                                                 num=num[0], s=s_u, span=span_u)

            # Flatten to 1-dimensional structure
            ctrlpts_new = []
            for w in range(obj.ctrlpts_size_w):
                for u in range(obj.ctrlpts_size_u + num[0]):
                    for v in range(obj.ctrlpts_size_v):
                        temp_pt = ctrlpts_tmp[u][v + (w * obj.ctrlpts_size_v)]
                        ctrlpts_new.append(temp_pt)

            # Update the volume after knot insertion
            obj.set_ctrlpts(ctrlpts_new, obj.ctrlpts_size_u + num[0], obj.ctrlpts_size_v, obj.ctrlpts_size_w)
            obj.knotvector_u = kv_u

        # v-direction
        if param[1] is not None and num[1] > 0:
            # Find knot multiplicity
            s_v = helpers.find_multiplicity(param[1], obj.knotvector_v)

            # Check if it is possible add that many number of knots
            if check_num and num[1] > obj.degree_v - s_v:
                raise GeomdlException("Knot " + str(param[1]) + " cannot be inserted " + str(num[1]) + " times (v-dir)",
                                      data=dict(knot=param[1], num=num[1], multiplicity=s_v))

            # Find knot span
            span_v = helpers.find_span_linear(obj.degree_v, obj.knotvector_v, obj.ctrlpts_size_v, param[1])

            # Compute new knot vector
            kv_v = helpers.knot_insertion_kv(obj.knotvector_v, param[1], span_v, num[1])

            # Use Pw if rational
            cpts = obj.ctrlptsw if obj.rational else obj.ctrlpts

            # Construct 2-dimensional structure
            cpt2d = []
            for v in range(obj.ctrlpts_size_v):
                temp_surf = []
                for w in range(obj.ctrlpts_size_w):
                    for u in range(obj.ctrlpts_size_u):
                        temp_pt = cpts[v + (u * obj.ctrlpts_size_v) + (w * obj.ctrlpts_size_u * obj.ctrlpts_size_v)]
                        temp_surf.append(temp_pt)
                cpt2d.append(temp_surf)

            # Compute new control points
            ctrlpts_tmp = helpers.knot_insertion(obj.degree_v, obj.knotvector_v, cpt2d, param[1],
                                                 num=num[1], s=s_v, span=span_v)

            # Flatten to 1-dimensional structure
            ctrlpts_new = []
            for w in range(obj.ctrlpts_size_w):
                for u in range(obj.ctrlpts_size_u):
                    for v in range(obj.ctrlpts_size_v + num[1]):
                        temp_pt = ctrlpts_tmp[v][u + (w * obj.ctrlpts_size_u)]
                        ctrlpts_new.append(temp_pt)

            # Update the volume after knot insertion
            obj.set_ctrlpts(ctrlpts_new, obj.ctrlpts_size_u, obj.ctrlpts_size_v + num[1], obj.ctrlpts_size_w)
            obj.knotvector_v = kv_v

        # w-direction
        if param[2] is not None and num[2] > 0:
            # Find knot multiplicity
            s_w = helpers.find_multiplicity(param[2], obj.knotvector_w)

            # Check if it is possible add that many number of knots
            if check_num and num[2] > obj.degree_w - s_w:
                raise GeomdlException("Knot " + str(param[2]) + " cannot be inserted " + str(num[2]) + " times (w-dir)",
                                      data=dict(knot=param[2], num=num[2], multiplicity=s_w))

            # Find knot span
            span_w = helpers.find_span_linear(obj.degree_w, obj.knotvector_w, obj.ctrlpts_size_w, param[2])

            # Compute new knot vector
            kv_w = helpers.knot_insertion_kv(obj.knotvector_w, param[2], span_w, num[2])

            # Use Pw if rational
            cpts = obj.ctrlptsw if obj.rational else obj.ctrlpts

            # Construct 2-dimensional structure
            cpt2d = []
            for w in range(obj.ctrlpts_size_w):
                temp_surf = [cpts[uv + (w * obj.ctrlpts_size_u * obj.ctrlpts_size_v)] for uv in
                             range(obj.ctrlpts_size_u * obj.ctrlpts_size_v)]
                cpt2d.append(temp_surf)

            # Compute new control points
            ctrlpts_tmp = helpers.knot_insertion(obj.degree_w, obj.knotvector_w, cpt2d, param[2],
                                                 num=num[2], s=s_w, span=span_w)

            # Flatten to 1-dimensional structure
            ctrlpts_new = []
            for w in range(obj.ctrlpts_size_w + num[2]):
                ctrlpts_new += ctrlpts_tmp[w]

            # Update the volume after knot insertion
            obj.set_ctrlpts(ctrlpts_new, obj.ctrlpts_size_u, obj.ctrlpts_size_v, obj.ctrlpts_size_w + num[2])
            obj.knotvector_w = kv_w

    # Return updated spline geometry
    return obj


def remove_knot(obj, param, num, **kwargs):
    """ Removes knots n-times from a spline geometry.

    :param obj: spline geometry
    :param param: knot(s) to be removed
    :param num: number of knot removals
    :return: updated spline geometry
    """
    # Get keyword arguments
    check_num = kwargs.get('check_num', True)  # can be set to False when the caller checks number of removals

    if check_num:
        # Check the validity of number of insertions
        if not isinstance(num, (list, tuple)):
            raise GeomdlException("The number of removals must be a list or a tuple",
                                  data=dict(num=num))

        if len(num) != obj.pdimension:
            raise GeomdlException("The length of the num array must be equal to the number of parametric dimensions",
                                  data=dict(pdim=obj.pdim, num_len=len(num)))

        for idx, val in enumerate(num):
            if val < 0:
                raise GeomdlException('Number of removals  must be a positive integer value',
                                      data=dict(idx=idx, num=val))

    # Start curve knot removal
    if isinstance(obj, abstract.Curve):
        if param[0] is not None and num[0] > 0:
            # Find knot multiplicity
            s = helpers.find_multiplicity(param[0], obj.knotvector)

            # It is impossible to remove knots if num > s
            if check_num and num[0] > s:
                raise GeomdlException("Knot " + str(param[0]) + " cannot be removed " + str(num[0]) + " times",
                                      data=dict(knot=param[0], num=num[0], multiplicity=s))

            # Find knot span
            span = helpers.find_span_linear(obj.degree, obj.knotvector, obj.ctrlpts_size, param[0])

            # Compute new control points
            cpts = obj.ctrlptsw if obj.rational else obj.ctrlpts
            ctrlpts_new = helpers.knot_removal(obj.degree, obj.knotvector, cpts, param[0], num=num[0], s=s, span=span)

            # Compute new knot vector
            kv_new = helpers.knot_removal_kv(obj.knotvector, span, num[0])

            # Update curve
            obj.set_ctrlpts(ctrlpts_new)
            obj.knotvector = kv_new

    # Start surface knot removal
    if isinstance(obj, abstract.Surface):
        # u-direction
        if param[0] is not None and num[0] > 0:
            # Find knot multiplicity
            s_u = helpers.find_multiplicity(param[0], obj.knotvector_u)

            # Check if it is possible add that many number of knots
            if check_num and num[0] > s_u:
                raise GeomdlException("Knot " + str(param[0]) + " cannot be removed " + str(num[0]) + " times (u-dir)",
                                      data=dict(knot=param[0], num=num[0], multiplicity=s_u))

            # Find knot span
            span_u = helpers.find_span_linear(obj.degree_u, obj.knotvector_u, obj.ctrlpts_size_u, param[0])

            # Get curves
            ctrlpts_new = []
            cpts = obj.ctrlptsw if obj.rational else obj.ctrlpts
            for v in range(obj.ctrlpts_size_v):
                ccu = [cpts[v + (obj.ctrlpts_size_v * u)] for u in range(obj.ctrlpts_size_u)]
                ctrlpts_tmp = helpers.knot_removal(obj.degree_u, obj.knotvector_u, ccu, param[0],
                                                   num=num[0], s=s_u, span=span_u)
                ctrlpts_new += ctrlpts_tmp

            # Compute new knot vector
            kv_u = helpers.knot_removal_kv(obj.knotvector_u, span_u, num[0])

            # Update the surface after knot removal
            obj.set_ctrlpts(compatibility.flip_ctrlpts_u(ctrlpts_new, obj.ctrlpts_size_u + num[0], obj.ctrlpts_size_v),
                            obj.ctrlpts_size_u + num[0], obj.ctrlpts_size_v)
            obj.knotvector_u = kv_u

        # v-direction
        if param[1] is not None and num[1] > 0:
            # Find knot multiplicity
            s_v = helpers.find_multiplicity(param[1], obj.knotvector_v)

            # Check if it is possible add that many number of knots
            if check_num and num[1] > s_v:
                raise GeomdlException("Knot " + str(param[1]) + " cannot be removed " + str(num[1]) + " times (v-dir)",
                                      data=dict(knot=param[1], num=num[1], multiplicity=s_v))

            # Find knot span
            span_v = helpers.find_span_linear(obj.degree_v, obj.knotvector_v, obj.ctrlpts_size_v, param[1])

            # Get curves
            ctrlpts_new = []
            cpts = obj.ctrlptsw if obj.rational else obj.ctrlpts
            for u in range(obj.ctrlpts_size_u):
                ccv = [cpts[v + (obj.ctrlpts_size_v * u)] for v in range(obj.ctrlpts_size_v)]
                ctrlpts_tmp = helpers.knot_removal(obj.degree_v, obj.knotvector_v, ccv, param[1],
                                                   num=num[1], s=s_v, span=span_v)
                ctrlpts_new += ctrlpts_tmp

            # Compute new knot vector
            kv_v = helpers.knot_removal_kv(obj.knotvector_v, span_v, num[1])

            # Update the surface after knot removal
            obj.set_ctrlpts(ctrlpts_new, obj.ctrlpts_size_u, obj.ctrlpts_size_v + num[1])
            obj.knotvector_v = kv_v

    # Start volume knot removal
    if isinstance(obj, abstract.Volume):
        # u-direction
        if param[0] is not None and num[0] > 0:
            # Find knot multiplicity
            s_u = helpers.find_multiplicity(param[0], obj.knotvector_u)

            # Check if it is possible add that many number of knots
            if check_num and num[0] > s_u:
                raise GeomdlException("Knot " + str(param[0]) + " cannot be removed " + str(num[0]) + " times (u-dir)",
                                      data=dict(knot=param[0], num=num[0], multiplicity=s_u))

            # Find knot span
            span_u = helpers.find_span_linear(obj.degree_u, obj.knotvector_u, obj.ctrlpts_size_u, param[0])

            # Use Pw if rational
            cpts = obj.ctrlptsw if obj.rational else obj.ctrlpts

        # v-direction
        if param[1] is not None and num[1] > 0:
            # Find knot multiplicity
            s_v = helpers.find_multiplicity(param[1], obj.knotvector_v)

            # Check if it is possible add that many number of knots
            if check_num and num[1] > s_v:
                raise GeomdlException("Knot " + str(param[1]) + " cannot be removed " + str(num[1]) + " times (v-dir)",
                                      data=dict(knot=param[1], num=num[1], multiplicity=s_v))

            # Find knot span
            span_v = helpers.find_span_linear(obj.degree_v, obj.knotvector_v, obj.ctrlpts_size_v, param[1])

            # Use Pw if rational
            cpts = obj.ctrlptsw if obj.rational else obj.ctrlpts

        # w-direction
        if param[2] is not None and num[2] > 0:
            # Find knot multiplicity
            s_w = helpers.find_multiplicity(param[2], obj.knotvector_w)

            # Check if it is possible add that many number of knots
            if check_num and num[2] > s_w:
                raise GeomdlException("Knot " + str(param[2]) + " cannot be removed " + str(num[2]) + " times (w-dir)",
                                      data=dict(knot=param[2], num=num[2], multiplicity=s_w))

            # Find knot span
            span_w = helpers.find_span_linear(obj.degree_w, obj.knotvector_w, obj.ctrlpts_size_w, param[2])

            # Use Pw if rational
            cpts = obj.ctrlptsw if obj.rational else obj.ctrlpts

            # # Compute new control points
            # ctrlpts_new = []
            #
            # # Compute new knot vector
            # kv_w = helpers.knot_removal_kv(obj.knotvector_w, span_w, num[2])
            #
            # # Update the volume after knot insertion
            # obj.set_ctrlpts(ctrlpts_new, obj.ctrlpts_size_u, obj.ctrlpts_size_v, obj.ctrlpts_size_w + num[2])
            # obj.knotvector_w = kv_w

    # Return updated spline geometry
    return obj


def split_curve(obj, param, **kwargs):
    """ Splits the curve at the input parametric coordinate.

    This method splits the curve into two pieces at the given parametric coordinate, generates two different
    curve objects and returns them. It does not modify the input curve.

    :param obj: Curve to be split
    :type obj: abstract.Curve
    :param param: parameter
    :type param: float
    :return: list of curves as the split pieces of the initial curve
    :rtype: list
    """
    # Validate input
    if not isinstance(obj, abstract.Curve):
        raise TypeError("Input shape must be an instance of abstract.Curve class")

    if param == obj.knotvector[0] or param == obj.knotvector[-1]:
        raise ValueError("Cannot split on the corner points")

    # Keyword arguments
    span_func = kwargs.get('find_span_func', helpers.find_span_linear)

    # Find multiplicity of the knot and define how many times we need to add the knot
    ks = span_func(obj.degree, obj.knotvector, len(obj.ctrlpts), param) - obj.degree + 1
    s = helpers.find_multiplicity(param, obj.knotvector)
    r = obj.degree - s

    # Create backups of the original curve
    temp_obj = copy.deepcopy(obj)

    # Insert knot
    insert_knot(temp_obj, [param], num=[r], check_num=False)

    # Knot vectors
    knot_span = span_func(temp_obj.degree, temp_obj.knotvector, len(temp_obj.ctrlpts), param) + 1
    curve1_kv = list(temp_obj.knotvector[0:knot_span])
    curve1_kv.append(param)
    curve2_kv = list(temp_obj.knotvector[knot_span:])
    for _ in range(0, temp_obj.degree + 1):
        curve2_kv.insert(0, param)

    # Control points (use private variable due to differences between rational and non-rational curve)
    curve1_ctrlpts = temp_obj._control_points[0:ks + r]
    curve2_ctrlpts = temp_obj._control_points[ks + r - 1:]

    # Create a new curve for the first half
    curve1 = temp_obj.__class__()
    curve1.degree = temp_obj.degree
    curve1.set_ctrlpts(curve1_ctrlpts)
    curve1.knotvector = curve1_kv

    # Create another curve fot the second half
    curve2 = temp_obj.__class__()
    curve2.degree = temp_obj.degree
    curve2.set_ctrlpts(curve2_ctrlpts)
    curve2.knotvector = curve2_kv

    # Return the split curves
    ret_val = [curve1, curve2]
    return ret_val


def decompose_curve(obj, **kwargs):
    """ Decomposes the curve into Bezier curve segments of the same degree.

    This operation does not modify the input curve, instead it returns the split curve segments.

    :param obj: Curve to be decomposed
    :type obj: abstract.Curve
    :return: a list of curve objects arranged in Bezier curve segments
    :rtype: list
    """
    if not isinstance(obj, abstract.Curve):
        raise TypeError("Input shape must be an instance of abstract.Curve class")

    multi_curve = []
    curve = copy.deepcopy(obj)
    knots = curve.knotvector[curve.degree + 1:-(curve.degree + 1)]
    while knots:
        knot = knots[0]
        curves = split_curve(curve, param=knot, **kwargs)
        multi_curve.append(curves[0])
        curve = curves[1]
        knots = curve.knotvector[curve.degree + 1:-(curve.degree + 1)]
    multi_curve.append(curve)

    return multi_curve


def derivative_curve(obj):
    """ Computes the hodograph (first derivative) curve of the input curve.

    This function constructs the hodograph (first derivative) curve from the input curve by computing the degrees,
    knot vectors and the control points of the derivative curve.

    :param obj: input curve
    :type obj: abstract.Curve
    :return: derivative curve
    """
    if not isinstance(obj, abstract.Curve):
        raise TypeError("Input shape must be an instance of abstract.Curve class")

    # Unfortunately, rational curves do NOT have this property
    # Ref: https://pages.mtu.edu/~shene/COURSES/cs3621/LAB/curve/1st-2nd.html
    if obj.rational:
        warnings.warn("Cannot compute hodograph curve for a rational curve")
        return obj

    # Find the control points of the derivative curve
    pkl = evaluators.CurveEvaluator2.derivatives_ctrlpts(r1=0,
                                                         r2=len(obj.ctrlpts) - 1,  # n + 1 = num of control points
                                                         degree=obj.degree,
                                                         knotvector=obj.knotvector,
                                                         ctrlpts=obj.ctrlpts,
                                                         dimension=obj.dimension,
                                                         deriv_order=1)

    # Generate the derivative curve
    curve = obj.__class__()
    curve.degree = obj.degree - 1
    curve.ctrlpts = pkl[1][0:-1]
    curve.knotvector = obj.knotvector[1:-1]
    curve.delta = obj.delta

    return curve


def length_curve(obj):
    """ Computes the approximate length of the parametric curve.

    Uses the following equation to compute the approximate length:

    .. math::

        \\sum_{i=0}^{n-1} \\sqrt{P_{i + 1}^2-P_{i}^2}

    where :math:`n` is number of evaluated curve points and :math:`P` is the n-dimensional point.

    :param obj: input curve
    :type obj: abstract.Curve
    :return: length
    :rtype: float
    """
    if not isinstance(obj, abstract.Curve):
        raise TypeError("Input shape must be an instance of abstract.Curve class")

    length = 0.0
    evalpts = obj.evalpts
    num_evalpts = len(obj.evalpts)
    for idx in range(num_evalpts - 1):
        length += linalg.point_distance(evalpts[idx], evalpts[idx + 1])
    return length


def add_dimension(obj, **kwargs):
    """ Converts x-dimensional curve to a (x+1)-dimensional curve.

    If you pass ``inplace=True`` keyword argument, the input shape will be updated. Otherwise, this function does not
    change the input shape but returns a new instance of the same shape with the updated data.

    Useful when converting a 2-dimensional curve to a 3-dimensional curve. Please note that this function does not
    change the parametric dimension but only the spatial dimension.

    :param obj: Curve
    :type obj: abstract.Curve
    :return: updated Curve
    :rtype: BSpline.Curve or NURBS.Curve
    """
    if not isinstance(obj, abstract.Curve):
        raise TypeError("Input shape must be an instance of abstract.Curve class")

    # Keyword arguments
    inplace = kwargs.get('inplace', False)
    array_init = kwargs.get('array_init', [[] for _ in range(len(obj.ctrlpts))])
    offset_value = kwargs.get('offset', 0.0)

    # Update control points
    new_ctrlpts = array_init
    for idx, point in enumerate(obj.ctrlpts):
        temp = [float(p) for p in point[0:obj.dimension]]
        temp.append(offset_value)
        new_ctrlpts[idx] = temp

    if inplace:
        obj.ctrlpts = new_ctrlpts
        return obj
    else:
        ret = copy.deepcopy(obj)
        ret.ctrlpts = new_ctrlpts
        return ret


def split_surface_u(obj, param, **kwargs):
    """ Splits the surface at the input parametric coordinate on the u-direction.

    This method splits the surface into two pieces at the given parametric coordinate on the u-direction,
    generates two different surface objects and returns them. It does not modify the input surface.

    :param obj: surface
    :type obj: abstract.Surface
    :param param: parameter for the u-direction
    :type param: float
    :return: list of surface as the split pieces of the initial surface
    :rtype: list
    """
    # Validate input
    if not isinstance(obj, abstract.Surface):
        raise TypeError("Input shape must be an instance of abstract.Surface class")

    if param == obj.knotvector_u[0] or param == obj.knotvector_u[-1]:
        raise ValueError("Cannot split on the edge")

    # Keyword arguments
    span_func = kwargs.get('find_span_func', helpers.find_span_linear)

    # Find multiplicity of the knot
    ks = span_func(obj.degree_u, obj.knotvector_u, obj.ctrlpts_size_u, param) - obj.degree_u + 1
    s = helpers.find_multiplicity(param, obj.knotvector_u)
    r = obj.degree_u - s

    # Create backups of the original surface
    temp_obj = copy.deepcopy(obj)

    # Split the original surface
    insert_knot(temp_obj, [param, None], num=[r, 0], check_num=False)

    # Knot vectors
    knot_span = span_func(temp_obj.degree_u, temp_obj.knotvector_u, temp_obj.ctrlpts_size_u, param) + 1
    surf1_kv = list(temp_obj.knotvector_u[0:knot_span])
    surf1_kv.append(param)
    surf2_kv = list(temp_obj.knotvector_u[knot_span:])
    for _ in range(0, temp_obj.degree_u + 1):
        surf2_kv.insert(0, param)

    # Control points
    surf1_ctrlpts = temp_obj.ctrlpts2d[0:ks + r]
    surf2_ctrlpts = temp_obj.ctrlpts2d[ks + r - 1:]

    # Create a new surface for the first half
    surf1 = temp_obj.__class__()
    surf1.degree_u = temp_obj.degree_u
    surf1.degree_v = temp_obj.degree_v
    surf1.ctrlpts2d = surf1_ctrlpts
    surf1.knotvector_u = surf1_kv
    surf1.knotvector_v = temp_obj.knotvector_v

    # Create another surface fot the second half
    surf2 = temp_obj.__class__()
    surf2.degree_u = temp_obj.degree_u
    surf2.degree_v = temp_obj.degree_v
    surf2.ctrlpts2d = surf2_ctrlpts
    surf2.knotvector_u = surf2_kv
    surf2.knotvector_v = temp_obj.knotvector_v

    # Return the new surfaces
    ret_val = [surf1, surf2]
    return ret_val


def split_surface_v(obj, param, **kwargs):
    """ Splits the surface at the input parametric coordinate on the v-direction.

    This method splits the surface into two pieces at the given parametric coordinate on the v-direction,
    generates two different surface objects and returns them. It does not modify the input surface.

    :param obj: surface
    :type obj: abstract.Surface
    :param param: parameter for the v-direction
    :type param: float
    :return: list of surface as the split pieces of the initial surface
    :rtype: list
    """
    # Validate input
    if not isinstance(obj, abstract.Surface):
        raise TypeError("Input shape must be an instance of abstract.Surface class")

    if param == obj.knotvector_v[0] or param == obj.knotvector_v[-1]:
        raise ValueError("Cannot split on the edge")

    # Keyword arguments
    span_func = kwargs.get('find_span_func', helpers.find_span_linear)

    # Find multiplicity of the knot
    ks = span_func(obj.degree_v, obj.knotvector_v, obj.ctrlpts_size_v, param) - obj.degree_v + 1
    s = helpers.find_multiplicity(param, obj.knotvector_v)
    r = obj.degree_v - s

    # Create backups of the original surface
    temp_obj = copy.deepcopy(obj)

    # Split the original surface
    insert_knot(temp_obj, [None, param], num=[0, r], check_num=False)

    # Knot vectors
    knot_span = span_func(temp_obj.degree_v, temp_obj.knotvector_v, temp_obj.ctrlpts_size_v, param) + 1
    surf1_kv = list(temp_obj.knotvector_v[0:knot_span])
    surf1_kv.append(param)
    surf2_kv = list(temp_obj.knotvector_v[knot_span:])
    for _ in range(0, temp_obj.degree_v + 1):
        surf2_kv.insert(0, param)

    # Control points
    surf1_ctrlpts = []
    for v_row in temp_obj.ctrlpts2d:
        temp = v_row[0:ks + r]
        surf1_ctrlpts.append(temp)
    surf2_ctrlpts = []
    for v_row in temp_obj.ctrlpts2d:
        temp = v_row[ks + r - 1:]
        surf2_ctrlpts.append(temp)

    # Create a new surface for the first half
    surf1 = temp_obj.__class__()
    surf1.degree_u = temp_obj.degree_u
    surf1.degree_v = temp_obj.degree_v
    surf1.ctrlpts2d = surf1_ctrlpts
    surf1.knotvector_v = surf1_kv
    surf1.knotvector_u = temp_obj.knotvector_u

    # Create another surface fot the second half
    surf2 = temp_obj.__class__()
    surf2.degree_u = temp_obj.degree_u
    surf2.degree_v = temp_obj.degree_v
    surf2.ctrlpts2d = surf2_ctrlpts
    surf2.knotvector_v = surf2_kv
    surf2.knotvector_u = temp_obj.knotvector_u

    # Return the new surfaces
    ret_val = [surf1, surf2]
    return ret_val


def decompose_surface(obj, **kwargs):
    """ Decomposes the surface into Bezier surface patches of the same degree.

    This operation does not modify the input surface, instead it returns the surface patches.

    :param obj: surface
    :type obj: abstract.Surface
    :return: a list of surface objects arranged as Bezier surface patches
    :rtype: multi.SurfaceContainer
    """
    # Validate input
    if not isinstance(obj, abstract.Surface):
        raise TypeError("Input shape must be an instance of abstract.Surface class")

    # Work with an identical copy
    surf = copy.deepcopy(obj)

    surf_list = []

    # Process u-direction
    knots_u = surf.knotvector_u[surf.degree_u + 1:-(surf.degree_u + 1)]
    while knots_u:
        knot = knots_u[0]
        surfs = split_surface_u(surf, param=knot, **kwargs)
        surf_list.append(surfs[0])
        surf = surfs[1]
        knots_u = surf.knotvector_u[surf.degree_u + 1:-(surf.degree_u + 1)]
    surf_list.append(surf)

    # Process v-direction
    multi_surf = []
    for surf in surf_list:
        knots_v = surf.knotvector_v[surf.degree_v + 1:-(surf.degree_v + 1)]
        while knots_v:
            knot = knots_v[0]
            surfs = split_surface_v(surf, param=knot, **kwargs)
            multi_surf.append(surfs[0])
            surf = surfs[1]
            knots_v = surf.knotvector_v[surf.degree_v + 1:-(surf.degree_v + 1)]
        multi_surf.append(surf)

    return multi_surf


def derivative_surface(obj):
    """ Computes the hodograph (first derivative) surface of the input surface.

    This function constructs the hodograph (first derivative) surface from the input surface by computing the degrees,
    knot vectors and the control points of the derivative surface.

    The return value of this function is a tuple containing the following derivative surfaces in the given order:

    * U-derivative surface (derivative taken only on the u-direction)
    * V-derivative surface (derivative taken only on the v-direction)
    * UV-derivative surface (derivative taken on both the u- and the v-direction)

    :param obj: input surface
    :type obj: abstract.Surface
    :return: derivative surfaces w.r.t. u, v and both u-v
    :rtype: tuple
    """
    if not isinstance(obj, abstract.Surface):
        raise TypeError("Input shape must be an instance of abstract.Surface class")

    if obj.rational:
        warnings.warn("Cannot compute hodograph surface for a rational surface")
        return obj

    # Find the control points of the derivative surface
    d = 2  # 0 <= k + l <= d, see pg. 114 of The NURBS Book, 2nd Ed.
    pkl = evaluators.SurfaceEvaluator2.derivatives_ctrlpts(r1=0, r2=obj.ctrlpts_size_u - 1,
                                                           s1=0, s2=obj.ctrlpts_size_v - 1,
                                                           degree_u=obj.degree_u, degree_v=obj.degree_v,
                                                           ctrlpts_size_u=obj.ctrlpts_size_u,
                                                           ctrlpts_size_v=obj.ctrlpts_size_v,
                                                           knotvector_u=obj.knotvector_u, knotvector_v=obj.knotvector_v,
                                                           ctrlpts=obj.ctrlpts2d,
                                                           dimension=obj.dimension,
                                                           deriv_order=d)

    ctrlpts2d_u = []
    for i in range(0, len(pkl[1][0]) - 1):
        ctrlpts2d_u.append(pkl[1][0][i])

    surf_u = copy.deepcopy(obj)
    surf_u.degree_u = obj.degree_u - 1
    surf_u.ctrlpts2d = ctrlpts2d_u
    surf_u.knotvector_u = obj.knotvector_u[1:-1]
    surf_u.delta = obj.delta

    ctrlpts2d_v = []
    for i in range(0, len(pkl[0][1])):
        ctrlpts2d_v.append(pkl[0][1][i][0:-1])

    surf_v = copy.deepcopy(obj)
    surf_v.degree_v = obj.degree_v - 1
    surf_v.ctrlpts2d = ctrlpts2d_v
    surf_v.knotvector_v = obj.knotvector_v[1:-1]
    surf_v.delta = obj.delta

    ctrlpts2d_uv = []
    for i in range(0, len(pkl[1][1]) - 1):
        ctrlpts2d_uv.append(pkl[1][1][i][0:-1])

    # Generate the derivative curve
    surf_uv = obj.__class__()
    surf_uv.degree_u = obj.degree_u - 1
    surf_uv.degree_v = obj.degree_v - 1
    surf_uv.ctrlpts2d = ctrlpts2d_uv
    surf_uv.knotvector_u = obj.knotvector_u[1:-1]
    surf_uv.knotvector_v = obj.knotvector_v[1:-1]
    surf_uv.delta = obj.delta

    return surf_u, surf_v, surf_uv


def translate(obj, vec, **kwargs):
    """ Translates curves, surface or volumes by the input vector.

    If you pass ``inplace=True`` keyword argument, the input shape will be updated. Otherwise, this function does not
    change the input shape but returns a new instance of the same shape with the updated data.

    :param obj: input geometry
    :type obj: abstract.SplineGeometry or multi.AbstractContainer
    :param vec: translation vector
    :type vec: list, tuple
    :return: translated geometry object
    """
    # Input validity checks
    if not vec or not isinstance(vec, (tuple, list)):
        raise TypeError("The input must be a list or a tuple")

    if isinstance(obj, abstract.SplineGeometry):
        return _operations.translate_single(obj, vec, **kwargs)
    elif isinstance(obj, multi.AbstractContainer):
        return _operations.translate_multi(obj, vec, **kwargs)
    else:
        raise TypeError("The input shape must be a curve or a surface (single or multi)")


def tangent(obj, params, **kwargs):
    """ Evaluates the tangent vector of the curves or surfaces at the input parameter values.

    This function is designed to evaluate tangent vectors of the B-Spline and NURBS shapes at single or
    multiple parameter positions.

    :param obj: input shape
    :type obj: abstract.Curve or abstract.Surface
    :param params: parameters
    :type params: float, list or tuple
    :return: a list containing "point" and "vector" pairs
    :rtype: tuple
    """
    normalize = kwargs.get('normalize', True)
    if isinstance(obj, abstract.Curve):
        if isinstance(params, (list, tuple)):
            return _operations.tangent_curve_single_list(obj, params, normalize)
        else:
            return _operations.tangent_curve_single(obj, params, normalize)
    if isinstance(obj, abstract.Surface):
        if isinstance(params[0], float):
            return _operations.tangent_surface_single(obj, params, normalize)
        else:
            return _operations.tangent_surface_single_list(obj, params, normalize)


def normal(obj, params, **kwargs):
    """ Evaluates the normal vector of the curves or surfaces at the input parameter values.

    This function is designed to evaluate normal vectors of the B-Spline and NURBS shapes at single or
    multiple parameter positions.

    :param obj: input geometry
    :type obj: abstract.Curve or abstract.Surface
    :param params: parameters
    :type params: float, list or tuple
    :return: a list containing "point" and "vector" pairs
    :rtype: tuple
    """
    normalize = kwargs.get('normalize', True)
    if isinstance(obj, abstract.Curve):
        if isinstance(params, (list, tuple)):
            return _operations.normal_curve_single_list(obj, params, normalize)
        else:
            return _operations.normal_curve_single(obj, params, normalize)
    if isinstance(obj, abstract.Surface):
        if isinstance(params[0], float):
            return _operations.normal_surface_single(obj, params, normalize)
        else:
            return _operations.normal_surface_single_list(obj, params, normalize)


def binormal(obj, params, **kwargs):
    """ Evaluates the binormal vector of the curves or surfaces at the input parameter values.

    This function is designed to evaluate binormal vectors of the B-Spline and NURBS shapes at single or
    multiple parameter positions.

    :param obj: input shape
    :type obj: abstract.Curve or abstract.Surface
    :param params: parameters
    :type params: float, list or tuple
    :return: a list containing "point" and "vector" pairs
    :rtype: tuple
    """
    normalize = kwargs.get('normalize', True)
    if isinstance(obj, abstract.Curve):
        if isinstance(params, (list, tuple)):
            return _operations.binormal_curve_single_list(obj, params, normalize)
        else:
            return _operations.binormal_curve_single(obj, params, normalize)
    if isinstance(obj, abstract.Surface):
        raise NotImplementedError("Binormal vector evaluation for the surfaces is not implemented!")


def find_ctrlpts(obj, u, v=None, **kwargs):
    """ Finds the control points involved in the evaluation of the curve/surface point defined by the input parameter(s).

    :param obj: curve or surface
    :type obj: abstract.Curve or abstract.Surface
    :param u: parameter (for curve), parameter on the u-direction (for surface)
    :type u: float
    :param v: parameter on the v-direction (for surface only)
    :type v: float
    :return: control points; 1-dimensional array for curve, 2-dimensional array for surface
    :rtype: list
    """
    if isinstance(obj, abstract.Curve):
        return _operations.find_ctrlpts_curve(u, obj, **kwargs)
    elif isinstance(obj, abstract.Surface):
        if v is None:
            raise ValueError("Parameter value for the v-direction must be set for operating on surfaces")
        return _operations.find_ctrlpts_surface(u, v, obj, **kwargs)
    else:
        raise NotImplementedError("The input must be an instance of abstract.Curve or abstract.Surface")


def rotate(obj, angle, **kwargs):
    """ Rotates curves, surfaces or volumes about the chosen axis.

    Keyword Arguments:
        * ``axis``: rotation axis; x, y, z correspond to 0, 1, 2 respectively.
        * ``inplace``: if True, the input shape is modified. *Default: False*

    :param obj: input geometry
    :type obj: abstract.Curve, abstract.Surface or abstract.Volume
    :param angle: angle of rotation (in degrees)
    :type angle: float
    :return: rotated geometry object
    """
    def rotate_x(ncs, opt, alpha):
        # Generate translation vector
        translate_vector = linalg.vector_generate(opt, [0.0 for _ in range(ncs.dimension)])

        # Translate to the origin
        translate(ncs, translate_vector, inplace=True)

        # Then, rotate about the axis
        rot = math.radians(alpha)
        new_ctrlpts = [[0.0 for _ in range(ncs.dimension)] for _ in range(len(ncs.ctrlpts))]
        for idx, pt in enumerate(ncs.ctrlpts):
            new_ctrlpts[idx][0] = pt[0]
            new_ctrlpts[idx][1] = (pt[1] * math.cos(rot)) - (pt[2] * math.sin(rot))
            new_ctrlpts[idx][2] = (pt[2] * math.cos(rot)) + (pt[1] * math.sin(rot))
        ncs.ctrlpts = new_ctrlpts

        # Finally, translate back to the starting location
        translate(ncs, [-o for o in opt])

    def rotate_y(ncs, opt, alpha):
        # Generate translation vector
        translate_vector = linalg.vector_generate(opt, [0.0 for _ in range(ncs.dimension)])

        # Translate to the origin
        translate(ncs, translate_vector, inplace=True)

        # Then, rotate about the axis
        rot = math.radians(alpha)
        new_ctrlpts = [[0.0 for _ in range(ncs.dimension)] for _ in range(len(ncs.ctrlpts))]
        for idx, pt in enumerate(ncs.ctrlpts):
            new_ctrlpts[idx][0] = (pt[0] * math.cos(rot)) - (pt[2] * math.sin(rot))
            new_ctrlpts[idx][1] = pt[1]
            new_ctrlpts[idx][2] = (pt[2] * math.cos(rot)) + (pt[0] * math.sin(rot))
        ncs.ctrlpts = new_ctrlpts

        # Finally, translate back to the starting location
        translate(ncs, [-o for o in opt])

    def rotate_z(ncs, opt, alpha):
        # Generate translation vector
        translate_vector = linalg.vector_generate(opt, [0.0 for _ in range(ncs.dimension)])

        # Translate to the origin
        translate(ncs, translate_vector, inplace=True)

        # Then, rotate about the axis
        rot = math.radians(alpha)
        new_ctrlpts = [list(ncs.ctrlpts[i]) for i in range(len(ncs.ctrlpts))]
        for idx, pt in enumerate(ncs.ctrlpts):
            new_ctrlpts[idx][0] = (pt[0] * math.cos(rot)) - (pt[1] * math.sin(rot))
            new_ctrlpts[idx][1] = (pt[1] * math.cos(rot)) + (pt[0] * math.sin(rot))
        ncs.ctrlpts = new_ctrlpts

        # Finally, translate back to the starting location
        translate(ncs, [-o for o in opt])

    if isinstance(obj, (abstract.Curve, abstract.Surface, abstract.Volume)):
        origin = obj.evaluate_single(0.0)
    else:
        raise TypeError("Can only work with a single curve, surface or volume")

    axis = 2 if obj.dimension == 2 else kwargs.get('axis', 2)
    inplace = kwargs.get('inplace', False)

    if inplace:
        _obj = obj
    else:
        _obj = copy.deepcopy(obj)

    args = [_obj, origin, angle]
    if axis == 0:
        rotate_x(*args)
    elif axis == 1:
        rotate_y(*args)
    elif axis == 2:
        rotate_z(*args)
    else:
        raise ValueError("Value of the 'axis' argument should be 0, 1 or 2")

    return _obj


def scale(obj, multiplier, **kwargs):
    """ Scales curves, surfaces or volumes by the input multiplier.

    Keyword Arguments:
        * ``inplace``: if True, the input shape is modified. *Default: False*

    :param obj: input geometry
    :type obj: abstract.Curve, abstract.Surface or abstract.Volume
    :param multiplier: scaling multiplier
    :type multiplier: float
    :return: scaled geometry object
    """
    # Input validity checks
    if not isinstance(multiplier, (int, float)):
        raise TypeError("The multiplier must be a float or an integer")

    if isinstance(obj, abstract.SplineGeometry):
        return _operations.scale_single(obj, multiplier, **kwargs)
    elif isinstance(obj, multi.AbstractContainer):
        return _operations.scale_multi(obj, multiplier, **kwargs)
    else:
        raise TypeError("The input shape must be a curve or a surface (single or multi)")


def transpose(surf, **kwargs):
    """ Transposes the input surface by swapping u and v parametric directions.

    If you pass ``inplace=True`` keyword argument, the input surface will be updated. Otherwise, this function does not
    change the input surface but returns a new instance of the same surface with the updated data.

    :param surf: input surface
    :type surf: abstract.Surface
    :return: transposed surface
    :rtype: abstract.Surface
    """
    if not isinstance(surf, abstract.Surface):
        raise TypeError("Can only transpose single surfaces")

    inplace = kwargs.get('inplace', False)

    # Get existing data
    degree_u_new = surf.degree_v
    degree_v_new = surf.degree_u
    kv_u_new = surf.knotvector_v
    kv_v_new = surf.knotvector_u
    ctrlpts2d_old = surf.ctrlpts2d

    # Find new control points
    ctrlpts2d_new = []
    for v in range(0, surf.ctrlpts_size_v):
        ctrlpts_u = []
        for u in range(0, surf.ctrlpts_size_u):
            temp = ctrlpts2d_old[u][v]
            ctrlpts_u.append(temp)
        ctrlpts2d_new.append(ctrlpts_u)

    # Save transposed data
    if inplace:
        surf_t = surf
    else:
        surf_t = surf.__class__()
    surf_t.degree_u = degree_u_new
    surf_t.degree_v = degree_v_new
    surf_t.ctrlpts2d = ctrlpts2d_new
    surf_t.knotvector_u = kv_u_new
    surf_t.knotvector_v = kv_v_new

    return surf_t
