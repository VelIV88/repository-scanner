import re
import subprocess
import sys
import os
import json

def get_https_url(local_repo_path="."):
    """
    Получает HTTPS URL удаленного репозитория
    
    :param local_repo_path: путь до локального репозитория
    """
    try:
        # Получаем URL из локального репозитория
        result = subprocess.run(
            ["git", "config", "--get", "remote.origin.url"],
            cwd=local_repo_path,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if result.returncode != 0 or not result.stdout.strip():
            return None
        
        url = result.stdout.strip()
        
        # Если уже HTTPS или HTTP - возвращаем как есть
        if url.startswith(('http')):
            return url
        
        https_url = convert_to_https(url)
        
        return https_url
        
    except Exception as e:
        print(f"Что-то пошло не так: {e}")
        return None

def convert_to_https(git_url):
    """
    Конвертирует различные форматы Git URL в HTTPS
    
    :param git_url: SSH URL git репозитория
    
    """
    
    ssh_patterns = [
        # git@host:user/repo.git
        r'^git@([^:]+):(.+?)(?:\.git)?$',
        # ssh://git@host/path
        r'^ssh://git@([^/]+)/(.+?)(?:\.git)?$',
        # ssh://user@host/path
        r'^ssh://([^@]+)@([^/]+)/(.+?)(?:\.git)?$'
    ]
    
    for pattern in ssh_patterns:
        match = re.match(pattern, git_url)
        if match:
            if len(match.groups()) == 2:
                # git@host:user/repo
                host, path = match.groups()
                return f"https://{host}/{path}"
            elif len(match.groups()) == 3:
                # ssh://user@host/path
                _, host, path = match.groups()
                return f"https://{host}/{path}"
    
    # Для других случаев возвращаем оригинал
    return git_url

def create_commit_url(project_url, commit_name):
    """
    Создает ссылку на коммит с секретом
    
    :param project_url: URL git репозитория
    :param commit_name: имя коммита
    """
    return project_url + "/commit/" + commit_name

def process_report(data):
    """
    Функия для обогащения отчета ссылкой на коммит и удаления лишних полей
    
    :param data: JSON из отчета gitleack
    """
    return {
            "Link" : create_commit_url(repository_https_url, data.get("Commit")),
            "Description": data.get("Description"),
            "StartLine": data.get("StartLine"),
            "EndLine": data.get("EndLine"),
            "StartColumn": data.get("StartColumn"),
            "EndColumn": data.get("EndColumn"),
            "Match": data.get("Match"),
            "Secret": data.get("Secret"),
            "File": data.get("File"),
            "Author": data.get("Author"),
            "Email": data.get("Email"),
            "Date": data.get("Date"),
        }

def get_report_info(report_path):
    """
    Функция для получения отчета в виде JSON
    
    :param report_path: путь к отчету
    """
    with open(report_path, encoding="utf-8") as inp_file:
        reports = json.load(inp_file)

    return reports
        
def write_reports(report_path, data):
    """
    Функция для записи обработанного результата
    
    :param report_path: Путь до отчета
    :param data: Обработанные данные
    """
    with open(report_path, "w", encoding="utf-8") as out_file:
        json.dump(data, out_file, indent=4)


if __name__ == "__main__":
    args = sys.argv

    if len(args) != 3:
        raise ValueError(f"Ожидается передача только пути до репозитория и пути до отчета {args}")
    
    repo_path = args[1]
    report_path = args[2]

    repository_https_url = get_https_url(repo_path)

    reports =  get_report_info(report_path)

    result = [
        process_report(report) for report in reports if report
    ]

    if result:
        write_reports(report_path, result)
    else:
        os.remove(report_path)
