# Projeto Integrador – Desenvolvimento Low Code em Ciência de Dados

 > **[Clique aqui para acessar o Dashboard Interativo](https://projeto-integrador-autoescola-gcvg7ejjyrv4murd2ijgsd.streamlit.app/)**

## Repositório

https://github.com/ads-senac-grupo66/projeto-integrador-autoescola

## Tema

Plataforma de Instrutores de Direção

## Objetivo

Desenvolver um dashboard analítico para monitorar indicadores de desempenho, volume de aulas, demanda por localidade e satisfação dos alunos de uma plataforma fictícia de instrutores de direção.

## Tecnologias Utilizadas

- Python
- Streamlit
- Pandas
- Plotly
- Microsoft Excel

## Base de Dados

Foi criada uma base de dados sintética contendo:

- 300 registros
- 50 alunos
- 8 instrutores
- 8 cidades
- Avaliações de satisfação em escala de 1 a 5

## Indicadores

- Total de Aulas Realizadas
- Total de Alunos Cadastrados
- Média Geral de Satisfação
- Cidade com Maior Demanda

## Dashboard

O dashboard desenvolvido apresenta indicadores e visualizações para apoiar a análise operacional da plataforma fictícia de instrutores de direção, permitindo identificar padrões de demanda, desempenho dos instrutores e níveis de satisfação dos alunos.

## Visualizações

- Instrutores com Maior Volume de Aulas
- Evolução Mensal das Aulas
- Demanda por Cidade
- Desempenho dos Instrutores
- Satisfação dos Alunos

## Principais Resultados

- Campinas apresentou o maior volume de aulas realizadas.
- Luciana Carvalho Lima obteve a maior média de avaliação entre os instrutores.
- A média geral de satisfação dos alunos foi de 2,99 em uma escala de 1 a 5.

## Estrutura do Projeto

```text
.
├── app.py
├── Autoescola_Aulas.csv
├── Autoescola.xlsx
├── Projeto Integrador - Dashboard Autoescola.pdf
├── README.md
└── requirements.txt
```

## Como Executar

### Instalar as dependências

```bash
pip install -r requirements.txt
```

### Executar o dashboard

```bash
streamlit run app.py
```

## Autor

Projeto desenvolvido pelo Grupo 66 para a disciplina de Desenvolvimento Low Code em Ciência de Dados.
