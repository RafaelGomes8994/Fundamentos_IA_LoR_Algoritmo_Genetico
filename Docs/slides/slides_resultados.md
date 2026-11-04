---
title: "Otimização de Builds no Legends of Runeterra via Algoritmo Genético"
subtitle: "Extensão do Cenário PvP (Riot Lock) para o Modo PvE (O Caminho dos Campeões)"
author: "Rafael Gomes Oliveira Santos — Fundamentos de Inteligência Artificial (UFS)"
date: "2025"
---

# Otimização de Builds no Legends of Runeterra via Algoritmo Genético

* **Disciplina:** Fundamentos de Inteligência Artificial (COMP/UFS)
* **Autor:** Rafael Gomes Oliveira Santos
* **Artigo Base:** *Developing Competitive Strategies for Legends of Runeterra using Genetic Algorithm* (Balbinot et al., XXIII SBGames, 2024)
* **Objetivo Cumprido:** Adaptação da meta-heurística evolutiva do formato competitivo PvP (*Riot Lock*) para otimização combinatória de **3 Relíquias** no modo PvE (*O Caminho dos Campeões*)

![Carta Oficial PT-BR: Aurelion Sol](https://dd.b.pvp.net/latest/set3/pt_br/img/cards/03MT087.png){width=28%}

::: notes
Olá professor, meu nome é Rafael. Neste trabalho prático de Fundamentos de IA, apresento a extensão do artigo de Balbinot et al. (SBGames 2024), adaptando o Algoritmo Genético do modo PvP para otimizar builds de 3 Relíquias no modo PvE O Caminho dos Campeões do Legends of Runeterra.
:::

---

# Do Problema Original (PvP) ao Objetivo Proposto (PvE)

* **Artigo Base — Cenário PvP (*Riot Lock*):**
  * Otimizava *lineups* de **3 baralhos** para torneios via matriz de *winrate* $a_{i,j}$
  * Avaliava três cenários táticos: Vitória Geral ($E_1$), Banimento Fixo ($E_2$) e Contra-Deck Alvo ($E_3$)
* **Trabalho Desenvolvido — Cenário PvE (*O Caminho dos Campeões*):**
  * **Arquitetura Evolutiva Preservada:** Seleção por Torneio ($k=3$), Crossover Posicional em 2 Passos com Inversão de Pais, Reparo Determinístico e Elitismo ($E=2$)
  * **Base de Dados PvE Estruturada:** **60 Campeões**, **34 Relíquias** (Comuns, Raras e Épicas), **8 Combos** e **8 Chefes Mundiais**
  * **Estratégias PvE Equivalentes:** Build Geral ($E_1$), Restrição de Inventário ($E_2$) e Contra-Chefe Específico ($E_3$)

![Carta Oficial PT-BR: Jinx Nível 1](https://dd.b.pvp.net/latest/set1/pt_br/img/cards/01PZ040.png){width=28%}

::: notes
Na Etapa 1, identificamos uma limitação do artigo original: ele focava apenas em torneios PvP. Cumprimos 100% do objetivo proposto mantendo o motor evolutivo intacto e construindo uma base de dados PvE com 60 campeões e 34 relíquias, mapeando as estratégias E1, E2 e E3 para o contexto PvE.
:::

---

# Modelagem Cromossômica e Operadores Evolutivos

* **1. Representação (Indivíduo):** Vetor de 3 Relíquias $B = (r_1, r_2, r_3)$ equipadas simultaneamente no campeão-alvo
* **2. Espaço de Busca Factível ($\Omega$):** Respeita a restrição de *stackability* ($s(r) \in \{0,1\}$), totalizando **6.188 combinações válidas** de 3 relíquias
* **3. Seleção e Elitismo:** Seleção por Torneio ($k=3$) combinada à preservação direta dos **2 melhores indivíduos** por geração ($E=2$)
* **4. Crossover em 2 Passos e Mutação:** Cruzamento posicional fiel à Figura 4 de Balbinot et al. (2024), com reparo determinístico de duplicatas ilegais e mutação pontual guiada por $TM$

![Carta Oficial PT-BR: Yasuo Nível 1](https://dd.b.pvp.net/latest/set1/pt_br/img/cards/01IO015.png){width=28%}

::: notes
Cada indivíduo da população é uma tupla de 3 relíquias. Considerando relíquias únicas e acumuláveis, o espaço de busca possui 6.188 builds válidas. Mantivemos o torneio de tamanho 3, elitismo de 2 indivíduos e o cruzamento em 2 passos com inversão da ordem dos pais e reparo determinístico.
:::

---

# A Nova Função de Fitness Multidimensional ($f(B)$)

$$f(B) = 0{,}15 \cdot f_{\text{base}}(B) + 0{,}40 \cdot f_{\text{champ}}(B, c) + 0{,}15 \cdot f_{\text{star}}(B, c, \star) + 0{,}15 \cdot f_{\text{combo}}(B) + 0{,}15 \cdot f_{\text{boss}}(B, \text{boss})$$

* **1. Poder Base ($15\%$ — $f_{\text{base}}$):** Pontuação intrínseca das 3 relíquias segundo raridade e impacto geral
* **2. Sinergia Campeão–Relíquia ($40\%$ — $f_{\text{champ}}$):** Afinidade mecânica extraída de *tier lists* da comunidade (peso principal)
* **3. Poder Estelar ($15\%$ — $f_{\text{star}}$):** Escalonamento do potencial conforme o nível de estrelas do campeão ($1\star$ a $6\star$)
* **4. Combos entre Relíquias ($15\%$ — $f_{\text{combo}}$):** Bônus para pares sinérgicos na mesma build (ex.: *Payload* + *Luden's Tempest*)
* **5. Efetividade Contra-Chefe ($15\%$ — $f_{\text{boss}}$):** Na estratégia $E_3$, bonifica *counters* ($+3{,}0$) e penaliza mecânicas punidas pelo chefe ($-3{,}5$)

![Carta Oficial PT-BR: Aurelion Sol Nível 2](https://dd.b.pvp.net/latest/set3/pt_br/img/cards/03MT087T1.png){width=25%}

::: notes
Como no PvE não há matriz de winrate entre baralhos, modelamos uma função de avaliação multidimensional com 5 componentes ponderados: 15% poder base, 40% sinergia direta com o campeão, 15% escalonamento com Poder Estelar, 15% bônus de combos entre relíquias e 15% adaptação contra mutadores de chefes.
:::

---

# Metodologia Experimental (Modelo GQM)

* **Questões de Pesquisa (Basili & Weiss, 1984):**
  * **RQ1 (Efetividade):** Quão próximo do ótimo global exato ($f^*$) o Algoritmo Genético converge em cada configuração?
  * **RQ2 (Eficiência):** Qual é o custo computacional médio em tempo de execução (em milissegundos)?
  * **RQ3 (Representatividade):** As builds geradas coincidem com o consenso *Best-in-Slot* (BiS) dos especialistas?
* **3 Configurações do Artigo Base (30 Repetições Independentes Cada):**
  * `conf1`: $P = 10$, $TM = 0{,}3$, $G = 10$ (baixa exploração — ~100 avaliações)
  * `conf2`: $P = 20$, $TM = 0{,}5$, $G = 50$ (exploração intermediária — ~1.000 avaliações)
  * `conf3`: $P = 30$, $TM = 0{,}7$, $G = 100$ (alta exploração — ~3.000 avaliações)
* **Linha de Base Exata (*Ground Truth*):** Busca Exaustiva nas **6.188 combinações válidas** para aferição de precisão real

![Carta Oficial PT-BR: Jinx Nível 2](https://dd.b.pvp.net/latest/set1/pt_br/img/cards/01PZ040T1.png){width=28%}

::: notes
Seguindo a metodologia GQM de Basili e Weiss (1984) usada no artigo base, definimos três questões de pesquisa: Efetividade (RQ1), Eficiência (RQ2) e Representatividade (RQ3). Executamos 30 repetições independentes para conf1, conf2 e conf3 e comparamos contra a Busca Exaustiva nas 6.188 builds válidas.
:::

---

# Resultados Quantitativos — Efetividade (RQ1) e Eficiência (RQ2)

| Campeão (Ótimo Exato $f^*$) | `conf1` ($P=10, G=10$) | `conf2` ($P=20, G=50$) | `conf3` ($P=30, G=100$) |
| :--- | :---: | :---: | :---: |
| **Jinx** ($18{,}07$) | $14{,}94$ ($82{,}7\%$) — $1{,}01\text{ ms}$ | $18{,}07$ ($100{,}0\%$) — $12{,}28\text{ ms}$ | **$18{,}07$ ($100{,}0\%$) — $42{,}84\text{ ms}$** |
| **Yasuo** ($17{,}77$) | $13{,}16$ ($74{,}0\%$) — $1{,}09\text{ ms}$ | $17{,}77$ ($100{,}0\%$) — $12{,}81\text{ ms}$ | **$17{,}77$ ($100{,}0\%$) — $43{,}96\text{ ms}$** |
| **Aurelion Sol** ($19{,}57$) | $14{,}67$ ($75{,}0\%$) — $1{,}31\text{ ms}$ | $19{,}57$ ($100{,}0\%$) — $13{,}22\text{ ms}$ | **$19{,}57$ ($100{,}0\%$) — $47{,}00\text{ ms}$** |
| **Swain** ($18{,}73$) | $14{,}37$ ($76{,}7\%$) — $1{,}15\text{ ms}$ | $18{,}72$ ($99{,}9\%$) — $14{,}78\text{ ms}$ | **$18{,}73$ ($100{,}0\%$) — $48{,}14\text{ ms}$** |

* **Convergência Prematura na `conf1`:** Retém entre $74{,}0\%$ e $82{,}7\%$ do ótimo global devido ao baixo número de gerações ($G=10$)
* **Convergência Exata na `conf3`:** Atinge **$100{,}0\%$ do ótimo global** com desvio padrão $\sigma = 0{,}00$ em `~45 ms` (4x mais rápido que os `190 ms` do artigo base)

![Carta Oficial PT-BR: Yasuo Nível 2](https://dd.b.pvp.net/latest/set1/pt_br/img/cards/01IO015T1.png){width=25%}

::: notes
Nos resultados quantitativos, a conf1 sofre convergência prematura, atingindo entre 74% e 82,7% do ótimo exato. Já a conf2 supera 99,9% em ~13 ms, e a conf3 atinge 100% do ótimo global em todas as 30 execuções para todos os campeões em cerca de 45 milissegundos, muito abaixo dos 190 ms do artigo base.
:::

---

# Resultados Qualitativos — Representatividade (RQ3) e Estratégias

* **Estratégia $E_1$ (Jinx — Tier S+):** `The Loose Cannon's Payload` + `Luden's Tempest` + `The Scourge's Stash` (**$100\%$ idêntica ao *Best-in-Slot* da comunidade**)
* **Estratégia $E_1$ (Yasuo — Tier S+):** `Tempest Blade` + `Everfrost` + `Yasuo's Windblade` (controle total de mesa ao subir de nível)
* **Descoberta Emergente (Swain — Tier S):** `Gatebreaker` (2x) + `Swain's Ravenous Flock` (exploração autônoma de relíquia *stackable*)
* **Estratégia $E_2$ (Restrição Fixa):** Sem `Payload` na Jinx, o AG reconfigura a build para `The Scourge's Stash` + `Luden's Tempest` (2x) ($f = 16{,}88$)
* **Estratégia $E_3$ (Contra-Chefe Lissandra $5\star$):** Penaliza *spam* de cartas baratas e prioriza *SpellShield* (`Banshee's Veil`) e atributos (`Chosen by the Stars`)

![Carta Oficial PT-BR: Lissandra Nível 1](https://dd.b.pvp.net/latest/set4/pt_br/img/cards/04FR005.png){width=28%}

::: notes
Na avaliação qualitativa (RQ3), o AG reproduziu com exatidão as builds Best-in-Slot de Jinx e Yasuo na Estratégia E1 e descobriu autonomamente o uso duplo de Gatebreaker no Swain. Na Estratégia E2 contornou a falta da relíquia principal da Jinx, e na Estratégia E3 adaptou a build contra o mutador da chefe Lissandra.
:::

---

# Conclusão e Referências Bibliográficas

* **Objetivo Integralmente Cumprido:** Adaptação completa do Algoritmo Genético de Balbinot et al. (2024) para os **60 campeões** do modo PvE *O Caminho dos Campeões*
* **Precisão e Desempenho:** `conf3` garante **$100{,}0\%$ de convergência** para o ótimo global em **menos de $50\text{ ms}$**, validada por **31 testes unitários automatizados**
* **Referências Bibliográficas Verificadas:**
  * **BALBINOT, R. A.; COSTA, L. M.; SOUZA, A. C. C.; SOUZA, F. C. M.** *Developing Competitive Strategies for Legends of Runeterra using Genetic Algorithm*. In: **Proceedings of the XXIII Brazilian Symposium on Games and Digital Entertainment (SBGames 2024)**, Manaus, 2024.
  * **BASILI, V. R.; WEISS, D. M.** *A methodology for collecting valid software engineering data*. **IEEE Transactions on Software Engineering**, v. 10, n. 6, p. 728–738, 1984.
  * **KRAMER, O.** *Genetic Algorithm Essentials*. Cham: **Springer**, 2017. (Studies in Computational Intelligence, v. 679).
  * **RIOT GAMES.** *Legends of Runeterra*, 2024.

![Carta Oficial PT-BR: Swain Nível 1](https://dd.b.pvp.net/latest/set2/pt_br/img/cards/02NX007.png){width=25%}

::: notes
Concluímos que o objetivo proposto foi integralmente cumprido para os 60 campeões do jogo, atingindo 100% de precisão na conf3 em menos de 50 ms e mantendo total fidelidade às referências bibliográficas originais. Muito obrigado!
:::

---

# Repositório Completo no GitHub (Código-Fonte e Testes)

* **Link Direto:** [github.com/RafaelGomes8994/Fundamentos_IA_LoR_Algoritmo_Genetico](https://github.com/RafaelGomes8994/Fundamentos_IA_LoR_Algoritmo_Genetico)
* **Destaques do Repositório:**
  * Motor evolutivo completo em Python padrão (Zero dependências externas obrigatórias)
  * Suíte com **31 testes unitários automatizados** (`python -m unittest discover tests -v`)
  * Base de dados curada com **60 Campeões**, **34 Relíquias** e **8 Chefes Mundiais**
  * Scripts prontos para benchmark GQM e geração de builds para todos os campeões

![QR Code do Repositório GitHub](qrcode_github.png){width=35%}

::: notes
Para finalizar, todo o projeto é open-source e está disponível publicamente no GitHub pelo QR Code em tela. O repositório conta com 31 testes unitários automatizados cobrindo todas as regras de negócio e os scripts de reprodução direta dos experimentos. Muito obrigado pela atenção e fico aberto às perguntas!
:::

