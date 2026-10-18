# AI Shorts Generator

**Gerador automático de vídeos curtos a partir de gameplays, desenvolvido em Python.**

**Status:** Em desenvolvimento — Alpha

**Tecnologias:** Python | OpenCV | FFmpeg | Faster-Whisper | NumPy

---

## Sobre o projeto

O **AI Shorts Generator** é uma aplicação desenvolvida em Python para automatizar o processo de identificação, classificação e edição de momentos interessantes em gravações de gameplay e transmissões ao vivo.

O projeto nasceu com o objetivo de reduzir o trabalho manual necessário para transformar gravações longas em vídeos curtos destinados a plataformas como **YouTube Shorts, TikTok e Instagram Reels**.

O sistema processa os vídeos localmente, combina informações visuais, sonoras e textuais e seleciona os melhores candidatos utilizando um mecanismo de pontuação de 0 a 100.

A aplicação também realiza a montagem dos cortes, a geração de legendas e a exportação automática dos arquivos.

**O projeto está em desenvolvimento contínuo.** A versão atual utiliza análise heurística e transcrição local. A integração de modelos multimodais para compreensão contextual da gameplay está planejada para versões futuras.

## Funcionalidades

### Implementadas

- **Análise audiovisual:** processamento da gravação para identificar alterações visuais, movimentação, características sonoras e eventos relevantes.
- **Transcrição local:** reconhecimento de fala utilizando Faster-Whisper, sem necessidade de enviar o áudio para APIs externas.
- **Ranking de momentos:** classificação dos candidatos com pontuações de 0 a 100.
- **Seleção automática:** escolha de até quatro momentos distintos, evitando sobreposições.
- **Geração de Shorts:** criação de vídeos verticais em 1080×1920, formato MP4.
- **Legendas sincronizadas:** utilização da transcrição para adicionar legendas aos cortes.
- **Exportação automática:** salvamento dos arquivos em um diretório configurado pelo usuário.
- **Retomada de processamento:** reaproveitamento de resultados intermediários para evitar repetir etapas já concluídas.
- **Verificação de integridade:** validação dos arquivos exportados e controle de duplicações.

### Em desenvolvimento

- Integração com modelos multimodais locais, como Qwen3-VL.
- Reconhecimento contextual de batalhas, chefes, vitórias e acontecimentos marcantes.
- Identificação aprimorada de humor, reações e momentos emocionantes.
- Ranking híbrido combinando heurísticas e interpretação semântica.
- Melhorias de desempenho e aproveitamento de aceleração por GPU.
- Refinamento automático da seleção e da qualidade editorial dos cortes.

## Tecnologias utilizadas

| Tecnologia     | Aplicação                                   |
| -------------- | ------------------------------------------- |
| Python         | Linguagem principal do projeto              |
| OpenCV         | Análise visual de frames                    |
| Faster-Whisper | Transcrição de áudio local                  |
| FFmpeg         | Processamento e renderização de vídeos      |
| NumPy          | Operações numéricas e análise de sinais     |
| CTranslate2    | Execução otimizada do modelo de transcrição |
| Git e GitHub   | Versionamento e documentação                |

O sistema foi desenvolvido para Windows e testado em ambiente com Python 3.14.7 de 64 bits.

A compatibilidade com outros sistemas operacionais e versões do Python ainda não foi completamente validada.

## Arquitetura do sistema

O processamento é dividido em etapas independentes, facilitando a manutenção e a evolução do projeto.

**1. Entrada do vídeo**

O usuário informa o caminho da gravação e o diretório de destino dos arquivos gerados.

**2. Análise audiovisual**

O sistema percorre a gravação, coleta indicadores visuais e sonoros e realiza a transcrição das falas.

**3. Identificação dos candidatos**

São identificados intervalos potencialmente interessantes com base nos indicadores disponíveis.

**4. Classificação e ranking**

Os candidatos recebem pontuações conforme os critérios definidos pelo sistema.

**5. Renderização**

Os trechos selecionados são convertidos para vídeos verticais, com áudio original e legendas.

**6. Verificação e exportação**

Os arquivos são verificados antes de serem copiados ao diretório de saída.

