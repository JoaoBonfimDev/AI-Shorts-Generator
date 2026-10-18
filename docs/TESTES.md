# Validação realizada

Ambiente: Windows local, Python 3.14.7, dependências existentes reutilizadas sem reinstalação. `pip check`: sem requisitos quebrados. Código compilado e CLI `doctor` executada fora de qualquer ferramenta exclusiva do Work.

## Resultados

- **6 testes automatizados aprovados:** invalidação do cache por fonte/configuração, trava de execução, ausência de candidatos em silêncio/imagem estática, seleção elegível perto do final da gravação e limites das notas, mapeamento/filtro de legendas, cópia sem sobrescrita com hashes e rejeição de conjunto incompleto.
- **Mídia sintética real de quatro segundos:** FFmpeg criou vídeo/áudio, scanner visual executou, Whisper small local carregou e processou o áudio, renderer CPU gerou um MP4 1080×1920 com ASS, decodificação integral passou e quatro cópias de teste foram verificadas por SHA-256. Três cópias adicionais reutilizam o mesmo MP4 sintético; não são quatro análises independentes.
- **Fluxo integrado com vídeo sintético de 32 segundos e transcrição de teste explícita:** ranking, renderização de 30 segundos, verificação e exportação passaram. Uma segunda execução de `export` não criou cópia duplicada. O caso de menos de quatro candidatos foi informado corretamente.
- **Sem reanálise de live particular, sem download de modelo e sem chamada paga.** O modelo já presente foi usado somente no teste sintético.

Durante o desenvolvimento foram corrigidos problemas nos fixtures dos testes (diretório temporário incompatível com o sandbox e campos obrigatórios ausentes). Os resultados acima são da execução final aprovada.

## Limites da validação

Não foi repetida uma instalação limpa pela internet. Os testes usaram o Python/venv existente como fornecedor das bibliotecas; o projeto não fixa esse caminho e não importa código da versão original. O ZIP não inclui esse ambiente nem o modelo. Após extração, instalar requirements ou selecionar um ambiente com essas bibliotecas.

Não foram medidos precisão semântica, qualidade das transcrições reais, retenção de público, custo energético nem desempenho em duas horas do fluxo migrado. O teste de som sintético confirma carregamento/execução do ASR, não sua capacidade de entender fala humana. A nova versão precisa de um ensaio controlado com uma gravação real para avaliação editorial.

O encoder automático optou por CPU nesta sessão. NVENC é suportado pelo código, mas não foi validado nesta entrega. Exportações de teste foram feitas em pastas temporárias locais, não no diretório de vídeos particulares do usuário.
