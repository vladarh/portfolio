# Миграция Helm-чартов

## Задача

Автоматизировать перенос 30+ Helm чартов между репозиториями с подписью артефактов.

## Реализация

Python скрипт + GitLab CI:

```python
# Пример структуры
helm pull chart --version X
helm push chart target-registry
cosign sign registry/chart:tag
```

## Итог

- 100% чартов мигрировано за 2 дня
- Все артефакты подписаны cosign
- Валидация в CI/CD
