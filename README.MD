## Образ приложения сканера локальных репозиториев
Предназначен для сканирования клонированных на локальную машину удалённых репозиториев. Основан на приложении `gitleaks`. 
После сканирования `python` скрипт обрабатывает отчеты: пустые - удаляются, к найденым уязвимостям добавляется ссылка на коммит в удалённом репозитории.
Для нормальной работы на Windows клонируйте репо с помощью команды:
```bash
git clone --config core.autocrlf=false <url-репозитория>
```
либо установите глобальный параметр для git:
```bash
git config --global core.autocrlf false
```

### Сборка.
``` bash
docker build -t gitleaks-scanner .
```

### Запуск.
Клонируем репозитории для сканирования в каталог `./repositories/`.  
Запуск сканирования всех папок в каталоге `./repositories/` (результаты попадут в каталог `/reports/*.json`):
#### Unix:
``` bash
docker run --rm -v $(pwd):/workspace gitleaks-scanner
```
Для сканирования конкретного репозитория передаём `REPOSITORY_NAME` папки из `./repositories/` параметром (результат попадёт в файл `/reports/REPOSITORY_NAME.json`):
``` bash
docker run --rm -v $(pwd):/workspace gitleaks-scanner REPOSITORY_NAME
```
#### Windows:
``` bash
docker run --rm -v ${PWD}:/workspace gitleaks-scanner
```
Для сканирования конкретного репозитория передаём `REPOSITORY_NAME` папки из `./repositories/` параметром (результат попадёт в файл `/reports/REPOSITORY_NAME.json`):
``` bash
docker run --rm -v ${PWD}:/workspace gitleaks-scanner REPOSITORY_NAME
```
В консоль будут выводиться результаты сканирования от gitleaks, в каталоге `/reports/` останутся только отредактированные отчеты с найденными кредами