## Sistema de ranking

Os momentos identificados são avaliados de acordo com seis critérios:

| Critério                                    | Pontuação máxima |
| ------------------------------------------- | ---------------: |
| Impacto visual e acontecimentos da gameplay |               25 |
| Falas e reações                             |               25 |
| Potencial de entretenimento                 |               20 |
| Contexto e narrativa                        |               15 |
| Qualidade audiovisual                       |               10 |
| Originalidade                               |                5 |
| **Total**                                   |          **100** |

A versão atual estima essas pontuações utilizando características visuais, indicadores sonoros e palavras identificadas durante a transcrição.

**Importante:** as pontuações são estimativas heurísticas. O sistema ainda não compreende semanticamente todos os acontecimentos da gameplay e não prevê visualizações ou viralização.

A evolução planejada é combinar esses indicadores com modelos de inteligência artificial capazes de interpretar imagens e contexto textual.

## Estrutura do projeto

Principais arquivos e diretórios:

- `main.py` — Interface de comandos da aplicação.
- `aishorts/scan.py` — Análise audiovisual e transcrição.
- `aishorts/ranking.py` — Classificação e seleção de momentos.
- `aishorts/render.py` — Renderização e montagem dos Shorts.
- `aishorts/export.py` — Exportação e verificação dos arquivos.
- `aishorts/media.py` — Funções de processamento multimídia.
- `aishorts/pipeline.py` — Orquestração das etapas.
- `aishorts/config.py` — Gerenciamento de configurações.
- `tests/` — Testes automatizados e testes de mídia.
- `docs/` — Documentação técnica complementar.
- `requirements.txt` — Dependências Python.
- `config.example.json` — Exemplo de configuração.
- `package_project.py` — Preparação do pacote de distribuição.

## Instalação

### Requisitos

- Windows.
- Python 3.14.7 (ambiente validado).
- Git (opcional, para desenvolvimento).
- Espaço livre para arquivos temporários, modelos e vídeos exportados.

O FFmpeg é disponibilizado pela dependência `imageio-ffmpeg`.

### 1. Clonar o repositório

Após a publicação no GitHub, utilize o endereço do repositório:

`git clone URL_DO_REPOSITORIO`

Acesse a pasta:

`cd AI-Shorts-Generator`

### 2. Criar o ambiente virtual

No terminal PowerShell:

`python -m venv .venv`

### 3. Instalar as dependências

`.\.venv\Scripts\python.exe -m pip install -r requirements.txt`

### 4. Verificar o ambiente

`.\.venv\Scripts\python.exe main.py doctor`

Esse comando permite verificar a disponibilidade das principais dependências.

## Configuração

Os caminhos locais e parâmetros de execução são definidos em `config.local.json`.

Esse arquivo contém configurações específicas do usuário e não deve ser enviado ao GitHub.

Para configurar a gravação e o diretório de saída:

`.\.venv\Scripts\python.exe main.py init --input "C:\Videos\live.mp4" --output "C:\Videos\Shorts"`

Substitua os caminhos de exemplo pelos diretórios do seu computador.

### Modelo de transcrição

O projeto utiliza um modelo Faster-Whisper executado localmente.

Para baixar o modelo configurado:

`.\.venv\Scripts\python.exe main.py prepare-model --allow-download`

O download deve ser autorizado explicitamente e é realizado apenas quando necessário.

Também é possível utilizar um modelo existente:

`.\.venv\Scripts\python.exe main.py init --model-path "C:\Modelos\whisper-small"`

O download do modelo requer internet, mas a análise das gravações pode funcionar localmente após a configuração.

## Execução

Para inspecionar as configurações:

`.\.venv\Scripts\python.exe main.py inspect`

Para executar o processamento completo:

`.\.venv\Scripts\python.exe main.py run`

O programa realizará a análise audiovisual, a classificação dos candidatos, a seleção dos melhores momentos, a renderização e a exportação dos vídeos.

Também é possível executar as etapas individualmente:

