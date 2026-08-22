# Аналіз даних і математичне моделювання — матеріали курсу

Сайт з лекціями та практичними заняттями, зібраний [MkDocs](https://www.mkdocs.org/) +
[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/).

## Локальний перегляд

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
mkdocs serve
```

Сайт буде доступний на http://127.0.0.1:8000.

## Структура

```
docs/
├── index.md              # головна сторінка курсу
├── lectures/              # конспекти лекцій
└── practice/              # завдання практичних занять
```

Нові заняття додаються так само, як уже наявні: створити `docs/lectures/0N-slug.md`
або `docs/practice/0N-slug.md` і додати рядок у розділ `nav:` файлу `mkdocs.yml`.
