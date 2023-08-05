#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Université de Lorraine - LORIA
# Fichier d'init du module Pose Transform :
#  -> matrices de transformations entre repères à partir d'une pose 3D
# utilisant le module numpy
#
################################################################################

################################################################################
# Chargement des modules standards
################################################################################
import numpy as np
import quaternion
import math
################################################################################

################################################################################
# DÉCLARATION DES TYPES DE DONNÉES
#
################################################################################
# Description d'une transformation
################################################################################
class Transformation:
    matrice = None  # Matrice de transfo

    # Constructeur
    def __init__(self, mat=None, quat=None, pos=None):
        assert(not(mat is not None and (quat is not None or pos is not None))), ''
        "Spécification exclusive matrice OU (quaternion + position) !"
        if mat is None:
            self.matrice = np.identity(4)
            if quat is not None and pos is not None:
                self.matrice[:3, :3] = quaternion.as_rotation_matrix(quat)
                self.matrice[:3, 3] = pos
        else:
            self.matrice = np.copy(mat)

    # Affichage de la transformation
    def __str__(self):
        q = self.quaternion()
        angle = 2*math.acos(q.w)
        d = np.linalg.norm([q.x, q.y, q.z])
        if (abs(d) < 1e-10):
            d = 1
        p = self.position()
        res = "|"
        res += str(p) + " "
        res += "(" + str(angle) + ", "
        res += "[" + str(q.x/d) + ", " + str(q.y/d) + ", " + str(q.z/d) + "]"
        res += ")"
        res += "|"
        return res

    # Conversion quaternion vers matrice
    def quat_2_mat(self, quat, pos):
        self.matrice[:3, :3] = quaternion.as_rotation_matrix(quat)
        self.matrice[:3, 3] = position

    # Inverse de la transformation
    def inverse(self):
        return Transformation(np.linalg.inv(self.matrice))

    # Extraction du quaternion de la matrice
    def quaternion(self):
        return quaternion.from_rotation_matrix(self.matrice)

    # Extraction de la position de la matrice
    def position(self):
        return self.matrice[:3, 3]

    # Composition de transformations
    def composition(self, tr):
        return Transformation(mat=self.matrice.dot(tr.matrice))

    # Transformation d'un point
    def projection(self, pt):
        if (len(pt) == 3):
            return self.matrice.dot(pt+[1])
        else:
            return self.matrice.dot(pt)
################################################################################
