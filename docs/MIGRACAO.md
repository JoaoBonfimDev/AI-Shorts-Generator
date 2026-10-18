# Origem e decisões da migração

A versão funcional anterior permaneceu no lugar. A cópia de desenvolvimento foi construída em outra pasta. Não foram copiadas gravações, exportações, credenciais, transcrições nem rankings particulares.

| Componente real anterior | Destino / decisão |
|---|---|
| `shorts.py` | Helpers reais de FFmpeg, inspeção, timestamps e gravação JSON em `media.py`; piloto monolítico substituído pela CLI modular |
| `editorial_scan.py` | Lógica de varredura e checkpoints adaptada em `scan.py`; memória limitada a blocos, faixa configurável, decoder genérico |
| `review_current.py`, `review_live1.py`, `refine_pt_live1.py`, `caption_check_current.py` | Estratégia local de janelas e confiança incorporada ao scanner; intervalos específicos e dados pessoais não transportados |
| `editorial_export.py` | Agrupamento de legendas, estilos ASS, composição, concatenação e parâmetros de qualidade reutilizados em `render.py`; rótulo configurável e encoder CPU alternativo |
| `prepare_editorial_captions.py`, `finalize_live1_captions.py` | Mapeamento temporal incorporado em `pipeline.captions`; correções específicas e manuais não generalizadas como inteligência automática |
| `export_destination.py` | Cópia exclusiva, verificação SHA-256 e proteção contra sobrescrita reutilizadas em `export.py` |
| `verify_current.py`, `verify_ranked_exports.py` | Verificação de streams, duração e decodificação completa em `pipeline.verify` |
| `build_live1.py`, `build_current.py` | Continham escolhas, notas e justificativas editoriais fixas; não eram algoritmos de descoberta. Substituídos por alternativa heurística explícita e importação de ranking revisado |
| `build_ranking_report.py`, `report_current.py`, `finalize_current.py` | Relatórios dependentes de lives específicas substituídos por relatório genérico com os caminhos confirmados |
| Atalhos `.cmd`, configurações e requirements | Novos atalhos portáteis, exemplos sem dados pessoais e inclusão de OpenCV/CT2 já utilizados anteriormente |

As versões iniciais usavam critérios diferentes; esta cópia adota exclusivamente os seis limites mais recentes: 25, 25, 20, 15, 10, 5. Não leva os rankings antigos como se fossem resultados do novo algoritmo.

`original_hashes.json` registra hashes dos scripts principais na origem para verificar que não foram alterados. Nomes e hashes não contêm mídia ou transcrições. A entrega não inclui todo o histórico descartável de uma live, porque esses scripts tinham nomes, falas, intervalos e julgamentos privados embutidos; sua lógica reutilizável foi extraída. Todo o código necessário à versão entregue está presente.
