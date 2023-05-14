import json
import boto3
import argparse
from botocore.exceptions import ClientError


def get_service_info(service_name, cluster_name):
    ecs = boto3.client('ecs')
    try:
        response = ecs.describe_services(
            services=[service_name],
            cluster=cluster_name
        )
        return response['services'][0]
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            return None
        else:
            raise e

def create_service(service_name, cluster_name, json_file):
    ecs = boto3.client('ecs')
    with open(json_file) as f:
        service_params = json.load(f)
    response = ecs.create_service(
        serviceName=service_name,
        cluster=cluster_name,
        **service_params
    )
    return response

def update_service(service_name, cluster_name, json_file):
    ecs = boto3.client('ecs')
    with open(json_file) as f:
        service_params = json.load(f)
    service_info = get_service_info(service_name, cluster_name)
    if service_info:
        ecs.update_service(
            service=service_name,
            cluster=cluster_name,
            **service_params
        )
        print(f'Serviço {service_name} atualizado com sucesso.')
    else:
        create_service(service_name, cluster_name, json_file)
        print(f'Serviço {service_name} criado com sucesso.')

def delete_service(service_name, cluster_name):
    ecs = boto3.client('ecs')
    ecs.delete_service(
        service=service_name,
        cluster=cluster_name
    )
    print(f'Serviço {service_name} excluído com sucesso.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Script para atualizar ou criar um serviço ECS na AWS com base em um arquivo JSON.')
    parser.add_argument('service_name', type=str, help='Nome do serviço ECS.')
    parser.add_argument('cluster_name', type=str, help='Nome do cluster ECS.')
    parser.add_argument('json_file', type=str, help='Caminho para o arquivo JSON que contém as configurações do serviço.')
    parser.add_argument('--delete', action='store_true', help='Se fornecido, exclui o serviço caso já exista.')
    args = parser.parse_args()

    if args.delete:
        delete_service(args.service_name, args.cluster_name)
    else:
        update_service(args.service_name, args.cluster_name, args.json_file)

