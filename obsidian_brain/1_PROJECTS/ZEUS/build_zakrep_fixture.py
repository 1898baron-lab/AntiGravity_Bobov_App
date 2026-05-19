# -*- coding: utf-8 -*-
"""
Скрипт автоматического построения 3D-модели станины сборочно-сварочного стапеля «ЗАКРЕП v1.0» в САПР КОМПАС-3D v24.
Материал станины: Сталь 3сп (ГОСТ 380-2005)
Профиль: Труба квадратная 80х80х5 (ГОСТ 8639-82)
Разработчик: Mastodont AI / AntiGravity
"""

import sys
import os
import pythoncom
from win32com.client import Dispatch, gencache

# Габаритные размеры станины стапеля
FRAME_X = 1300.0        # Длина по оси X, мм
FRAME_Y = 900.0         # Ширина по оси Y, мм
PROFILE_SIZE = 80.0     # Сторона квадратной трубы, мм
PROFILE_WALL = 5.0      # Толщина стенки трубы, мм

def connect_to_kompas():
    """Подключение к API КОМПАС-3D v24."""
    print(">>> Подключение к КОМПАС-3D...")
    try:
        # Инициализация раннего связывания с КОМПАС (API7)
        kompas_api7 = gencache.EnsureModule('{69C10971-1138-40C2-835C-681966952877}', 0, 1, 0)
        kompas = Dispatch('Kompas.Application.7')
        kompas.Visible = True
        print(">>> Успешно подключено к КОМПАС-3D.")
        return kompas
    except Exception as e:
        print(f"[ОШИБКА] Не удалось подключиться к КОМПАС-3D. Запустите САПР на компьютере.")
        print(f"Подробности: {e}")
        return None

