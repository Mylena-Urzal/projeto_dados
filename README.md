 Dashboard de Vendas - Loja de Informática

 🔴 [CLIQUE AQUI PARA VER O PROJETO ONLINE](http://localhost:8501/)

---

🎯 Objetivo do Projeto
Como analista de dados em formação, desenvolvi este projeto para simular o dia a dia de uma empresa. O objetivo foi criar um sistema completo: desde a *criação dos dados* até a *visualização final* para tomada de decisão.

Eu queria responder perguntas como:
* "Qual vendedor está performando melhor?"
* "Como as vendas desse ano se comparam com o ano passado?"

⚙️ Como o projeto foi construído (Passo a Passo)

O projeto não é apenas um gráfico, ele segue um fluxo lógico de dados:

*1. Geração e Tratamento de Dados (gerar_dados.py)*
* Usei *Python* (bibliotecas pandas, numpy e datetime) para criar uma base de dados fictícia, simulando vendas, datas e vendedores.
* Isso permitiu trabalhar com dados "sujos" e tratá-los antes da análise.

*2. Banco de Dados SQL (loja_vendas.db)*
* Armazenei tudo em um banco de dados *SQLite3*.
* Isso simula um ambiente real onde os dados não ficam em planilhas soltas, mas sim estruturados em tabelas (SELECT * FROM sales).

*3. Análise Exploratória (analise_vendas.py)*
* Antes de criar o visual, fiz análises prévias usando *Pandas* e *Matplotlib* para entender o comportamento dos números e validar se as métricas faziam sentido.

*4. Dashboard Interativo (dashboard_streamlit.py)*
* O resultado final é este painel feito com *Streamlit*.
* Ele conecta no banco SQL, lê os dados em tempo real e gera gráficos interativos para o usuário final.

 🛠️ Tecnologias Utilizadas
* *Linguagem:* Python
* *Banco de Dados:* SQL (SQLite)
* *Análise:* Pandas & Numpy
* *Visualização:* Streamlit & Matplotlib


 👩‍💻 Autora & Contato
Este projeto faz parte do meu portfólio de Análise de Dados. Estou disponível para oportunidades na área.

