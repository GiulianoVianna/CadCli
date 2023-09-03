# Sobre o Projeto

Este é um projeto de cadastro de clientes desenvolvido em Python com a biblioteca PyQt5 para interface gráfica. Ele fornece uma forma prática de gerenciar informações sobre clientes, seja pessoa física ou jurídica.

![image](https://github.com/GiulianoVianna/SIG/assets/101942554/29296724-0b87-4eb3-9928-6338bb0d4975)


## Funcionalidades

- **Cadastro de Clientes**: Permite cadastrar informações básicas como nome, CPF (para pessoas físicas) e CNPJ (para pessoas jurídicas).
- **Edição e Exclusão**: Possibilita editar ou excluir registros existentes.
- **Filtragem**: Permite visualizar registros filtrados por nome através de um ComboBox.
- **Validação**: Realiza validação básica de campos para garantir que as informações necessárias sejam preenchidas.
- **Validação de CPF/CNPJ**: Implementa algoritmos para validar a estrutura do CPF e CNPJ inseridos, garantindo dados mais confiáveis.

## Como Usar

- **Instalação**: Certifique-se de ter o Python e o PyQt5 instalados em sua máquina.
- **Execução**: Execute o arquivo principal do projeto para abrir a interface gráfica.
- **Cadastro**: Preencha os campos e clique no botão "Salvar" para cadastrar um novo cliente.
- **Edição/Exclusão**: Selecione um registro na tabela e utilize os botões "Editar" ou "Excluir" conforme a necessidade.

## Estrutura de Código

O projeto é orientado a objetos e utiliza os seguintes métodos e classes principais:

- `class MinhaJanela(QMainWindow)`: Classe principal que gerencia a interface gráfica e a lógica do programa.
- `configurar_interface()`: Carrega a interface do usuário e inicializa componentes da UI.
- `conectar_eventos()`: Conecta os eventos da interface com seus respectivos métodos.
- `cadastrar()`: Realiza o cadastro de um novo cliente.
- `editar()`: Edita um registro selecionado.
- `excluir()`: Exclui um registro selecionado.
- `validar_cpf()`: Valida o CPF inserido.
- `validar_cnpj()`: Valida o CNPJ inserido.

## Requisitos

- Python 3.x
- PyQt5
