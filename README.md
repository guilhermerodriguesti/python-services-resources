# python-services-resources


Primeiro, o programa verifica se o recurso existe

Se o recurso existe e o parâmetro delete estiver habilitado, o recurso é deletado

Se o recurso existe e o parâmetro delete não foi habilitado,o recurso é atualizado

Se o recurso não existe, o recurso é atualizado com base nos parametros do arquivo json


# teste 1
```
import os
import argparse

# Criando um parser para os argumentos da linha de comando
parser = argparse.ArgumentParser()
parser.add_argument('filename', type=str, help='Nome do arquivo')
parser.add_argument('content', type=str, help='Conteúdo do arquivo')
parser.add_argument('--delete', action='store_true', help='Deletar o arquivo, se já existir')
args = parser.parse_args()

# Verificando se o arquivo já existe
if os.path.isfile(args.filename):
    # Deletando o arquivo, se o parâmetro delete estiver habilitado
    if args.delete:
        os.remove(args.filename)
    # Atualizando o arquivo
    else:
        with open(args.filename, 'w') as f:
            f.write(args.content)
# Criando o arquivo, se ele não existir
else:
    with open(args.filename, 'w') as f:
        f.write(args.content)
        
```
## teste 2
```
import boto3
import json
import argparse

# Configurações do boto3
ecs_client = boto3.client('ecs')

# Definição dos argumentos da linha de comando
parser = argparse.ArgumentParser(description='Gerenciamento de recursos ECS')
parser.add_argument('--name', type=str, required=True, help='Nome do recurso a ser gerenciado')
parser.add_argument('--json', type=str, required=True, help='Arquivo JSON com as configurações do recurso')
parser.add_argument('--delete', action='store_true', help='Se definido, o recurso será deletado')
args = parser.parse_args()

# Verificação da existência do recurso
try:
    response = ecs_client.describe_task_definition(
        taskDefinition=args.name
    )
    exists = True
except ecs_client.exceptions.ClientError as e:
    exists = False

# Gerenciamento do recurso
if exists and args.delete:
    # Deletando o recurso
    response = ecs_client.deregister_task_definition(
        taskDefinition=args.name
    )
    print(f'Recurso {args.name} deletado com sucesso')

elif exists:
    # Atualizando o recurso
    with open(args.json, 'r') as file:
        task_definition = json.load(file)
    response = ecs_client.register_task_definition(
        family=args.name,
        containerDefinitions=task_definition['containerDefinitions']
    )
    print(f'Recurso {args.name} atualizado com sucesso')

else:
    # Criando o recurso
    with open(args.json, 'r') as file:
        task_definition = json.load(file)
    response = ecs_client.register_task_definition(
        family=args.name,
        containerDefinitions=task_definition['containerDefinitions']
    )
    print(f'Recurso {args.name} criado com sucesso')

```