| Comando          | Função                        |
| ---------------- | ----------------------------- |
| `main.py scan`   | Realiza a análise audiovisual |
| `main.py rank`   | Classifica os candidatos      |
| `main.py render` | Gera e verifica os MP4        |
| `main.py verify` | Verifica os vídeos produzidos |
| `main.py export` | Exporta os arquivos           |

Utilize esses comandos com o interpretador Python do ambiente virtual.

## Formato dos vídeos gerados

Os Shorts são produzidos com as seguintes características:

| Propriedade          | Configuração                    |
| -------------------- | ------------------------------- |
| Formato              | MP4                             |
| Resolução            | 1080×1920                       |
| Proporção            | 9:16                            |
| Codec de vídeo       | H.264                           |
| Codec de áudio       | AAC                             |
| Duração preferencial | 30 a 60 segundos                |
| Quantidade           | Até quatro cortes por execução  |
| Legendas             | Geradas a partir da transcrição |

O sistema utiliza a imagem da gameplay centralizada sobre um fundo desfocado para adaptar o conteúdo horizontal ao formato vertical.

## Testes e validação

O projeto inclui testes automatizados para verificar componentes essenciais da aplicação.

Para executar os testes:

`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`

Testes adicionais:

`.\.venv\Scripts\python.exe tests\smoke_media.py`

`.\.venv\Scripts\python.exe tests\smoke_pipeline.py`

Durante a preparação da versão independente, foram relatados seis testes automatizados aprovados, além de verificações com mídia sintética.

Esses resultados não representam validação completa de todas as situações possíveis, especialmente gravações longas, diferentes formatos de mídia e qualidade editorial dos cortes.

Mais informações estão disponíveis em `docs/TESTES.md`.

## Privacidade e processamento local

O AI Shorts Generator foi projetado para executar o processamento de vídeos localmente.

A versão atual:

- Não exige login no ChatGPT Work ou Codex.
- Não utiliza APIs pagas para analisar as gravações.
- Não envia automaticamente vídeos pessoais para serviços externos.
- Permite configurar os diretórios de entrada e saída.
- Mantém arquivos temporários e resultados de análise no armazenamento local.

Os arquivos pessoais, modelos baixados, configurações privadas e intermediários de processamento não devem ser incluídos no repositório público.

## Limitações conhecidas

Esta é uma versão Alpha.

As principais limitações são:

- O ranking atual utiliza indicadores heurísticos e ainda não possui compreensão semântica completa.
- A amostragem visual pode deixar de identificar acontecimentos rápidos entre os frames analisados.
- O sistema não reconhece automaticamente todos os tipos de chefes, piadas ou reações.
- A qualidade editorial pode ser inferior à seleção realizada anteriormente por um agente multimodal.
- O desempenho depende da CPU, GPU, memória e duração da gravação.
- O enquadramento vertical ainda não possui rastreamento inteligente de personagens.

Essas limitações fazem parte do planejamento de evolução do projeto.

Consulte `docs/LIMITACOES.md` para informações adicionais.

## Roadmap

- [x] Implementação do pipeline Python independente.
- [x] Transcrição de áudio local.
- [x] Sistema de ranking heurístico.
- [x] Renderização de Shorts verticais.
- [x] Exportação automática de vídeos.
- [x] Retomada de etapas de processamento.
- [x] Testes automatizados iniciais.
- [ ] Integração com modelo multimodal local.
- [ ] Ranking contextual com interpretação de acontecimentos.
- [ ] Identificação aprimorada de reações e humor.
- [ ] Otimizações de desempenho para gravações longas.
- [ ] Melhorias no enquadramento automático.
- [ ] Validação ampliada com gameplays reais.

## Objetivo do desenvolvimento

O AI Shorts Generator também é um projeto de estudo e portfólio, com foco no desenvolvimento de habilidades relacionadas a:

- Programação Python e organização de software.
- Automação de tarefas.
- Processamento de áudio e vídeo.
- Inteligência artificial e transcrição.
- Análise de dados e classificação.
- Testes, documentação e versionamento de código.

O projeto continuará recebendo melhorias conforme novas funcionalidades forem implementadas e validadas.

---

**AI Shorts Generator — Projeto em desenvolvimento.**

*Automatizando a transformação de gameplays em conteúdo para vídeos curtos.*
