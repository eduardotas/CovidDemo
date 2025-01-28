# Projeto de Extração e Análise de Dados do Covid-19

Este é um projeto simples em Python para extrair dados do Covid-19 a partir do site do Ministério da Saúde e armazená-los em um banco de dados PostgreSQL no AWS RDS. Além disso, o projeto inclui análises para fornecer informações relevantes sobre os números da Covid-19.

## Demonstração

Você pode assistir a uma demonstração do projeto neste [vídeo](<link>).

## Estrutura de Pastas

O projeto possui a seguinte estrutura de pastas:

- `1_script`: Contém os scripts Python para a extração e inserção dos dados no banco de dados.
  - `dowload_covid_file.py`: Realiza o download dos dados em formato zip do site https://covid.saude.gov.br/ e extrai os arquivos para a pasta `data`. Utiliza a biblioteca Selenium para acessar o site e realizar o download dos arquivos.
  - `extract_to_db.py`: Lê os arquivos da pasta `data` e insere os dados no banco de dados. Utiliza as bibliotecas Pandas e Sqlalchemy para extrair os dados dos arquivos e inseri-los no banco.
- `data`: Pasta onde são armazenados os arquivos baixados do Covid-19.
- `driver`: Contém o `chromedriver.exe`, que é utilizado pelo script `dowload_covid_file.py`.
- `querys`: Contém arquivos SQL com as queries para criação da tabela que receberá os dados e análises para fornecer informações relevantes sobre a Covid-19.
  - `create_table.sql`: Query SQL com a estrutura da tabela que receberá os dados.
  - `indicadores`: Arquivos SQL com as análises para obter informações relevantes sobre a Covid-19.

## Dificuldades
Durante o desenvolvimento do projeto, foram enfrentadas algumas dificuldades relacionadas à compreensão dos cálculos utilizados para obter os indicadores da Covid-19. A documentação fornecida no site do Ministério da Saúde (https://covid.saude.gov.br/) na aba "sobre" não foi esclarecedora o suficiente quanto ao método de cálculo empregado.

Para superar esse obstáculo, foi necessário buscar informações adicionais em fontes externas. Um dos recursos que ajudou foi o artigo disponível em https://unasus2.moodle.ufsc.br/pluginfile.php/33454/mod_resource/content/1/un1/top5_1.html#:~:text=A%20incid%C3%AAncia%20diz%20respeito%20%C3%A0,casos%20(PEREIRA%2C%201995), que descreve de forma mais detalhada o método utilizado para calcular os indicadores, como a incidência e a mortalidade.