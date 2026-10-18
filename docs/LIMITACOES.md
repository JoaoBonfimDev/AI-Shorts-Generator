# Limites reais da versão independente

## O que executa sozinho

- Leitura do vídeo local completo, extração e transcrição local, amostragem de imagem, energia sonora e mudanças visuais.
- Propostas de cortes cobrindo toda a duração, ordenadas por uma fórmula transparente com os limites 25/25/20/15/10/5.
- Até quatro escolhas sem sobreposição temporal, com distância mínima e comparação textual para reduzir repetição.
- Legendas ASS/SRT com timestamps, MP4 vertical, áudio original de uma faixa configurada, verificação integral de decodificação e cópia com SHA-256.
- Checkpoints, cache por fonte/configuração e execução por Python comum, sem ferramentas do Work.

## O que ainda não é equivalente à curadoria anterior

1. **Reconhecimento semântico:** os scripts originais não continham modelo visual de bosses, vitórias, HUD, reações ou humor. O agente fazia esse julgamento. O novo ranking calcula proxies a partir de movimento, brilho, fala e palavras-chave; uma palavra pode vir de um personagem do jogo. Não afirmar que a nota comprova um momento épico.
2. **Narrativa e originalidade:** limites de janela e similaridade textual não comprovam começo/fim de acontecimento nem impedem toda repetição do mesmo evento. Não há detector de carregamento/menu confiável. Imagens escuras e estáticas são despriorizadas, com possíveis falsos negativos.
3. **Separação de vozes:** não há diarização nem isolamento automático de voz do jogador. Áudio misturado pode produzir traduções/hallucinações. O filtro de confiança e idioma reduz, mas não elimina, esses erros. O teste sintético não mede precisão em gameplays reais.
4. **Legendas:** automáticas, parciais quando confiança é baixa. Não traduzem sistematicamente diálogo inglês para português; legendas já presentes no vídeo continuam visíveis. Janelas de ASR podem cortar frases na fronteira. Antes de publicar, conferir pelo ouvido.
5. **Enquadramento:** conserva toda a imagem com fundo desfocado. Não há reenquadramento inteligente, detecção de webcam ou rastreamento de HUD/personagens.
6. **Áudio separado:** `audio_track` pode analisar só o microfone, mas `render_audio_track` deve apontar a uma faixa já mixada para conservar jogo e voz juntos. Mistura automática de múltiplas faixas ainda não foi integrada.
7. **Hardware e instalação:** CPU testada; a sondagem NVENC optou por CPU nesta sessão. Não foi feita instalação limpa da internet nem ensaio de duas horas na versão migrada. As funções originais já haviam processado lives longas, mas isso não substitui validar o novo fluxo em uma live real.

## Como as notas automáticas são calculadas

O código de referência está em `aishorts/ranking.py`. Visual usa diferença entre amostras e termos de acontecimentos; reações usa termos emocionais e proporção de fala; entretenimento combina esses sinais; narrativa usa fala, pontuação e termos de desfecho; qualidade usa brilho e energia; originalidade começa com um valor conservador e a seleção elimina algumas repetições. Todos são **indicadores indiretos**, não avaliação editorial validada. Silêncio e imagem estática sem evidências não geram quatro cortes artificiais.

## Integrações ainda necessárias para aproximar a qualidade anterior

- Avaliador visual/linguístico local que interprete amostras e transcrição dos candidatos e produza evidências verificáveis.
- Ajuste semântico de limites de cenas e separação de fala do criador versus jogo.
- Avaliação com um conjunto de trechos anotados por pessoas, para medir a seleção e não só a integridade dos MP4.

Essas integrações não estão disfarçadas como implementadas. Hoje, o caminho para qualidade editorial é revisar `ranking.json` e importar essa seleção. Isso pode ser feito no VS Code, sem Work e sem API. Não há integração paga configurada.
