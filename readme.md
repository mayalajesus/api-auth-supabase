# API-AUTH-SUPABASE

**Simplifique e potencialize a autenticação em sua aplicação com segurança e eficiência.**

![License](https://img.shields.io/github/license/mayalajesus/api-auth-supabase?style=default&logo=opensourceinitiative&logoColor=white&color=0080ff)
![Last Commit](https://img.shields.io/github/last-commit/mayalajesus/api-auth-supabase?style=default&logo=git&logoColor=white&color=0080ff)
![Top Language](https://img.shields.io/github/languages/top/mayalajesus/api-auth-supabase?style=default&color=0080ff)
![Language Count](https://img.shields.io/github/languages/count/mayalajesus/api-auth-supabase?style=default&color=0080ff)

---

## Índice

- [Visão Geral](#visão-geral)
- [Funcionalidades](#funcionalidades)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Roteiro do Projeto](#roteiro-do-projeto)
---

## 🎯 Visão Geral

API-AUTH-SUPABASE é uma API desenvolvida com **FastAPI** e integrada ao **Supabase** para fornecer autenticação segura, eficiente e personalizável para aplicações. Ideal para desenvolvedores que buscam uma solução rápida e robusta para gerenciar login, cadastro e exclusão de usuários.

### Principais Benefícios:
- **Segurança em Primeiro Lugar**: Criptografia e validação de credenciais.
- **Integração Simples**: Facilmente adaptável a projetos existentes.
- **Alta Performance**: Construída sobre tecnologias modernas como FastAPI e Supabase.

---

## 🚀 Funcionalidades

| Recurso          | Descrição                                                                                         |
| ----------------- | ------------------------------------------------------------------------------------------------ |
| **Cadastro de Usuários** | Permite criar novos usuários com validação de e-mail e senha forte.                         |
| **Login**          | Garante autenticação segura e feedback claro para credenciais inválidas.                         |
| **Exclusão de Conta** | Remove usuários cadastrados de forma eficiente.                                                |
| **Listagem de Usuários** | Gera relatórios de e-mails cadastrados (requer credenciais específicas).                     |
| **Validação de Senhas** | Força mínima: 6 caracteres, incluindo maiúsculas, minúsculas e caracteres especiais.          |
| **Integração com Supabase** | Utiliza Supabase para gestão de autenticação, escalabilidade e persistência.             |

---

## 🗂️ Estrutura do Projeto

```plaintext
└── api-auth-supabase/
    └── auth.py  # Arquivo principal com a lógica de autenticação.
```

## 🛤️ Roteiro do Projeto

- [X] **Implementar cadastro de usuários.**
- [X] **Implementar login com validação de senha.**
- [X] **Listar usuários registrados.**
- [ ] **Melhorar mensagens de erro e tratamento de exceções.**
- [ ] **Adicionar testes unitários mais abrangentes.**
