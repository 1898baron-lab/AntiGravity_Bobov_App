# Code review suggestions

### USER
import React, { useState } from 'react';
import { Download, Check, AlertCircle, FileText } from 'lucide-react';

const DocumentsTracker = () => {
  const [documents, setDocuments] = useState([
    // ПРИОРИТЕТ 1 - Базовые требования для работы на УЭХК
    { id: 1, num: '1', code: 'СТО 26.197-2021', name: 'Правила внутреннего трудового распорядка', purpose: 'График работы, режим, пропуска на УЭХК, дисциплина', priority: 1, category: 'Базовые требования УЭХК', date: '02.12.25', studied: false },
    { id: 2, num: '6', code: 'СТО 35.012-2025', name: 'Положение о защите информации, составляющей коммерческую тайну', purpose: 'КРИТИЧНО: работа с данными УЭХК, что нельзя выносить', priority: 1, category: 'Базовые требования УЭХК', date: '08.02.25', studied: false },
    { id: 3, num: '7', code: 'СТО 35.008-2025', name: 'Инструкция о порядке учёта, хранения и обращения с носителями КТ', purpose: 'Как маркировать модели/чертежи, где хранить, как передавать', priority: 1, category: 'Базовые требования УЭХК', date: '08.12.25', studied: false },
    { id: 4, num: '8', code: 'СТО 85.123-2025', name: 'Инструкция о порядке обращения со служебной информацией ОРД', purpose: 'Что такое ДСП, как работать с "Для служебного пользования"', priority: 1, category: 'Базовые требования УЭХК', date: '08.12.25', studied: false },
    { id: 5, num: '4', code: 'СТО 26.242-2021', name: 'Положение об обработке и защите персональных данных', purpose: 'Если в модели будут данные о персонале УЭХК', priority: 1, category: 'Базовые требования УЭХК', date: '08.12.25', studied: false },
    
    // ПРИОРИТЕТ 1 - Управление документацией
    { id: 6, num: '31', code: 'СТО 00.003-2021', name: 'ИСМ. Управление документацией', purpose: 'КРИТИЧНО: как оформлять модели, версии, согласования, архив', priority: 1, category: 'Управление документацией', date: '08.12.25', studied: false },
    { id: 7, num: '32', code: 'СТО 00.004-2021', name: 'ИСМ. Управление записями', purpose: 'Как хранить версии моделей, логировать изменения, сроки', priority: 1, category: 'Управление документацией', date: '08.12.25', studied: false },
    
    // ПРИОРИТЕТ 1 - Безопасность
    { id: 8, num: '46', code: 'СТО 10.085-2025', name: 'Пожарная безопасность. Инструкция о мерах ПБ', purpose: 'Огнетушители, эвакуация на УЭХК, действия при пожаре', priority: 1, category: 'Безопасность', date: '08.12.25', studied: false },
    { id: 9, num: '19', code: 'Приказ №311/392-П', name: 'Кодекс этики и корпоративного поведения', purpose: 'Правила на объекте, конфликт интересов, антикоррупция', priority: 1, category: 'Безопасность', date: '09.12.25', studied: false },

    // ПРИОРИТЕТ 2 - Контекст и процессы
    { id: 10, num: '18', code: 'Приказ №311/55-П', name: 'Политика в области качества, экологии, ОТ, устойчивого развития', purpose: 'Контекст ИСМ, стратегия цифровизации (цифровые двойники)', priority: 2, category: 'Контекст и процессы', date: '08.12.25', studied: false },
    { id: 11, num: '36', code: 'СТО 00.062-2024', name: 'Руководство по интегрированной системе менеджмента', purpose: 'Процессная модель, твоё место (процесс 22 - ИМ и цифровизация)', priority: 2, category: 'Контекст и процессы', date: '08.12.25', studied: false },
    { id: 12, num: '26', code: 'СТО 26.104-2021', name: 'Порядок организации контроля исполнения поручений', purpose: 'Как работать с задачами от ГИПа/руководства, сроки, отчёты', priority: 2, category: 'Контекст и процессы', date: '08.12.25', studied: false },
    { id: 13, num: '2', code: 'СТО 26.110-2022', name: 'Положение по оплате труда работников', purpose: 'Зарплата, премии, KPI за выполнение проекта', priority: 2, category: 'Контекст и процессы', date: '02.12.25', studied: false },

    // ПРИОРИТЕТ 2 - Рабочие процессы
    { id: 14, num: '10', code: 'СТО 26.110-2021', name: 'Положение о порядке направления работников в командировки', purpose: 'Если будут выезды на УЭХК или в Москву', priority: 2, category: 'Рабочие процессы', date: '08.02.25', studied: false },
    { id: 15, num: '17', code: 'СТО 26.238-2021', name: 'Положение об электронном взаимодействии через ЛК работника', purpose: 'Кадровая система, заявки на пропуска/отпуск', priority: 2, category: 'Рабочие процессы', date: '08.12.25', studied: false },
    { id: 16, num: '14', code: 'СТО 26.037-2022', name: 'Положение о подарках, приглашениях и делового гостеприимства', purpose: 'Что можно принимать от заказчика (УЭХК) - антикоррупция', priority: 2, category: 'Рабочие процессы', date: '08.12.25', studied: false },

    // ПРИОРИТЕТ 3 - Специальные BIM-документы (запросить)
    { id: 17, num: '-', code: 'Запросить', name: 'СТО по информационному моделированию (BIM/ТИМ)', purpose: 'Требования к LOD, форматы (IFC/RVT), структура именования', priority: 3, category: 'Специальные BIM-документы', date: '-', studied: false },
    { id: 18, num: '-', code: 'Запросить', name: 'СТО по цифровым двойникам', purpose: 'Состав ЦД, требования к точности, интеграция с КИРО', priority: 3, category: 'Специальные BIM-документы', date: '-', studied: false },
    { id: 19, num: '-', code: 'Запросить', name: 'Регламент работы с данными УЭХК', purpose: 'Какие данные выносить, как маркировать модели, где хранить', priority: 3, category: 'Специальные BIM-документы', date: '-', studied: false },
    { id: 20, num: '-', code: 'Запросить', name: 'Шаблон проекта Revit ЦПТИ (RTE)', purpose: 'Настроенный шаблон с семействами, стандартами оформления', priority: 3, category: 'Специальные BIM-документы', date: '-', studied: false },
    { id: 21, num: '-', code: 'Запросить', name: 'Библиотека семейств ЦПТИ (RFA)', purpose: 'Типовые элементы оборудования, конструкций для УЭХК', priority: 3, category: 'Специальные BIM-документы', date: '-', studied: false },
    { id: 22, num: '-', code: 'Запросить', name: 'Стандарты именования файлов/папок', purpose: 'Структура каталогов, версионность, синхронизация', priority: 3, category: 'Специальные BIM-документы', date: '-', studied: false },

    // ПРИОРИТЕТ 3 - Справочно
    { id: 23, num: '3', code: 'СТО 26.308-2024', name: 'Программа помощи в улучшении жилищных условий', purpose: 'Если планируешь брать ипотеку', priority: 3, category: 'Справочно', date: '08.12.25', studied: false },
    { id: 24, num: '5', code: 'СТО 26.367-2025', name: 'Корпоративная социальная программа АО «ЦПТИ»', purpose: 'Соцпакет, ДМС, льготы', priority: 3, category: 'Справочно', date: '08.12.25', studied: false },
    { id: 25, num: '15', code: 'СТО 26.078-2022', name: 'Положение по применению инструментов мотивации', purpose: 'Рационализаторские предложения по улучшению BIM-процессов', priority: 3, category: 'Справочно', date: '08.02.25', studied: false },
  ]);

  const toggleStudied = (id) => {
    setDocuments(docs => docs.map(doc => 
      doc.id === id ? { ...doc, studied: !doc.studied } : doc
    ));
  };

  const downloadCSV = () => {
    const headers = ['№', 'Обозначение', 'Название документа', 'Назначение', 'Приоритет', 'Категория', 'Дата ознакомления', 'Изучено'];
    const rows = documents.map(doc => [
      doc.num,
      doc.code,
      doc.name,
      doc.purpose,
      doc.priority === 3 && doc.code === 'Запросить' ? 'Запросить у руководителя' : Приоритет ${doc.priority},
      doc.category,
      doc.date,
      doc.studied ? 'Да' : 'Нет'
    ]);

    const csvContent = [
      headers.join(';'),
      ...rows.map(row => row.map(cell => "${cell}").join(';'))
    ].join('\n');

    const BOM = '\uFEFF';
    const blob = new Blob([BOM + csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'ЦПТИ_Документы_BIM-моделлер_Бобов_КО.csv';
    link.click();
  };

  const priorityColors = {
    1: 'bg-red-50 border-red-200',
    2: 'bg-yellow-50 border-yellow-200',
    3: 'bg-blue-50 border-blue-200'
  };

  const priorityLabels = {
    1: 'Обязательно (неделя 1)',
    2: 'Желательно (месяц 1)',
    3: 'Запросить у руководителя'
  };

  const groupedDocs = documents.reduce((acc, doc) => {
    if (!acc[doc.priority]) acc[doc.priority] = {};
    if (!acc[doc.priority][doc.category]) acc[doc.priority][doc.category] = [];
    acc[doc.priority][doc.category].push(doc);
    return acc;
  }, {});

  const stats = {
    total: documents.length,
    studied: documents.filter(d => d.studied).length,
    priority1: documents.filter(d => d.priority === 1).length,
    priority2: documents.filter(d => d.priority === 2).length,
    priority3: documents.filter(d => d.priority === 3).length,
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <div className="flex justify-between items-start mb-4">
            <div>
              <h1 className="text-2xl font-bold text-gray-900 mb-2">
                Перечень документов для изучения
              </h1>
              <p className="text-gray-600 mb-1">
                <strong>Должность:</strong> Инженер-конструктор 2 категории (BIM-моделлер)
              </p>
              <p className="text-gray-600 mb-1">
                <strong>ФИО:</strong> Бобов Кирилл Олегович
              </p>
              <p className="text-gray-600 mb-1">
                <strong>Филиал:</strong> Уральский филиал, г. Новоуральск
              </p>
              <p className="text-gray-600">
                <strong>Проект:</strong> Цифровой двойник КИУ, здание 203 УЭХК
              </p>
            </div>
            <button
              onClick={downloadCSV}
              className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
            >
              <Download size={20} />
              Скачать CSV
            </button>
          </div>

          <div className="grid grid-cols-5 gap-4">
            <div className="bg-gray-100 p-4 rounded-lg">
              <div className="text-2xl font-bold text-gray-900">{stats.total}</div>
              <div className="text-sm text-gray-600">Всего документов</div>
            </div>
            <div className="bg-green-100 p-4 rounded-lg">
              <div className="text-2xl font-bold text-green-700">{stats.studied}</div>
              <div className="text-sm text-gray-600">Изучено</div>
            </div>
            <div className="bg-red-100 p-4 rounded-lg">
              <div className="text-2xl font-bold text-red-700">{stats.priority1}</div>
              <div className="text-sm text-gray-600">Неделя 1</div>
            </div>
            <div className="bg-yellow-100 p-4 rounded-lg">
              <div className="text-2xl font-bold text-yellow-700">{stats.priority2}</div>
              <div className="text-sm text-gray-600">Месяц 1</div>
            </div>
            <div className="bg-blue-100 p-4 rounded-lg">
              <div className="text-2xl font-bold text-blue-700">{stats.priority3}</div>
              <div className="text-sm text-gray-600">Запросить</div>
            </div>
          </div>
        </div>

        {[1, 2, 3].map(priority => (
          <div key={priority} className="mb-6">
            <div className="flex items-center gap-2 mb-4">
              <h2 className="text-xl font-bold text-gray-900">
                {priorityLabels[priority]}
              </h2>
              {priority === 3 && (
                <AlertCircle size={20} className="text-blue-600" />
              )}
            </div>
            
            {Object.entries(groupedDocs[priority] || {}).map(([category, docs]) => (
              <div key={category} className="mb-4">
                <h3 className="text-md font-semibold text-gray-700 mb-3 flex items-center gap-2">
                  <FileText size={16} />
                  {category}
                </h3>
                <div className="space-y-3">
                  {docs.map(doc => (
                    <div
                      key={doc.id}
                      className={border rounded-lg p-4 ${priorityColors[priority]} ${
                        doc.studied ? 'opacity-60' : ''
                      }}
                    >
                      <div className="flex items-start gap-4">
                        <button
                          onClick={() => toggleStudied(doc.id)}
                          className={flex-shrink-0 w-6 h-6 rounded border-2 flex items-center justify-center transition-colors ${
                            doc.studied
                              ? 'bg-green-600 border-green-600'
                              : 'bg-white border-gray-300 hover:border-green-600'
                          }}
                        >
                          {doc.studied && <Check size={16} className="text-white" />}
                        </button>
                        <div className="flex-1">
                          <div className="flex items-start justify-between mb-2">
                            <div>
                              {doc.num !== '-' && (
                                <span className="text-sm font-semibold text-gray-500">№{doc.num}</span>
                              )}
                              <span className={${doc.num !== '-' ? 'ml-3' : ''} text-sm font-mono ${
                                doc.code === 'Запросить' ? 'text-blue-700 font-bold' : 'text-gray-700'
                              }}>
                                {doc.code}
                              </span>
                            </div>
                            {doc.date !== '-' && (
                              <span className="text-xs text-gray-500">{doc.date}</span>
                            )}
                          </div>
                          <h3 className="font-semibold text-gray-900 mb-2">{doc.name}</h3>
                          <p className="text-sm text-gray-600">{doc.purpose}</p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        ))}

        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mt-6">
          <h3 className="font-semibold text-blue-900 mb-2">💡 План изучения для BIM-моделлера:</h3>
          <ul className="text-sm text-blue-800 space-y-1">
            <li>• <strong>День 1-3:</strong> Приоритет 1 "Базовые требования УЭХК" (№1, 6-8, 4, 46, 19) — КТ/ДСП/ПБ</li>
            <li>• <strong>День 4-5:</strong> Приоритет 1 "Управление документацией" (№31, 32) — версии моделей</li>
            <li>• <strong>Неделя 2:</strong> Приоритет 2 "Контекст и процессы" — понимание ИСМ и твоего места</li>
            <li>• <strong>Неделя 3-4:</strong> Приоритет 2 "Рабочие процессы" — командировки, ЛК, антикоррупция</li>
            <li>• <strong>Сразу:</strong> Запросить у руководителя все документы из Приоритета 3 (BIM-стандарты)</li>
          </ul>
        </div>

        <div className="bg-orange-50 border border-orange-200 rounded-lg p-4 mt-4">
          <h3 className="font-semibold text-orange-900 mb-2">⚠️ Контрольные вопросы к руководителю:</h3>
          <div className="text-sm text-orange-800 space-y-1">
            <p><strong>По проекту:</strong> Исходные данные здания 203? LOD? Состав модели? Цель ЦД?</p>
            <p><strong>По процессу:</strong> Заказчик? Команда? Форматы выдачи? BIM-стандарты?</p>
            <p><strong>По допуску:</strong> Выезд на УЭХК? Гриф секретности здания 203?</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DocumentsTracker;

### ASSISTANT


### USER
Запусти посмотрим

### ASSISTANT
Я сам код запустить не могу, но давай сделаем так, чтобы ты запустил и увидел ровно то же, что вижу я по логике. Ниже — минимально-корректный способ, без лишней болтовни.

Как быстро запустить локально (5 минут)
1. Создай проект
Bash
npm create vite@latest documents-tracker -- --template react
cd documents-tracker
npm install
2. Поставь зависимости
Bash
npm install lucide-react

Tailwind (обязательно, иначе UI «слепой»):

Bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

tailwind.config.js

JavaScript
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: { extend: {} },
  plugins: [],
}

src/index.css

CSS
@tailwind base;
@tailwind components;
@tailwind utilities;
3. Вставь компонент

src/DocumentsTracker.jsx
👉 вставляешь код ровно тот, что прислал

src/App.jsx

JavaScript
import DocumentsTracker from './DocumentsTracker';

function App() {
  return <DocumentsTracker />;
}

export default App;
4. Запуск
Bash
npm run dev

Открываешь:

http://localhost:5173
Что ты должен увидеть (чек-лист)

✅ Заголовок «Перечень документов для изучения»
✅ Карточки по приоритетам (красный / жёлтый / синий)
✅ Чекбоксы «Изучено»
✅ Кнопка «Скачать CSV» → файл корректно открывается в Excel
✅ Статистика сверху считается правильно
✅ «Запросить» подсвечено синим и с иконкой Alert

Если что-то из этого не так — это уже баг, и мы его точечно правим.

Важно

Если Tailwind не подключился, то:

логика будет работать,

но внешний вид будет «голым».

Это 90% всех «не работает» в таких случаях.

Запусти и скажи одно из трёх:

«Работает, всё как надо»

«Работает, но … (что не так визуально/логически)»

«Не стартует, вот ошибка» — просто скопируй ошибку

Дальше идём либо в доводку, либо в оформление как корпоративного инструмента.

