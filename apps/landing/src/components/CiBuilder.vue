<template>
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

  return jobs.join('\n');
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
