"""
Общие геометрические утилиты
"""
import numpy as np
import math

class GeometryUtils:
    @staticmethod
    def get_line_intersection(p1, p2, p3, p4):
        """Находит точку пересечения двух отрезков"""
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = p3
        x4, y4 = p4
        
        denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if denominator == 0:
            return None
            
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denominator
        
        if 0 <= t <= 1:
            x = x1 + t * (x2 - x1)
            y = y1 + t * (y2 - y1)
            return (x, y)
        return None

    @staticmethod
    def dot_product(v1, v2):
        """Скалярное произведение векторов"""
        return v1[0]*v2[0] + v1[1]*v2[1]

    @staticmethod
    def normalize_vector(v):
        """Нормализация вектора"""
        length = math.sqrt(v[0]**2 + v[1]**2)
        return (v[0]/length, v[1]/length) if length > 0 else (0, 0) 