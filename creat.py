#!/usr/bin/env python3
"""
Portfolio Hybrid Setup Script
Creates Astro landing + MkDocs documentation structure
"""

import os
from pathlib import Path

def create_file(path: str, content: str):
    """Create file with content, making parent dirs if needed"""
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding='utf-8')
    print(f"✓ Created: {path}")

def main():
    base = Path.cwd()
    print(f"Creating portfolio structure in: {base}\n")

    # Root files
    create_file("mkdocs.yml", """site_name: Владислав Рубцов — Портфолио
site_url: https://example.com
site_description: DevSecOps/DevOps инженер и full-stack разработчик
repo_url: https://gitlab.com/yourusername/portfolio
repo_name: GitLab

theme:
  name: material
  language: ru
  palette:
    - scheme: default
      primary: blue
      accent: purple
      toggle:
        icon: material/brightness-7
        name: Тёмная тема
    - scheme: slate
      primary: blue
      accent: purple
      toggle:
        icon: material/brightness-4
        name: Светлая тема
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.top
    - search.suggest
    - content.code.copy

plugins:
  - search:
      lang: ru
  - minify:
      minify_html: true

markdown_extensions:
  - admonition
  - pymdownx.highlight
  - pymdownx.superfences
  - pymdownx.tabbed
  - toc:
      permalink: true

nav:
  - Главная: index.md
  - Кейсы:
      - cases/compliance-automation.md
      - cases/helm-migration.md
  - Чертежи:
      - blueprints/gitlab-ci-templates.md
  - Контакты: contacts.md
""")

    create_file("requirements.txt", """mkdocs>=1.5.3
mkdocs-material>=9.5.0
mkdocs-minify-plugin>=0.7.2
pymdown-extensions>=10.7
""")

    create_file(".gitlab-ci.yml", """stages: [build, deploy]

variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"
  NODE_ENV: "production"

cache:
  paths:
    - .cache/pip
    - apps/landing/node_modules/

build:docs:
  stage: build
  image: python:3.11
  script:
    - pip install -r requirements.txt
    - mkdocs build --strict
  artifacts:
    paths:
      - site/
    expire_in: 1 week

build:landing:
  stage: build
  image: node:20-alpine
  before_script:
    - cd apps/landing
  script:
    - npm ci
    - npm run build
  artifacts:
    paths:
      - apps/landing/dist/
    expire_in: 1 week

pages:
  stage: deploy
  image: alpine:3.19
  needs: ["build:docs", "build:landing"]
  script:
    - mkdir -p public
    - cp -r apps/landing/dist/* public/
    - mkdir -p public/docs
    - cp -r site/* public/docs/
  artifacts:
    paths:
      - public
  only:
    - main
""")

    create_file(".gitignore", """# Python
__pycache__/
*.py[cod]
.venv/
venv/
site/
.cache/

# Node
node_modules/
dist/
.astro/

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
""")

    # MkDocs content
    create_file("docs/index.md", """# Владислав Рубцов

DevSecOps/DevOps инженер • Full-Stack разработчик

## О себе

Ускоряю выпуск продукта без компромиссов по безопасности. 3+ года коммерческого опыта, 6+ лет в ИБ.

## Компетенции

- **DevSecOps/DevOps**: Ansible, GitLab CI, CI/CD, Cosign, Helm, Kubernetes
- **Backend**: FastAPI, Django, PostgreSQL, Redis/Celery
- **Frontend**: Vue 3, Vite, Tailwind, Bootstrap

## Достижения

- −50% времени оценки соответствия
- 2× рост пропускной способности команды
- 300+ часов экономии/квартал

[Флагманский кейс →](cases/compliance-automation.md){ .md-button .md-button--primary }
[Все кейсы →](cases/compliance-automation.md){ .md-button }
""")

    create_file("docs/contacts.md", """# Контакты

- **Email**: [vladarh11v@gmail.com](mailto:vladarh11v@gmail.com)
- **GitHub**: [github.com/yourusername](https://github.com/yourusername)
- **Telegram**: [@yourusername](https://t.me/yourusername)
- **GitLab**: [gitlab.com/yourusername](https://gitlab.com/yourusername)
""")

    create_file("docs/cases/compliance-automation.md", """# Автоматизация оценки соответствия

## Проблема

Ручная оценка compliance для 40+ микросервисов занимала 2-3 недели, блокировала релизы.

## Решение

Автоматизация через GitLab CI + Ansible + custom FastAPI сервис:

- SAST/DAST интеграция
- SBOM генерация и подпись (cosign)
- Автоматические отчёты (JSON/HTML/PDF)

## Результаты

| Метрика | До | После |
|---------|-----|-------|
| Время оценки | 2-3 недели | 3-4 дня |
| Пропускная способность | 1 релиз/месяц | 2-3 релиза/месяц |
| Экономия времени | - | 300+ часов/квартал |

## Стек

- GitLab CI, Ansible
- FastAPI + PostgreSQL
- Trivy, Semgrep, ZAP
- Cosign, SBOM (Syft)
""")

    create_file("docs/cases/helm-migration.md", """# Миграция Helm-чартов

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
""")

    create_file("docs/blueprints/gitlab-ci-templates.md", """# GitLab CI шаблоны

Готовые include-файлы для типовых задач.

## SAST

```yaml
include:
  - template: Security/SAST.gitlab-ci.yml

sast:
  variables:
    SAST_EXCLUDED_PATHS: "tests/,docs/"
```

## Trivy

```yaml
trivy:
  image: aquasec/trivy:latest
  script:
    - trivy fs --exit-code 0 --severity HIGH,CRITICAL .
```

## Cosign

```yaml
sign:
  image: gcr.io/projectsigstore/cosign:latest
  script:
    - cosign sign --key $COSIGN_KEY $IMAGE
```
""")

    # Astro landing
    create_file("apps/landing/package.json", """{
  "name": "portfolio-landing",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "astro dev",
    "build": "astro build",
    "preview": "astro preview --host",
    "format": "prettier -w ."
  },
  "dependencies": {
    "astro": "^4.10.0",
    "@astrojs/tailwind": "^5.1.0",
    "@astrojs/vue": "^4.0.0",
    "vue": "^3.4.0"
  },
  "devDependencies": {
    "autoprefixer": "^10.4.18",
    "postcss": "^8.4.35",
    "tailwindcss": "^3.4.3",
    "prettier": "^3.3.2"
  }
}
""")

    create_file("apps/landing/astro.config.mjs", """import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import vue from '@astrojs/vue';

export default defineConfig({
  site: 'https://example.com',
  integrations: [
    tailwind({ applyBaseStyles: true }),
    vue()
  ],
  prefetch: true,
  output: 'static',
  trailingSlash: 'never'
});
""")

    create_file("apps/landing/tailwind.config.mjs", """/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./src/**/*.{astro,html,js,jsx,ts,tsx,vue}"
  ],
  theme: {
    extend: {
      colors: {
        primary: { DEFAULT: '#3b82f6', dark: '#2563eb', light: '#60a5fa' },
        accent: '#8b5cf6'
      },
      backgroundImage: {
        'brand-gradient': 'linear-gradient(135deg,#f0f9ff 0%,#e0f2fe 100%)',
        'text-gradient': 'linear-gradient(135deg,#3b82f6 0%,#8b5cf6 100%)'
      }
    }
  },
  plugins: []
}
""")

    create_file("apps/landing/postcss.config.cjs", """module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {}
  }
}
""")

    create_file("apps/landing/src/layouts/Base.astro", """---
const { title = "Владислав Рубцов — DevSecOps/DevOps", description = "DevSecOps/DevOps инженер и full‑stack разработчик: Ansible, GitLab CI, FastAPI, Django, Vue 3" } = Astro.props;
---
<html lang="ru" class="h-full">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width,initial-scale=1" />
    <meta name="description" content={description} />
    <meta name="theme-color" content="#3b82f6" />
    <title>{title}</title>

    <meta property="og:title" content={title} />
    <meta property="og:description" content={description} />
    <meta property="og:type" content="website" />
    <meta property="og:image" content="/og.png" />
    <link rel="icon" href="/favicon.ico" />
  </head>
  <body class="min-h-full bg-brand-gradient text-slate-800 antialiased">
    <header class="sticky top-0 z-40 backdrop-blur bg-white/70 border-b border-slate-200">
      <nav class="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
        <div class="font-extrabold text-xl bg-text-gradient bg-clip-text text-transparent">ВР</div>
        <div class="flex items-center gap-4 text-sm">
          <a href="/#stack" class="hover:text-primary">Стек</a>
          <a href="/#builder" class="hover:text-primary">CI Builder</a>
          <a href="/docs/" class="inline-flex items-center gap-2 px-3 py-1.5 rounded-full border border-primary text-primary hover:bg-primary hover:text-white transition">
            Документация
          </a>
        </div>
      </nav>
    </header>
    <main>
      <slot />
    </main>
    <footer class="mt-16 border-t border-slate-200">
      <div class="max-w-6xl mx-auto px-4 py-8 text-sm flex flex-col md:flex-row items-center justify-between gap-4">
        <p>© {new Date().getFullYear()} Владислав Рубцов</p>
        <div class="flex items-center gap-3">
          <a class="hover:text-primary" href="mailto:vladarh11v@gmail.com">Email</a>
          <a class="hover:text-primary" href="https://github.com/yourusername" target="_blank" rel="noopener noreferrer">GitHub</a>
          <a class="hover:text-primary" href="https://t.me/yourusername" target="_blank" rel="noopener noreferrer">Telegram</a>
          <a class="hover:text-primary" href="/docs/">Документация</a>
        </div>
      </div>
    </footer>
  </body>
</html>
""")

    create_file("apps/landing/src/components/Hero.astro", """---
---
<section class="py-20">
  <div class="max-w-6xl mx-auto px-4 text-center">
    <h1 class="text-4xl md:text-6xl font-extrabold leading-tight">
      <span class="bg-text-gradient bg-clip-text text-transparent">DevSecOps / DevOps инженер</span>
      <br />
      <span class="text-slate-900">Full‑Stack разработчик</span>
    </h1>
    <p class="mt-6 text-slate-600 max-w-2xl mx-auto">
      Ускоряю выпуск продукта без компромиссов по безопасности: GitLab CI, Ansible, SAST/DAST, SBOM/подпись артефактов.
      Backend — FastAPI, Django. Frontend — Vue 3 + Vite. UI — Tailwind/Bootstrap.
    </p>
    <div class="mt-8 flex items-center justify-center gap-3">
      <a href="/docs/cases/compliance-automation/" class="px-5 py-3 rounded-full bg-primary text-white font-semibold shadow hover:shadow-lg transition">Флагманский кейс</a>
      <a href="/docs/" class="px-5 py-3 rounded-full border border-primary text-primary hover:bg-primary hover:text-white transition">Вся документация</a>
    </div>
  </div>
</section>
""")

    create_file("apps/landing/src/components/Stats.astro", """<section class="pb-6">
  <div class="max-w-6xl mx-auto px-4 grid grid-cols-2 md:grid-cols-3 gap-4">
    <div class="rounded-xl border border-slate-200 bg-white p-5">
      <div class="text-3xl font-extrabold bg-text-gradient bg-clip-text text-transparent">3+</div>
      <div class="text-slate-600 text-sm mt-1">года коммерческого опыта</div>
    </div>
    <div class="rounded-xl border border-slate-200 bg-white p-5">
      <div class="text-3xl font-extrabold bg-text-gradient bg-clip-text text-transparent">6+</div>
      <div class="text-slate-600 text-sm mt-1">лет практики в ИБ</div>
    </div>
    <div class="rounded-xl border border-slate-200 bg-white p-5 col-span-2 md:col-span-1">
      <div class="text-3xl font-extrabold bg-text-gradient bg-clip-text text-transparent">50% / 2×</div>
      <div class="text-slate-600 text-sm mt-1">сокращение времени / рост пропускной способности</div>
    </div>
  </div>
</section>
""")

    create_file("apps/landing/src/components/StackChips.astro", """<section id="stack" class="py-10">
  <div class="max-w-6xl mx-auto px-4">
    <h2 class="text-xl font-bold mb-4">Стек</h2>
    <div class="grid md:grid-cols-3 gap-4">
      <div class="rounded-xl border border-slate-200 bg-white p-4">
        <div class="text-xs uppercase tracking-wide text-slate-500 font-bold mb-2">DevSecOps / DevOps</div>
        <div class="flex flex-wrap gap-2 text-sm">
          <span class="px-3 py-1 rounded-full border bg-slate-50">Ansible</span>
          <span class="px-3 py-1 rounded-full border bg-slate-50">GitLab CI</span>
          <span class="px-3 py-1 rounded-full border bg-slate-50">CI/CD</span>
          <span class="px-3 py-1 rounded-full border bg-slate-50">Cosign</span>
          <span class="px-3 py-1 rounded-full border bg-slate-50">Helm</span>
          <span class="px-3 py-1 rounded-full border bg-slate-50">Kubernetes</span>
        </div>
      </div>
      <div class="rounded-xl border border-slate-200 bg-white p-4">
        <div class="text-xs uppercase tracking-wide text-slate-500 font-bold mb-2">Backend</div>
        <div class="flex flex-wrap gap-2 text-sm">
          <span class="px-3 py-1 rounded-full border bg-slate-50">FastAPI</span>
          <span class="px-3 py-1 rounded-full border bg-slate-50">Django</span>
          <span class="px-3 py-1 rounded-full border bg-slate-50">PostgreSQL</span>
          <span class="px-3 py-1 rounded-full border bg-slate-50">Redis/Celery</span>
        </div>
      </div>
      <div class="rounded-xl border border-slate-200 bg-white p-4">
        <div class="text-xs uppercase tracking-wide text-slate-500 font-bold mb-2">Frontend / UI</div>
        <div class="flex flex-wrap gap-2 text-sm">
          <span class="px-3 py-1 rounded-full border bg-slate-50">Vue 3</span>
          <span class="px-3 py-1 rounded-full border bg-slate-50">Vite</span>
          <span class="px-3 py-1 rounded-full border bg-slate-50">Tailwind</span>
          <span class="px-3 py-1 rounded-full border bg-slate-50">Bootstrap</span>
        </div>
      </div>
    </div>
  </div>
</section>
""")

    create_file("apps/landing/src/components/CiBuilder.vue", """<template>
  <section id="builder" class="py-10">
    <div class="max-w-6xl mx-auto px-4">
      <h2 class="text-xl font-bold mb-2">CI Builder (.gitlab-ci.yml)</h2>
      <p class="text-slate-600 mb-4">Соберите минимальный пайплайн под ваш стек. Копируйте и адаптируйте.</p>

      <div class="grid md:grid-cols-3 gap-4">
        <div class="rounded-xl border border-slate-200 bg-white p-4 md:col-span-1">
          <div class="space-y-3">
            <div>
              <label class="block text-sm font-medium">Backend</label>
              <select v-model="backend" class="mt-1 w-full border rounded-lg px-3 py-2">
                <option value="fastapi">FastAPI</option>
                <option value="django">Django</option>
              </select>
            </div>

            <div>
              <label class="block text-sm font-medium">Security</label>
              <div class="mt-1 space-y-1">
                <label class="flex items-center gap-2 text-sm">
                  <input type="checkbox" v-model="sast" /> SAST
                </label>
                <label class="flex items-center gap-2 text-sm">
                  <input type="checkbox" v-model="trivy" /> Trivy (fs/image)
                </label>
                <label class="flex items-center gap-2 text-sm">
                  <input type="checkbox" v-model="zap" /> ZAP Baseline (DAST)
                </label>
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium">Деплой</label>
              <div class="mt-1 space-y-1">
                <label class="flex items-center gap-2 text-sm">
                  <input type="checkbox" v-model="ansible" /> Ansible (prod/stage)
                </label>
              </div>
            </div>

            <button @click="copy" class="mt-2 w-full px-3 py-2 rounded-lg bg-primary text-white font-semibold hover:shadow">
              Копировать YAML
            </button>
            <p v-if="copied" class="text-green-700 text-sm">Скопировано!</p>
          </div>
        </div>

        <div class="rounded-xl border border-slate-200 bg-white p-4 md:col-span-2">
          <pre class="text-xs overflow-auto"><code>{{ yaml }}</code></pre>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, ref } from 'vue';

const backend = ref('fastapi');
const sast = ref(true);
const trivy = ref(true);
const zap = ref(false);
const ansible = ref(true);
const copied = ref(false);

const yaml = computed(() => {
  const jobs = [];

  jobs.push(`# stages`);
  jobs.push(`stages: [lint, test, build${(sast.value||trivy.value||zap.value)?', security':''}${ansible.value?', deploy':''}]`);
  jobs.push(``);

  jobs.push(`# lint`);
  jobs.push(`lint:`);
  jobs.push(`  stage: lint`);
  jobs.push(`  image: node:20-alpine`);
  jobs.push(`  script:`);
  jobs.push(`    - pnpm -v || npm i -g pnpm`);
  jobs.push(`    - pnpm -C frontend lint || echo "no frontend lint"`);
  jobs.push(`    - ruff --version || pip install ruff`);
  jobs.push(`    - ruff ${backend.value === 'django' ? 'backend' : 'app'} || echo "ruff soft"`);

  jobs.push(``);
  jobs.push(`# test`);
  jobs.push(`test:`);
  jobs.push(`  stage: test`);
  jobs.push(`  image: python:3.11`);
  jobs.push(`  script:`);
  jobs.push(`    - pip install -r requirements.txt || true`);
  jobs.push(`    - pytest -q || echo "no tests"`);

  jobs.push(``);
  jobs.push(`# build`);
  jobs.push(`build:`);
  jobs.push(`  stage: build`);
  if (backend.value === 'django') {
    jobs.push(`  image: node:20-alpine`);
    jobs.push(`  script:`);
    jobs.push(`    - echo "build frontend if exists"`);
    jobs.push(`    - echo "collect static for Django in release stage"`);
  } else {
    jobs.push(`  image: python:3.11`);
    jobs.push(`  script:`);
    jobs.push(`    - echo "build fastapi image in release pipeline"`);
  }
  jobs.push(`  artifacts: { when: always }`);

  if (sast.value || trivy.value || zap.value) {
    jobs.push(``);
    jobs.push(`# security`);
    if (sast.value) {
      jobs.push(`security:sast:`);
      jobs.push(`  stage: security`);
      jobs.push(`  image: registry.gitlab.com/security-products/sast:latest`);
      jobs.push(`  script: ["/analyzer run"]`);
      jobs.push(`  artifacts: { reports: { sast: gl-sast-report.json }, when: always }`);
    }
    if (trivy.value) {
      jobs.push(`security:trivy:`);
      jobs.push(`  stage: security`);
      jobs.push(`  image: aquasec/trivy:latest`);
      jobs.push(`  script:`);
      jobs.push(`    - trivy fs --exit-code 0 --severity HIGH,CRITICAL .`);
      jobs.push(`  artifacts: { when: always }`);
    }
    if (zap.value) {
      jobs.push(`security:zap:`);
      jobs.push(`  stage: security`);
      jobs.push(`  image: owasp/zap2docker-stable`);
      jobs.push(`  variables: { APP_URL: $PREVIEW_URL }`);
      jobs.push(`  script:`);
      jobs.push(`    - zap-baseline.py -t $APP_URL -r dast.html || true`);
      jobs.push(`  artifacts: { paths: [dast.html], when: always }`);
    }
  }

  if (ansible.value) {
    jobs.push(``);
    jobs.push(`# deploy`);
    jobs.push(`deploy:`);
    jobs.push(`  stage: deploy`);
    jobs.push(`  image: alpine:3.19`);
    jobs.push(`  script:`);
    jobs.push(`    - apk add --no-cache ansible openssh`);
    jobs.push(`    - ansible --version`);
    jobs.push(`    - ansible-playbook deploy.yml -i inventory/stage --check || true`);
    jobs.push(`  when: manual`);
    jobs.push(`  allow_failure: true`);
  }

  return jobs.join('\\n');
});

const copy = async () => {
  await navigator.clipboard.writeText(yaml.value);
  copied.value = true;
  setTimeout(() => (copied.value = false), 1500);
};
</script>

<style scoped>
pre { white-space: pre; }
</style>
""")

    create_file("apps/landing/src/pages/index.astro", """---
import Base from "../layouts/Base.astro";
import Hero from "../components/Hero.astro";
import Stats from "../components/Stats.astro";
import StackChips from "../components/StackChips.astro";
import CiBuilder from "../components/CiBuilder.vue";
---
<Base>
  <Hero />
  <Stats />
  <StackChips />
  <CiBuilder client:visible />
  <section class="py-12">
    <div class="max-w-6xl mx-auto px-4 grid md:grid-cols-3 gap-4">
      <a href="/docs/cases/compliance-automation/" class="rounded-xl border border-slate-200 bg-white p-5 hover:shadow-lg transition">
        <div class="text-sm text-slate-500">Кейс</div>
        <div class="text-lg font-bold">Автоматизация оценки соответствия</div>
        <p class="text-slate-600 mt-2 text-sm">−50% времени, 2× throughput, 300+ часов экономии.</p>
      </a>
      <a href="/docs/cases/helm-migration/" class="rounded-xl border border-slate-200 bg-white p-5 hover:shadow-lg transition">
        <div class="text-sm text-slate-500">Кейс</div>
        <div class="text-lg font-bold">Миграция Helm‑чартов</div>
        <p class="text-slate-600 mt-2 text-sm">Автоматизация multi‑source/target, подписи cosign.</p>
      </a>
      <a href="/docs/blueprints/gitlab-ci-templates/" class="rounded-xl border border-slate-200 bg-white p-5 hover:shadow-lg transition">
        <div class="text-sm text-slate-500">Blueprint</div>
        <div class="text-lg font-bold">GitLab CI шаблоны</div>
        <p class="text-slate-600 mt-2 text-sm">Готовые include‑файлы для быстрых стартов.</p>
      </a>
    </div>
  </section>
</Base>
""")

    # README
    create_file("README.md", """# Portfolio Hybrid (Astro + MkDocs)

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
""")

    print(f"\n✅ Структура создана!\n")
    print("Следующие шаги:")
    print("\n1. MkDocs документация:")
    print("   pip install -r requirements.txt")
    print("   mkdocs serve")
    print("\n2. Astro лендинг:")
    print("   cd apps/landing")
    print("   npm install")
    print("   npm run dev")
    print("\n3. Замените 'yourusername' на реальные ссылки")
    print("4. Push в GitLab main → автодеплой через Pages\n")

if __name__ == "__main__":
    main()