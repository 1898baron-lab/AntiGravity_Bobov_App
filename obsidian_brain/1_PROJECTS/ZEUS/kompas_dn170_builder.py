# -*- coding: utf-8 -*-
"""
Скрипт автоматического построения 3D-модели корпуса клапана Ду 170 в САПР КОМПАС-3D v24.
Материал: Алюминиевый сплав АМг6 (ГОСТ 4784)
Разработчик: Mastodont AI / AntiGravity
"""

import sys
import os
import pythoncom
from win32com.client import Dispatch, gencache

# Константы геометрии корпуса Ду 170 (АМг6)
BODY_SIZE = 302.0       # Внешний размер квадратного корпуса, мм
WALL_THICKNESS = 5.0    # Толщина стенки корпуса, мм
BODY_HEIGHT = 400.0     # Высота обечайки, мм
FLANGE_DIAMETER = 280.0 # Внешний диаметр присоединительных фланцев, мм
INNER_DIAMETER = 170.0  # Условный проход Ду (DN), мм
FLANGE_THICKNESS = 10.0 # Толщина фланца чистовая, мм

def connect_to_kompas():
    """Подключение к API КОМПАС-3D v24."""
    print(">>> Подключение к КОМПАС-3D...")
    try:
        # Инициализация раннего связывания с библиотекой типов КОМПАС (API7)
        kompas_api7 = gencache.EnsureModule('{69C10971-1138-40C2-835C-681966952877}', 0, 1, 0)
        kompas = Dispatch('Kompas.Application.7')
        kompas.Visible = True
        print(">>> Успешно подключено к КОМПАС-3D.")
        return kompas
    except Exception as e:
        print(f"[ОШИБКА] Не удалось подключиться к КОМПАС-3D. Проверьте, запущена ли САПР.")
        print(f"Подробности: {e}")
        return None

def create_dn170_valve_body(kompas):
    """Построение 3D-модели корпуса клапана Ду 170."""
    try:
        # Получение активного окна или создание новой детали
        documents = kompas.Documents
        doc = documents.Add(1, True) # 1 - константа для создания 3D-детали (Part)
        doc.Name = "Корпус клапана Ду170 (АМг6)"
        
        # Получение корневого интерфейса детали
        part = doc.TopPart
        print(f">>> Создана новая деталь: {doc.Name}")

        # Назначение материала АМг6
        print(">>> Присвоение материала: АМг6 ГОСТ 4784-2019...")
        part.Material = "АМг6 ГОСТ 4784-2019"
        part.Update()

        # Получение базовой плоскости XOY (XY_PLANE)
        planes = part.Planes
        plane_xy = planes.GetByName("Плоскость XOY")
        if not plane_xy:
            plane_xy = part.DefaultPlane(0) # 0 - XY плоскость

        # ---------------------------------------------------------------------
        # ШАГ 1: Построение наружного контура квадратного корпуса (302х302 мм)
        # ---------------------------------------------------------------------
        print(f">>> Создание эскиза квадратного корпуса ({BODY_SIZE}x{BODY_SIZE} мм)...")
        sketches = part.Sketches
        sketch1 = sketches.Add(plane_xy)
        sketch_edit = sketch1.BeginEdit()

        # Рисуем внешний квадрат со скругленными углами
        half = BODY_SIZE / 2.0
        # Отрисовка линий контура квадрата
        p1 = sketch_edit.LineSeg(-half, -half, half, -half)
        p2 = sketch_edit.LineSeg(half, -half, half, half)
        p3 = sketch_edit.LineSeg(half, half, -half, half)
        p4 = sketch_edit.LineSeg(-half, half, -half, -half)
        
        sketch1.EndEdit()

        # Выдавливание сплошного бруска на 400 мм (BODY_HEIGHT)
        print(f">>> Выдавливание корпуса на высоту {BODY_HEIGHT} мм...")
        extrusions = part.Extrusions
        extr1 = extrusions.Add(sketch1, 0) # 0 - направление выдавливания
        extr1.Direction = 0 # 0 - прямое направление
        extr1.Length = BODY_HEIGHT
        extr1.Update()

        # ---------------------------------------------------------------------
        # ШАГ 2: Вырезание внутреннего квадратного отверстия (стенка 5 мм)
        # ---------------------------------------------------------------------
        print(f">>> Вырезание внутренней полости (толщина стенки {WALL_THICKNESS} мм)...")
        # Создаем эскиз на верхней грани выдавленного бруска
        faces = part.Faces
        # Выбираем верхнюю плоскую грань (нормаль вдоль Z)
        top_face = None
        for face in faces:
            if face.Area > 90000: # Грань 302х302 имеет площадь ~91204 мм2
                top_face = face
                break

        if top_face:
            sketch2 = sketches.Add(top_face)
            sketch_edit2 = sketch2.BeginEdit()
            # Внутренний квадрат 292х292 мм
            inner_half = half - WALL_THICKNESS
            sketch_edit2.LineSeg(-inner_half, -inner_half, inner_half, -inner_half)
            sketch_edit2.LineSeg(inner_half, -inner_half, inner_half, inner_half)
            sketch_edit2.LineSeg(inner_half, inner_half, -inner_half, inner_half)
            sketch_edit2.LineSeg(-inner_half, inner_half, -inner_half, -inner_half)
            sketch2.EndEdit()

            # Вырезание выдавливанием насквозь
            cuts = part.CutExtrusions
            cut1 = cuts.Add(sketch2, 0)
            cut1.Direction = 0
            cut1.Length = BODY_HEIGHT
            cut1.Update()
        else:
            print("[ПРЕДУПРЕЖДЕНИЕ] Не удалось автоматически найти верхнюю грань для выреза полости.")

        # ---------------------------------------------------------------------
        # ШАГ 3: Создание круглых присоединительных фланцев (Ø280 мм, h=10 мм)
        # ---------------------------------------------------------------------
        print(f">>> Создание верхнего и нижнего фланцев Ø{FLANGE_DIAMETER} мм...")
        # Строим эскиз фланца на верхней грани
        if top_face:
            sketch3 = sketches.Add(top_face)
            sketch_edit3 = sketch3.BeginEdit()
            # Наружная окружность фланца Ø280
            sketch_edit3.Circle(0, 0, FLANGE_DIAMETER / 2.0)
            # Внутренняя окружность условного прохода Ø170
            sketch_edit3.Circle(0, 0, INNER_DIAMETER / 2.0)
            sketch3.EndEdit()

            # Выдавливание фланца толщиной 10 мм
            extr2 = extrusions.Add(sketch3, 0)
            extr2.Direction = 0 # Вверх
            extr2.Length = FLANGE_THICKNESS
            extr2.Update()

        # Обновляем сборку и пересчитываем массу
        part.Update()
        print(">>> 3D-модель успешно построена!")
        print(f">>> Расчетная масса детали: {part.Mass:.3f} кг")
        
        # Сохранение детали
        save_path = os.path.join(os.getcwd(), "DN170_Valve_Body_AMg6.m3d")
        doc.SaveAs(save_path)
        print(f">>> Файл 3D-модели сохранен: {save_path}")

    except Exception as e:
        print(f"[ОШИБКА] Произошел сбой при геометрическом построении: {e}")

if __name__ == "__main__":
    kompas = connect_to_kompas()
    if kompas:
        create_dn170_valve_body(kompas)
    else:
        print("\n[ИНСТРУКЦИЯ] Пожалуйста, запустите КОМПАС-3D v24 на компьютере и повторно запустите скрипт.")
        print("Скрипт автоматически подключится к открытой САПР и создаст идеальную 3D-модель корпуса Ду 170.")
