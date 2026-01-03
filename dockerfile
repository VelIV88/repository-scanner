# Используем официальный Python образ как базовый
FROM python:3.11-slim

# Устанавливаем необходимые системные пакеты
RUN apt-get update && apt-get install -y \
    curl \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем gitleaks
RUN curl -sSfL https://github.com/gitleaks/gitleaks/releases/download/v8.18.1/gitleaks_8.18.1_linux_x64.tar.gz | \
    tar -xz -C /usr/local/bin && \
    chmod +x /usr/local/bin/gitleaks

# Создаем рабочую директорию
WORKDIR /workspace

# Копируем скрипт запуска сканера
COPY local-scanner.sh /usr/local/bin/local-scanner
RUN chmod +x /usr/local/bin/local-scanner

# Копируем скрипт обработки отчетов
COPY reports_processing.py /workspace/reports_processing.py

# Включаем настройку безопасности владения гит реп
RUN git config --global --add safe.directory '*'

# Устанавливаем переменные окружения
ENV PATH="/usr/local/bin:${PATH}"

# Проверяем установку
RUN python --version && \
    bash --version && \
    gitleaks version

ENTRYPOINT ["local-scanner"]