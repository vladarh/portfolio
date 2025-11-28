# GitLab CI шаблоны

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
