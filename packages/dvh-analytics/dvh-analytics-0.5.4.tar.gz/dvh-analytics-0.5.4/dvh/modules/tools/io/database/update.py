#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
functions to update various columns in the SQL database
Created on Fri Dec 28 2018
@author: Dan Cutright, PhD
"""

from __future__ import print_function
from future.utils import listitems
import numpy as np
from sql_connector import DVH_SQL
from ...roi import geometry as roi_geom
from ...roi import formatter as roi_form


def centroid(study_instance_uid, roi_name):
    """
    This function will recalculate the centroid of an roi based on data in the SQL DB.
    :param study_instance_uid: uid as specified in SQL DB
    :param roi_name: roi_name as specified in SQL DB
    """

    coordinates_string = DVH_SQL().query('dvhs',
                                         'roi_coord_string',
                                         "study_instance_uid = '%s' and roi_name = '%s'"
                                         % (study_instance_uid, roi_name))

    roi = roi_form.get_planes_from_string(coordinates_string[0][0])
    data = roi_geom.centroid(roi)

    data = [str(round(v, 3)) for v in data]

    update_dvhs_table(study_instance_uid, roi_name, 'centroid', ','.join(data))


def cross_section(study_instance_uid, roi_name):
    """
    This function will recalculate the centoid of an roi based on data in the SQL DB.
    :param study_instance_uid: uid as specified in SQL DB
    :param roi_name: roi_name as specified in SQL DB
    """

    coordinates_string = DVH_SQL().query('dvhs',
                                         'roi_coord_string',
                                         "study_instance_uid = '%s' and roi_name = '%s'"
                                         % (study_instance_uid, roi_name))

    roi = roi_form.get_planes_from_string(coordinates_string[0][0])
    area = roi_geom.cross_section(roi)

    for key in ['max', 'median']:
        update_dvhs_table(study_instance_uid, roi_name, 'cross_section_%s' % key, area[key])


def spread(study_instance_uid, roi_name):
    """
    This function will recalculate the spread of an roi based on data in the SQL DB.
    :param study_instance_uid: uid as specified in SQL DB
    :param roi_name: roi_name as specified in SQL DB
    """

    coordinates_string = DVH_SQL().query('dvhs',
                                         'roi_coord_string',
                                         "study_instance_uid = '%s' and roi_name = '%s'"
                                         % (study_instance_uid, roi_name))

    roi = roi_form.get_planes_from_string(coordinates_string[0][0])
    data = roi_geom.spread(roi)

    data = [str(round(v/10., 3)) for v in data]

    for i, column in enumerate(['spread_x', 'spread_y', 'spread_z']):
        update_dvhs_table(study_instance_uid, roi_name, column, data[i])


def min_distances(study_instance_uid, roi_name):
    """
    This function will recalculate the min, mean, median, and max PTV distances an roi based on data in the SQL DB.
    :param study_instance_uid: uid as specified in SQL DB
    :param roi_name: roi_name as specified in SQL DB
    """

    oar_coordinates_string = DVH_SQL().query('dvhs',
                                             'roi_coord_string',
                                             "study_instance_uid = '%s' and roi_name = '%s'"
                                             % (study_instance_uid, roi_name))

    ptv_coordinates_strings = DVH_SQL().query('dvhs',
                                              'roi_coord_string',
                                              "study_instance_uid = '%s' and roi_type like 'PTV%%'"
                                              % study_instance_uid)

    if ptv_coordinates_strings:

        oar_coordinates = roi_form.get_roi_coordinates_from_string(oar_coordinates_string[0][0])

        ptvs = [roi_form.get_planes_from_string(ptv[0]) for ptv in ptv_coordinates_strings]
        tv_coordinates = roi_form.get_roi_coordinates_from_planes(roi_geom.union(ptvs))

        try:
            data = roi_geom.min_distances_to_target(oar_coordinates, tv_coordinates)
            dth = roi_geom.dth(data)
            dth_string = ','.join(['%.3f' % num for num in dth])

            data_map = {'dist_to_ptv_min': round(float(np.min(data)), 2),
                        'dist_to_ptv_mean': round(float(np.mean(data)), 2),
                        'dist_to_ptv_median': round(float(np.median(data)), 2),
                        'dist_to_ptv_max': round(float(np.max(data)), 2),
                        'dth_string': dth_string}

            for key, value in listitems(data_map):
                update_dvhs_table(study_instance_uid, roi_name, key, value)

        except:
            print('dist_to_ptv calculation failure, skipping')


def treatment_volume_overlap(study_instance_uid, roi_name):
    """
    This function will recalculate the PTV overlap of an roi based on data in the SQL DB.
    :param study_instance_uid: uid as specified in SQL DB
    :param roi_name: roi_name as specified in SQL DB
    """

    oar_coordinates_string = DVH_SQL().query('dvhs',
                                             'roi_coord_string',
                                             "study_instance_uid = '%s' and roi_name = '%s'"
                                             % (study_instance_uid, roi_name))

    ptv_coordinates_strings = DVH_SQL().query('dvhs',
                                              'roi_coord_string',
                                              "study_instance_uid = '%s' and roi_type like 'PTV%%'"
                                              % study_instance_uid)

    if ptv_coordinates_strings:
        oar = roi_form.get_planes_from_string(oar_coordinates_string[0][0])

        ptvs = [roi_form.get_planes_from_string(ptv[0]) for ptv in ptv_coordinates_strings]

        tv = roi_geom.union(ptvs)
        overlap = roi_geom.overlap_volume(oar, tv)

        update_dvhs_table(study_instance_uid, roi_name, 'ptv_overlap', round(float(overlap), 2))


def dist_to_ptv_centroids(study_instance_uid, roi_name):
    """
    This function will recalculate the OARtoPTV centroid distance based on data in the SQL DB.
    :param study_instance_uid: uid as specified in SQL DB
    :param roi_name: roi_name as specified in SQL DB
    """

    oar_centroid_string = DVH_SQL().query('dvhs',
                                          'centroid',
                                          "study_instance_uid = '%s' and roi_name = '%s'"
                                          % (study_instance_uid, roi_name))
    oar_centroid = np.array([float(i) for i in oar_centroid_string[0][0].split(',')])

    ptv_coordinates_strings = DVH_SQL().query('dvhs',
                                              'roi_coord_string',
                                              "study_instance_uid = '%s' and roi_type like 'PTV%%'"
                                              % study_instance_uid)

    if ptv_coordinates_strings:

        ptvs = [roi_form.get_planes_from_string(ptv[0]) for ptv in ptv_coordinates_strings]
        tv = roi_geom.union(ptvs)
        ptv_centroid = np.array(roi_geom.centroid(tv))

        data = float(np.linalg.norm(ptv_centroid - oar_centroid)) / 10.

        update_dvhs_table(study_instance_uid, roi_name, 'dist_to_ptv_centroids', round(float(data), 3))


def volumes(study_instance_uid, roi_name):
    """
    This function will recalculate the volume of an roi based on data in the SQL DB.
    :param study_instance_uid: uid as specified in SQL DB
    :param roi_name: roi_name as specified in SQL DB
    """

    coordinates_string = DVH_SQL().query('dvhs',
                                         'roi_coord_string',
                                         "study_instance_uid = '%s' and roi_name = '%s'"
                                         % (study_instance_uid, roi_name))

    roi = roi_form.get_planes_from_string(coordinates_string[0][0])

    data = roi_geom.volume(roi)

    update_dvhs_table(study_instance_uid, roi_name, 'volume', round(float(data), 2))


def surface_area(study_instance_uid, roi_name):
    """
    This function will recalculate the surface area of an roi based on data in the SQL DB.
    :param study_instance_uid: uid as specified in SQL DB
    :param roi_name: roi_name as specified in SQL DB
    """

    coordinates_string = DVH_SQL().query('dvhs',
                                         'roi_coord_string',
                                         "study_instance_uid = '%s' and roi_name = '%s'"
                                         % (study_instance_uid, roi_name))

    roi = roi_form.get_planes_from_string(coordinates_string[0][0])

    data = roi_geom.surface_area(roi, coord_type="sets_of_points")

    update_dvhs_table(study_instance_uid, roi_name, 'surface_area', round(float(data), 2))


def update_dvhs_table(study_instance_uid, roi_name, column, value):
    DVH_SQL().update('dvhs', column, value,
                     "study_instance_uid = '%s' and roi_name = '%s'" % (study_instance_uid, roi_name))


def update_plan_toxicity_grades(cnx, study_instance_uid):
    toxicities = cnx.get_unique_values('DVHs', 'toxicity_grade', "study_instance_uid = '%s'" % study_instance_uid)
    toxicities_str = ','.join(toxicities)
    cnx.update('Plans', 'toxicity_grades', toxicities_str, "study_instance_uid = '%s'" % study_instance_uid)


def update_all_plan_toxicity_grades(*condition):
    if condition:
        condition = condition[0]
    cnx = DVH_SQL()
    uids = cnx.get_unique_values('Plans', 'study_instance_uid', condition, return_empty=True)
    for uid in uids:
        update_plan_toxicity_grades(uid)
    cnx.close()


def plan_complexity(cnx, study_instance_uid):
    beam_complexities = cnx.query('Beams', 'complexity_mean, beam_mu', "study_instance_uid = '%s'" % study_instance_uid)
    plan_mu = float(np.sum([row[1] for row in beam_complexities]))
    mean_complexity = float(np.sum([row[0] * row[1] for row in beam_complexities])) / plan_mu
    cnx.update('Plans', 'complexity', mean_complexity, "study_instance_uid = '%s'" % study_instance_uid)


def plan_complexities(*condition):
    if condition:
        condition = condition[0]
    cnx = DVH_SQL()
    uids = cnx.get_unique_values('Plans', 'study_instance_uid', condition, return_empty=True)
    for uid in uids:
        plan_complexity(cnx, uid)
    cnx.close()
