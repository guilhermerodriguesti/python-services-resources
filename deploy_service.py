import os
import json
from typing import Dict, Optional
from dotenv import dotenv_values


class ServiceNotFound(Exception):
    pass

def get_resource_data(resource_id: str) -> Optional[dict]:
    """Obtém os dados de um recurso com um determinado ID"""
    with open("resources.json", "r") as f:
        data = json.load(f)
    for resource in data["resources"]:
        if resource["id"] == resource_id:
            return resource
    raise ServiceNotFound(f"Recurso com ID {resource_id} não encontrado")


def check_resource(resource_id: str) -> Optional[dict]:
    """Verifica se um recurso existe ou não"""
    print(f"Verificando recurso com ID {resource_id}")
    try:
        resource_data = get_resource_data(resource_id)
        print(f"Recurso encontrado com ID {resource_data['id']}, região {resource_data['region']}, cluster {resource_data['cluster']}, nome {resource_data['name']}, alb {resource_data['alb']}, dns {resource_data['dns']}")
        return resource_data
    
    except ServiceNotFound as e:
        print(f"Erro ao verificar serviço: {e}")
        return None


def create_resource(resource_data: dict) -> None:
    """Creates a new resource with the specified properties"""
    with open("resources.json", "r+") as f:
        file_data = json.load(f)
        file_data["resources"].append(resource_data)
        f.seek(0)
        json.dump(file_data, f, indent=4)
        f.truncate()
    print(f"Resource with ID {resource_data['id']} created successfully")

def update_resource(resource_data: dict, destroy: bool = False) -> None:
    print(f"Updating resource with data: {resource_data}")
    
    if destroy:
        delete_resource(resource_data['id'])
    else:
        
        with open("resources.json", "r+") as f:
            file_data = json.load(f)
            for i, resource in enumerate(file_data["resources"]):
                if resource["id"] == resource_data["id"]:
                    file_data["resources"][i] = resource_data
                    f.seek(0)
                    json.dump(file_data, f, indent=4)
                    f.truncate()
                    print(f"Resource with ID {resource_data['id']} updated successfully.")
                    return

            print(f"Resource with ID {resource_data['id']} not found.")


def delete_resource(resource_id: str) -> None:
    print(f"Deleting resource with ID {resource_id}")
    
    with open("resources.json", "r+") as f:
        file_data = json.load(f)
        for i, resource in enumerate(file_data["resources"]):
            if resource["id"] == resource_id:
                del file_data["resources"][i]
                f.seek(0)
                json.dump(file_data, f, indent=4)
                f.truncate()
                print(f"Resource with ID {resource_id} deleted successfully.")
                return

        print(f"Resource with ID {resource_id} not found.")


def load_resource_data() -> Dict[str, Optional[str]]:
    # Carrega as variáveis definidas no arquivo .env em um dicionário
    env_vars = dotenv_values(".env")

    # Cria um dicionário vazio para armazenar os dados
    resource_data = {}

    # Itera sobre as chaves do dicionário env_vars para obter os valores das variáveis de ambiente
    for var in env_vars:
        value = os.environ.get(var)
        if value is not None:
            resource_data[var] = value
        else:
            resource_data[var] = env_vars[var]

    return resource_data


def main(resource_data: dict) -> None:
    for key, value in resource_data.items():
        print(f"{key}: {value}")
    
    
    resource = check_resource(resource_data['id'])

    if resource:
        update_resource(resource_data, resource_data.get('destroy', False))
    else:
        create_resource(resource_data)


if __name__ == '__main__':
    resource_data = load_resource_data()
    if resource_data is not None:
        main(resource_data)
