#!/usr/bin/env python3
"""
Преобразует OpenAPI YAML в HTML документацию
"""

import yaml
import json
from pathlib import Path
from datetime import datetime, date

def convert_for_json(obj):
    """Рекурсивно преобразует datetime и date в строки"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    elif isinstance(obj, dict):
        return {k: convert_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_for_json(item) for item in obj]
    else:
        return obj

def main():
    # Пути к файлам
    yaml_path = Path('docs/openapi-spec/openapi.yaml')
    output_dir = Path('docs/openapi-generated')
    
    # Создаем директории
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Загружаем YAML
    if not yaml_path.exists():
        print(f"Файл не найден: {yaml_path}")
        return 1
    
    with open(yaml_path, 'r', encoding='utf-8') as f:
        spec = yaml.safe_load(f)
    
    # Преобразуем все даты и datetime в строки
    spec = convert_for_json(spec)
    
    # Конвертируем в JSON для Swagger UI
    spec_json = json.dumps(spec, ensure_ascii=False)
    
    # Экранируем для JS
    spec_json_escaped = spec_json.replace('</script>', '<\\/script>')
    
    # Генерируем HTML
    title = spec.get('info', {}).get('title', 'API Documentation')
    html_content = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui.css">
</head>
<body>
    <div id="swagger-ui"></div>
    
    <script id="openapi-spec" type="application/json">
{spec_json_escaped}
    </script>
    
    <script src="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui-bundle.js"></script>
    <script>
        const spec = JSON.parse(document.getElementById('openapi-spec').textContent);
        window.onload = function() {{
            SwaggerUIBundle({{
                spec: spec,
                dom_id: '#swagger-ui',
                deepLinking: true
            }});
        }};
    </script>
</body>
</html>'''
    
    # Сохраняем HTML
    html_path = output_dir / 'index.html'
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"HTML документация создана: {html_path}")
    return 0

if __name__ == "__main__":
    exit(main())