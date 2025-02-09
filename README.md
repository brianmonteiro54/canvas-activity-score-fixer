# canvas-activity-score-fixer
Este repositório contém uma solução desenvolvida para professores do Canvas que precisam corrigir a pontuação dos alunos, aplicando proporcionalidade e ajustando os resultados de acordo com as atividades não realizadas. A solução utiliza Python e pandas para processar os dados exportados do Canvas em formato CSV, corrigindo os valores das notas dos alunos para refletir corretamente seu desempenho. Com isso, é possível garantir que a nota do aluno seja calculada de forma justa, considerando apenas as atividades completadas. Além disso, essa ferramenta foi projetada para ser utilizada no contexto das aulas de AWS Restart, possibilitando a análise de dados de desempenho na plataforma AWS.

## Contexto

Quando as notas de atividades são exportadas do Canvas, as pontuações de alunos que ainda não realizaram as atividades podem aparecer como 100%, o que distorce a avaliação real de seu desempenho. Com essa ferramenta, é possível corrigir essas pontuações e ajustar as notas de forma proporcional, garantindo que o desempenho refletido seja o correto.

Este script foi desenvolvido para ser utilizado por professores da plataforma **AWS Restart**, e pode ser integrado com a plataforma Canvas para monitorar o progresso dos alunos de maneira precisa.

## Como Funciona

1. O script recebe um arquivo CSV exportado do Canvas contendo os dados de desempenho dos alunos.
2. O processo de correção é realizado, aplicando proporcionalidade para atividades não realizadas e ajustando as notas de acordo com os critérios definidos.
3. O arquivo corrigido é gerado e pode ser utilizado para análise ou importação de volta para o sistema de avaliação.

## Como Funciona

**Input:** O script recebe um arquivo CSV exportado do Canvas contendo os dados de desempenho dos alunos.
**Processamento:** O processo de correção aplica proporcionalidade para atividades não realizadas, ajustando as notas conforme os critérios definidos (considerando a nota zero para atividades não realizadas).
**Output:** O arquivo corrigido é gerado e pode ser utilizado para análise ou importação de volta ao sistema de avaliação.

## Visualização dos Resultados

Após o processamento do arquivo CSV, os professores podem visualizar os resultados detalhados no [CSV Viewer Online](https://brianmonteiro54.github.io/csv-viewer-online/kc/). No site, é possível consultar as seguintes informações:

- **Desempenho total do aluno**
- **Resultados das atividades de laboratório (labs)**
- **Análise das competências (KCs)**
- **Envio de e-mails aos alunos** com as atividades pendentes, garantindo que os alunos saibam exatamente o que precisam completar.

Essa funcionalidade ajuda a manter um acompanhamento eficiente do progresso dos alunos e facilita a comunicação direta com eles sobre as pendências nas atividades.

## 📌 Pré-requisitos

Antes de instalar a ferramenta, certifique-se de ter o **Python 3.x** instalado em sua máquina. Você pode verificar se o Python já está instalado com:

```sh
python --version
```

Além disso, você precisará de alguns pacotes para que o script funcione corretamente:

- **pandas**: Usado para manipulação de dados.
- **flask**: Usado para criar a aplicação web que recebe o arquivo CSV.
- **uuid**: Biblioteca padrão do Python (não requer instalação adicional).

## 🚀 Passos para instalação

### 1️⃣ Clone o repositório para sua máquina local:
```sh
git clone https://github.com/seu-usuario/canvas-activity-score-fixer.git
cd canvas-activity-score-fixer
```

### 2️⃣ Crie e ative um ambiente virtual (recomendado para isolar as dependências):

Para **Linux/Mac**:
```sh
python -m venv venv
source venv/bin/activate
```

Para **Windows**:
```sh
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Instale as dependências necessárias:
```sh
pip install -r requirements.txt
```

## 🔥 Rodando o servidor Flask localmente

Para rodar o servidor localmente e fazer o upload do arquivo CSV, execute:
```sh
flask run
```
O servidor será iniciado no endereço **http://127.0.0.1:5000**

## 📤 Enviando um arquivo CSV para correção

Após iniciar o servidor, você pode enviar um arquivo CSV para correção usando `curl`:
```sh
curl -X POST http://127.0.0.1:5000/process-csv \
     -H "Content-Type: multipart/form-data" \
     -F "file=@2025-02-09T0153_Notas-BRSAOxxx.csv" -o corrigido.csv
```

📌 **Explicação:**
- `-X POST`: Define que a requisição será do tipo **POST**.
- `-H "Content-Type: multipart/form-data"`: Indica que estamos enviando um arquivo.
- `-F "file=@seuarquivo.csv"`: Substitua **seuarquivo.csv** pelo nome do arquivo que deseja corrigir.
- `-o corrigido.csv`: O arquivo corrigido será salvo com esse nome.

Agora seu arquivo **corrigido.csv** estará pronto para uso! ✅

