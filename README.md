# **Explicação da Lógica do Sistema de Processos**

Este sistema foi desenvolvido para facilitar o gerenciamento de **processos jurídicos ou administrativos**, surgindo de uma demanda real da empresa onde trabalho. Nesse sistema é possível cadastrar, consultar, atualizar e remover processos.

## **Objetivo do Sistema**

Fornecer uma maneira atual e eficiente de acompanhar processos, armazenando informações essenciais como:

- Número do processo
- Descrição
- Datas importantes
- Atualização de Processos

---

## **Funcionalidades Principais**

### 1. **Gerenciamento de Processos**

- Cadastro de novos processos com número único
- Inclusão de descrição, data de início e data de fim
- Listagem de todos os processos cadastrados
- Consulta por número do processo
- Atualização de dados de um processo
- Remoção de um processo existente

---

## Como Rodar o Sistema

1. **Clone o repositório:**

```bash
git clone https://github.com/seu_usuario/sistema-monitoria.git
```

2. **Instale as dependências:**

```bash
pip install -r requirements.txt
```

3. **Inicie o servidor:**

```bash
flask run --host 0.0.0.0 --port 5000 --reload
```

4. **Acesse a aplicação:**  
   [http://localhost:5000](http://localhost:5000)

---
