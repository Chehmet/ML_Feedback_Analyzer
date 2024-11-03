# ScoreWorker - Система анализа обратной связи сотрудников
# Команда - Girlies
**ScoreWorker** — это система анализа обратной связи сотрудников, предназначенная для оценки и генерации сводной информации о сотрудниках на основе отзывов коллег и руководителей. Система построена на базе Django для бэкенда, HTML/CSS/JavaScript для фронтенда, Python для обработки данных и Figma для разработки интерфейса.

## Описание проекта

Основная задача **ScoreWorker** — создание динамичной системы, которая позволяет:
- **Суммировать оценки сотрудников** на основе обратной связи.
- **Оценивать навыки по заданным критериям**.
- **Выделять технические навыки (hard skills)**, указанные в отзывах.
- **Определять общую оценку** сотрудника по шкале от 1 до 5 на основе всех отзывов.

Система использует графическое представление "колесо баланса" для визуализации оценки soft skills и применяет методы машинного обучения для анализа стиля самооценки сотрудника.

---

## Функциональные возможности

1. **Оценка компетенций**  
   Мы передали большой языковой модели все отзывы и выявили часто встречающиеся компетенции:   
   - Профессионализм
   - Инициативность
   - Решение конфликтов
   - Лидерство
   - Тайм-менеджмент
   - Адаптивность
   - Ответственность
   - Целеустремленность
   - Саморазвитие
   - Коммуникация

2. **Выделение hard skills**  
   На основе обработки естественного языка система извлекает технические навыки, упомянутые в отзывах, исключая soft skills, и возвращает только ключевые профессиональные компетенции.

3. **Анализ самооценки**  
   Система анализирует согласованность самооценки сотрудника с обратной связью от коллег, определяя склонность к чрезмерно положительной или отрицательной самооценке.

4. **Автоматическая генерация краткого резюме**  
   На основе методов обработки естественного языка (NLP) система генерирует краткое резюме производительности сотрудника.

---

## Стек технологий

- **Бэкенд**: Django
- **Фронтенд**: HTML, CSS, JavaScript
- **Продвинутые техники больших языковых моделей**: классификатор(facebook/bart-large-mnli), prompt-engineering, перефразирование и эмбеддинги
- **Обработка данных**: Python, API, NLP, transoformer(zero-shot, paraphrase-multilingual-MiniLM-L12-v2), кластеризация(KMeans), Torch
- **Дизайн**: Figma для прототипирования интерфейса

---

## Рабочий процесс

1. **Сбор данных**: Получение отзывов, удаление неинформативных, слишком позитивных или негативных, а так же устранение дополнительных и невидимых символов, чтобы оставить только полезные отзывы.
2. **Обработка данных**:
   - Генерация сводного резюме.
   - Выделение soft skills, их оценка, описание, а так же цитата напрямую из отзыва, чтобы увеличить уровень доверия к модели.
   - Выделение hard skills напрямую из отзыва где это возможно.
4. **Анализ**: Дополнительная информация, которую могут использоватьт HR компаний
   - Система оценивает самооценку сотрудника, сравнивая его отзывы с оценками коллег, и сообщает, нужна ли сотруднику психологическая или другая помощь, а так же курсы повышения квалификации.
   - Можно будет прочитать какой стиль написания фидбэка другим использует сотрудник и стоит ли учитывать его отзывы, если они слишком негативные или позитивные.
6. **Визуализация**: Представление оценок soft skills на круговой диаграмме для наглядного восприятия и подробное описание каждого критерия с ссылкой на отзыв, повлиявший на решение системы в большей степени.
7. **Вывод**: Генерация и сохранение детализированного отчета в формате JSON, который можно отобразить в HTML с использованием CSS.

---

## Визуализация

На нашем сервисе можно увидеть айди или имя сотрудника, его рейтинг, резюме производительности и дополнительную информацию, описанную выше.
Для наглядного представления оценок soft skills используется круговая диаграмма, отображающая значения следующих шагов:
1. Генерация оценок компетенций
2. Построение диаграммы
3. Отображение итогового рейтинга в виде средней оценки по всем компетенциям.
4. Описание компетенций и ссылка на отзыв с цитатой оттуда.
5. Топ отзывов, просортированных в порядке полезности.
---

## Интеграция с API

- **API URL**: Используется для NLP-задач и анализа текста.
- **Библиотека requests**: Применяется для выполнения API-запросов, генерации сводок, анализа отзывов и оценки компетенций.

---

## Варианты улучшений

- **Углубленный анализ настроения**: Добавление анализа настроения для более точной оценки самооценки.
- **Дополнительные визуализации**: Добавление временных линий для анализа динамики изменения оценок.
- **Автоматизация отчетности**: Автоматическое создание и отправка отчетов по расписанию.

---

## Установка и запуск

1. **Склонируйте репозиторий**:
   ```bash
   git clone https://github.com/Chehmet/InnoglobalHack.git
   ```
2. **Подключите API url:**
   
   Создайте файл `.env` в корне проекта и заполните поля ниже
   ```
   DATASET_DIR = ""
   API_URL = ""
   API_URL_BACKUP = ""
   ```
2. **Установите зависимости**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Запустите сервер Django**:
   ```bash
   python manage.py runserver
   ```
4. **Откройте панель управления**: Перейдите по адресу `http://localhost:8000`, чтобы получить доступ к интерфейсу.

---

## Примеры

- **Сгенерированное резюме**:
   ```json
   {
       "competencies": [{"competency": "Инициативность", "score": 5, "reason": "Отмечена способность брать на себя ответственность и решать задачи", "confirmation": "Не боишься брать на себя ответственность, устойчив к стрессу и терпелив."}],
       "hard skills": ["Программирование", "Аналитика"],
       "score": 4.6
   }
   ```

## Лицензия

Проект распространяется под лицензией MIT.

Для более подробной информации по настройке и дизайну системы, обращайтесь к исходному коду и не стесняйтесь писать разработчикам напрямую:
- **ML-инженеры** - [Чулпан](https://t.me/Chehmet), [Миляуша](https://t.me/mili_sham), [Назгуль](https://t.me/kokosinka123)
- **Backend developer** - [Галия](https://t.me/donna_Kupidona)
- **Frontend developer** - [Любовь](https://t.me/mangocandle)
