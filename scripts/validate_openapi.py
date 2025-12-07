import json
import yaml
import jsonschema
from pathlib import Path

def validate_openapi_schema(spec):
    
    openapi_schema = {
        "type": "object",
        "required": ["openapi", "info", "paths"],
        "properties": {
            "openapi": {"type": "string", "pattern": "^3\\.0\\.\\d+$"},
            "info": {
                "type": "object",
                "required": ["title", "version"],
                "properties": {
                    "title": {"type": "string"},
                    "version": {"type": "string"}
                }
            },
            "paths": {"type": "object"}
        }
    }
    
    try:
        jsonschema.validate(instance=spec, schema=openapi_schema)
        print("Спецификация соответствует OpenAPI 3.0")
        return True
    except jsonschema.ValidationError as e:
        print(f"Ошибка валидации: {e}")
        return False

def check_required_endpoints(spec):
    required_paths = [
        '/auth/register',
        '/auth/login',
        '/restaurants',
        '/dishes',
        '/orders',
        '/promotions'
    ]
    
    missing_paths = []
    
    for path in required_paths:
        if path not in spec.get('paths', {}):
            missing_paths.append(path)
    
    if missing_paths:
        print(f"Отсутствуют обязательные эндпоинты: {missing_paths}")
        return False
    
    print("Все обязательные эндпоинты присутствуют")
    return True

def check_examples(spec):
    paths_with_examples = 0
    total_paths = len(spec.get('paths', {}))
    
    for path, methods in spec.get('paths', {}).items():
        for method, details in methods.items():
            if 'responses' in details:
                for code, response in details['responses'].items():
                    if 'content' in response:
                        for content_type, content in response['content'].items():
                            if 'example' in content or 'examples' in content:
                                paths_with_examples += 1
                                break
    
    coverage = (paths_with_examples / total_paths * 100) if total_paths > 0 else 0
    
    print(f"Примеры покрывают {coverage:.1f}% эндпоинтов ({paths_with_examples}/{total_paths})")
    return coverage > 50

def main():
    print("🔍 Валидация OpenAPI спецификации...")
    
    try:
        json_path = Path('docs/openapi-generated/openapi.json')
        
        if not json_path.exists():
            yaml_path = Path('docs/openapi-spec/openapi.yaml')
            with open(yaml_path, 'r', encoding='utf-8') as f:
                spec = yaml.safe_load(f)
        else:
            with open(json_path, 'r', encoding='utf-8') as f:
                spec = json.load(f)
        
        checks = [
            ("Соответствие схеме OpenAPI 3.0", validate_openapi_schema(spec)),
            ("Обязательные эндпоинты", check_required_endpoints(spec)),
            ("Наличие примеров", check_examples(spec))
        ]
        
        print("\nРезультаты валидации:")
        for name, result in checks:
            status = "SUCCESS" if result else "INVALID"
            print(f"  {status} {name}")
        
        all_passed = all(result for _, result in checks)
        
        if all_passed:
            print("\nВсе проверки пройдены!")
        else:
            print("\n⚠Некоторые проверки не пройдены")
            exit(1)
            
    except Exception as e:
        print(f"Ошибка при валидации: {e}")
        exit(1)

if __name__ == "__main__":
    main()