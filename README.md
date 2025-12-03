🐾 Animal Blog API - Документация
📖 О проекте
Animal Blog API — это полноценное RESTful API для блога о животных, построенное на Django и Django REST Framework. API предоставляет полный набор эндпоинтов для управления постами о животных, категориями, тегами и пользователями.

🚀 Основные возможности:
📝 CRUD операции для постов, категорий и тегов

🔍 Поиск и фильтрация по различным параметрам

🔐 Аутентификация и авторизация

📊 Пагинация и сортировка

📈 Статистика и аналитика

🏷️ Тегирование и категоризация

👁️ Система просмотров

🖼️ Работа с изображениями

🛠 Технологический стек
Компонент	Технология
Бэкенд	Django 5.2 + Django REST Framework
База данных	SQLite (разработка) / PostgreSQL (продакшен)
Аутентификация	DRF Token, JWT (опционально)
Документация	Django REST Framework Browsable API
Разработка	Poetry, Django Extensions

📡 API Endpoints

🔹 Посты (Posts)
Метод	Endpoint	Описание
GET	/api/v1/posts/	Список всех постов
GET	/api/v1/posts/{slug}/	Детали поста
POST	/api/v1/posts/create/	Создание поста
GET	/api/v1/recent/	Последние посты
GET	/api/v1/popular/	Популярные посты

🔹 Категории (Categories)
Метод	Endpoint	Описание
GET	/api/v1/categories/	Все категории
GET	/api/v1/categories/{slug}/	Категория детально

🔹 Теги (Tags)
Метод	Endpoint	Описание
GET	/api/v1/tags/	Все теги
GET	/api/v1/tags/{slug}/	Посты по тегу

🔹 Системные
Метод	Endpoint	Описание
GET	/api/v1/statistics/	Статистика сайта
GET	/api-auth/login/	Логин (Browsable API)

🤝 Вклад в проект
Форкните репозиторий
Создайте ветку для фичи (git checkout -b feature/amazing-feature)
Закоммитьте изменения (git commit -m 'Add amazing feature')
Запушьте ветку (git push origin feature/amazing-feature)
Откройте Pull Request