def build_zakrep_frame(kompas):
    """Построение 3D-модели станины стапеля «ЗАКРЕП v1.0»."""
    try:
        # Создаем новый 3D-документ (деталь)
        documents = kompas.Documents
        doc = documents.Add(1, True) # 1 - константа для 3D-детали (Part)
        doc.Name = "Станина стапеля ЗАКРЕП v1.0"
        
        part = doc.TopPart
        print(f">>> Создана новая деталь для стапеля: {doc.Name}")

        # Назначение материала
        print(">>> Назначение материала: Сталь 3сп ГОСТ 380-2005...")
        part.Material = "Сталь 3сп ГОСТ 380-2005"
        part.Update()

        # Получаем базовую плоскость XOY
        planes = part.Planes
        plane_xy = planes.GetByName("Плоскость XOY")
        if not plane_xy:
            plane_xy = part.DefaultPlane(0)

        # ---------------------------------------------------------------------
        # ШАГ 1: Построение наружного контура рамы (1300 х 900 мм) из труб 80х80
        # Для простоты моделируем раму выдавливанием эскиза коробчатого сечения.
        # ---------------------------------------------------------------------
        print(f">>> Создание эскиза рамы {FRAME_X}x{FRAME_Y} мм...")
        sketches = part.Sketches
        sketch1 = sketches.Add(plane_xy)
        sketch_edit = sketch1.BeginEdit()

        # Внешний габарит плиты стапеля
        half_x = FRAME_X / 2.0
        half_y = FRAME_Y / 2.0
        
        sketch_edit.LineSeg(-half_x, -half_y, half_x, -half_y)
        sketch_edit.LineSeg(half_x, -half_y, half_x, half_y)
        sketch_edit.LineSeg(half_x, half_y, -half_x, half_y)
        sketch_edit.LineSeg(-half_x, half_y, -half_x, -half_y)

        # Внутреннее окно рамы (вычитаем ширину профильной трубы 80 мм с каждой стороны)
        inner_half_x = half_x - PROFILE_SIZE
        inner_half_y = half_y - PROFILE_SIZE
        
        sketch_edit.LineSeg(-inner_half_x, -inner_half_y, inner_half_x, -inner_half_y)
        sketch_edit.LineSeg(inner_half_x, -inner_half_y, inner_half_x, inner_half_y)
        sketch_edit.LineSeg(inner_half_x, inner_half_y, -inner_half_x, inner_half_y)
        sketch_edit.LineSeg(-inner_half_x, inner_half_y, -inner_half_x, -inner_half_y)
        
        sketch1.EndEdit()

        # Выдавливание внешнего каркаса станины на высоту профиля (80 мм)
        print(f">>> Выдавливание внешнего силового каркаса на {PROFILE_SIZE} мм...")
        extrusions = part.Extrusions
        extr1 = extrusions.Add(sketch1, 0)
        extr1.Direction = 0
        extr1.Length = PROFILE_SIZE
        extr1.Update()

        # ---------------------------------------------------------------------
        # ШАГ 2: Вырезание внутренних полостей труб для имитации толщины стенки 5 мм
        # В реальной САПР это делается профилями металлоконструкций, здесь — 3D вырезом
        # ---------------------------------------------------------------------
        print(">>> Моделирование полых профилей (толщина стенки 5 мм)...")
        # Выбираем верхнюю плоскость для построения внутренних контуров труб
        faces = part.Faces
        top_face = None
        for face in faces:
            if face.Area > 200000: # Площадь поверхности рамки ~352000 мм2
                top_face = face
                break

        if top_face:
            sketch2 = sketches.Add(top_face)
            sketch_edit2 = sketch2.BeginEdit()
            
            # Контуры выреза для каждой из четырех сторон рамы
            # Верхний и нижний профили
            sketch_edit2.LineSeg(-half_x + PROFILE_WALL, -half_y + PROFILE_WALL, half_x - PROFILE_WALL, -half_y + PROFILE_WALL)
            sketch_edit2.LineSeg(half_x - PROFILE_WALL, -half_y + PROFILE_WALL, half_x - PROFILE_WALL, -inner_half_y - PROFILE_WALL)
            sketch_edit2.LineSeg(half_x - PROFILE_WALL, -inner_half_y - PROFILE_WALL, -half_x + PROFILE_WALL, -inner_half_y - PROFILE_WALL)
            sketch_edit2.LineSeg(-half_x + PROFILE_WALL, -inner_half_y - PROFILE_WALL, -half_x + PROFILE_WALL, -half_y + PROFILE_WALL)

            sketch_edit2.LineSeg(-half_x + PROFILE_WALL, inner_half_y + PROFILE_WALL, half_x - PROFILE_WALL, inner_half_y + PROFILE_WALL)
            sketch_edit2.LineSeg(half_x - PROFILE_WALL, inner_half_y + PROFILE_WALL, half_x - PROFILE_WALL, half_y - PROFILE_WALL)
            sketch_edit2.LineSeg(half_x - PROFILE_WALL, half_y - PROFILE_WALL, -half_x + PROFILE_WALL, half_y - PROFILE_WALL)
            sketch_edit2.LineSeg(-half_x + PROFILE_WALL, half_y - PROFILE_WALL, -half_x + PROFILE_WALL, inner_half_y + PROFILE_WALL)
            
            sketch2.EndEdit()

            # Вырезание внутренних полостей труб
            cuts = part.CutExtrusions
            cut1 = cuts.Add(sketch2, 0)
            cut1.Direction = 0
            cut1.Length = PROFILE_SIZE
            cut1.Update()

        # Обновляем деталь и рассчитываем массу
        part.Update()
        print(">>> 3D-модель станины стапеля «ЗАКРЕП v1.0» успешно построена!")
        print(f">>> Расчетная масса станины из стали: {part.Mass:.3f} кг")

        # Сохранение детали
        save_path = os.path.join(os.getcwd(), "ZAKREP_Frame_Base.m3d")
        doc.SaveAs(save_path)
        print(f">>> Файл сохранен: {save_path}")

    except Exception as e:
        print(f"[ОШИБКА] Не удалось построить геометрию станины: {e}")

if __name__ == "__main__":
    kompas = connect_to_kompas()
    if kompas:
        build_zakrep_frame(kompas)
    else:
        print("\n[ИНСТРУКЦИЯ] Пожалуйста, запустите КОМПАС-3D v24 на компьютере и повторно запустите скрипт.")
        print("Скрипт автоматически построит прочную сварную станину стапеля из квадратного профиля.")
