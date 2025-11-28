# Portfolio Hybrid (Astro + MkDocs)

## Структура

- `/` — Astro landing (apps/landing/)
- `/docs/` — MkDocs documentation (docs/)

## Локальный запуск

### MkDocs (документация)
```bash
pip install -r requirements.txt
mkdocs serve
# http://localhost:8000
```

### Astro (лендинг)
```bash
cd apps/landing
npm install
npm run dev
# http://localhost:4321
```

## Деплой (GitLab Pages)

Push в `main` → автоматическая сборка обоих компонентов → деплой на Pages.

## Кастомизация

1. Замените `yourusername` на реальные ссылки
2. Обновите контент в `docs/`
3. Измените палитру в `tailwind.config.mjs`
