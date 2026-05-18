import pythoncom
from win32com.client import Dispatch, gencache

def connect_to_kompas():
    """Подключение к API КОМПАС-3D v24."""
    try:
        kompas_api7 = gencache.EnsureModule('{69C10971-1138-40C2-835C-681966952877}', 0, 1, 0)
        kompas_object = Dispatch('Kompas.Application.7')
        return kompas_object
    except Exception as e:
        print(f"Ошибка подключения к КОМПАСу: {e}")
        return None

def change_material_to_amg6(doc):
    """Смена материала на АМг6 в активном документе."""
    # Логика смены материала через API
    # АМг6 ГОСТ 4784-97
    print("Применение материала: АМг6...")
    # Здесь будет вызов API для редактирования свойств IPart
    pass

if __name__ == "__main__":
    kompas = connect_to_kompas()
    if kompas:
        active_doc = kompas.ActiveDocument
        if active_doc:
            print(f"Документ: {active_doc.Name}")
            change_material_to_amg6(active_doc)
        else:
            print("Нет активного документа в КОМПАСе.")
