import yaml
import json
import os
from pathlib import Path
from datetime import datetime

def convert_yaml_to_json():
    
    yaml_path = Path('docs/openapi-spec/openapi.yaml')
    json_path = Path('docs/openapi-generated/openapi.json')
    json_min_path = Path('docs/openapi-generated/openapi.min.json')
    
    json_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(yaml_path, 'r', encoding='utf-8') as f:
        spec = yaml.safe_load(f)
    
    spec['info']['x-generated'] = {
        'timestamp': datetime.now().isoformat(),
        'generator': 'generate_openapi.py',
        'version': '1.0.0'
    }
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(spec, f, indent=2, ensure_ascii=False)
    
    with open(json_min_path, 'w', encoding='utf-8') as f:
        json.dump(spec, f, separators=(',', ':'), ensure_ascii=False)
    
    print(f"OpenAPI JSON сгенерирован: {json_path}")
    print(f"Минифицированная версия: {json_min_path}")
    
    return spec

def generate_html_docs(spec):
    
    html_template = """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>API Документация - Махачкала</title>
        <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            body { margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
            #swagger-ui { padding: 20px; }
            .header { 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white; 
                padding: 20px; 
                text-align: center;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            .header h1 { margin: 0; font-size: 28px; }
            .header p { margin: 10px 0 0; opacity: 0.9; }
            .info-box { 
                background: #f8f9fa; 
                border-left: 4px solid #667eea;
                padding: 15px; 
                margin: 20px; 
                border-radius: 4px;
            }
            .download-links { margin: 20px; }
            .download-links a { 
                display: inline-block; 
                margin-right: 10px; 
                padding: 10px 15px;
                background: #667eea; 
                color: white; 
                text-decoration: none;
                border-radius: 4px;
                transition: background 0.3s;
            }
            .download-links a:hover { background: #764ba2; }
            .footer { 
                text-align: center; 
                padding: 20px; 
                color: #666; 
                font-size: 14px;
                border-top: 1px solid #eee;
                margin-top: 30px;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1><i class="fas fa-utensils"></i> API Документация - Махачкала</h1>
            <p>Сеть ресторанов с шаурмой за 5 рублей</p>
        </div>
        
        <div class="info-box">
            <h3><i class="fas fa-info-circle"></i> Информация</h3>
            <p>Версия API: <strong>{{version}}</strong></p>
            <p>Сгенерировано: <strong>{{timestamp}}</strong></p>
            <p>Базовый URL: <code>{{base_url}}</code></p>
        </div>
        
        <div class="download-links">
            <a href="openapi.json" download><i class="fas fa-download"></i> Скачать JSON</a>
            <a href="openapi.min.json" download><i class="fas fa-download"></i> Скачать минифицированный JSON</a>
            <a href="openapi.yaml" download><i class="fas fa-download"></i> Скачать YAML</a>
        </div>
        
        <div id="swagger-ui"></div>
        
        <div class="footer">
            <p>Проект "Махачкала" | Команда Alhamdulillah | ФПМИ БГУ 2024-2025</p>
            <p>
                <a href="https://github.com/fpmi-hci-2025/project11a-alhamdulillah" style="color: #667eea;">
                    <i class="fab fa-github"></i> GitHub репозиторий
                </a>
            </p>
        </div>
        
        <script src="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui-bundle.js"></script>
        <script src="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui-standalone-preset.js"></script>
        <script>
            window.onload = function() {
                const ui = SwaggerUIBundle({
                    url: "openapi.json",
                    dom_id: '#swagger-ui',
                    deepLinking: true,
                    presets: [
                        SwaggerUIBundle.presets.apis,
                        SwaggerUIStandalonePreset
                    ],
                    plugins: [
                        SwaggerUIBundle.plugins.DownloadUrl
                    ],
                    layout: "StandaloneLayout",
                    validatorUrl: null,
                    defaultModelsExpandDepth: -1,
                    docExpansion: 'list',
                    filter: true,
                    displayRequestDuration: true
                });
                
                window.ui = ui;
            }
        </script>
    </body>
    </html>
    """
    
    html_content = html_template.replace('{{version}}', spec['info']['version'])
    html_content = html_content.replace('{{timestamp}}', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    html_content = html_content.replace('{{base_url}}', spec['servers'][0]['url'] if spec.get('servers') else '/')
    
    html_path = Path('docs/openapi-generated/index.html')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"HTML документация сгенерирована: {html_path}")

def copy_yaml_spec():
    import shutil
    
    src = Path('docs/openapi-spec/openapi.yaml')
    dst = Path('docs/openapi-generated/openapi.yaml')
    
    if src.exists():
        shutil.copy2(src, dst)
        print(f"YAML спецификация скопирована: {dst}")
    else:
        print(f"YAML файл не найден: {src}")

def main():
    print("🚀 Начало генерации OpenAPI документации...")
    
    try:
        spec = convert_yaml_to_json()
        
        copy_yaml_spec()
        
        generate_html_docs(spec)
        
        readme_content = """# OpenAPI Документация для проекта "Махачкала"

Автоматически сгенерированная документация API.

## Файлы

- `openapi.yaml` - исходная спецификация в YAML
- `openapi.json` - спецификация в JSON (форматированная)
- `openapi.min.json` - спецификация в JSON (минифицированная)
- `index.html` - интерактивная документация (Swagger UI)

## Использование

### Для разработчиков
1. Используйте `openapi.json` для генерации клиентских библиотек
2. Используйте `openapi.yaml` для импорта в Postman/Swagger Editor

### Для тестирования
1. Откройте `index.html` в браузере
2. Используйте интерактивную документацию для тестирования API

## Генерация

Документация генерируется автоматически при изменении `openapi.yaml`
или вручную через GitHub Actions.

## Ссылки

- [GitHub репозиторий](https://github.com/fpmi-hci-2025/project11a-alhamdulillah)
- [GitHub Pages](https://fpmi-hci-2025.github.io/project11a-alhamdulillah/)
"""
        
        with open('docs/openapi-generated/README.md', 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print("Генерация документации завершена успешно!")
        
    except Exception as e:
        print(f"Ошибка генерации: {e}")
        raise

if __name__ == "__main__":
    main()