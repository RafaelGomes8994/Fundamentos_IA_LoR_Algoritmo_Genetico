# Relatório Técnico: Otimização de Builds no Caminho dos Campeões (Legends of Runeterra) Utilizando Algoritmo Genético

**Disciplina:** Fundamentos de Inteligência Artificial  
**Trabalho Prático:** Extensão de Artigo Científico Recente (SBGames 2024)  
**Autor:** Rafael Gomes Oliveira Santos  
**Artigo Base:** *Developing Competitive Strategies for Legends of Runeterra using Genetic Algorithm* (Balbinot et al., SBGames 2024)  

---

## 1. Introdução e Motivação

Os jogos de cartas colecionáveis digitais (*Digital Collectible Card Games* — DCCGs), inspirados no conceito pioneiro de *Magic: The Gathering* (1993), apresentam espaços combinatórios extensos nos quais a sinergia entre cartas e mecânicas determina o desempenho das estratégias. Lançado pela Riot Games em 2020, *Legends of Runeterra* (LoR) destacou-se inicialmente pelo seu formato competitivo de torneios (*Riot Lock*), estudado por Balbinot et al. (2024), e posteriormente redirecionou seu foco principal para o modo *roguelike* PvE **O Caminho dos Campeões** (*The Path of Champions* — PoC).

No modo *Caminho dos Campeões*, o jogador seleciona um Campeão, evolui seus Poderes Estelares (de 1 a 6 estrelas) e equipa até **3 Relíquias** (itens de raridade Comum, Rara ou Épica) para enfrentar aventuras contra o ambiente e chefes mundiais dotados de mutadores severos (como *Teemo, Aurelion Sol, Lissandra* e *Swain*). Considerando um catálogo de 34 relíquias e as regras estritas de acúmulo (*stackability*), existem **6.188 combinações válidas** de relíquias para cada campeão, tornando a escolha manual por tentativa e erro lenta e propensa a configurações subótimas.

Seguindo o objetivo apresentado na primeira etapa da disciplina, este trabalho realiza a **extensão do artigo de Balbinot et al. (2024)**: mantém-se a arquitetura do Algoritmo Genético (AG) original intacta, migra-se a base de dados do cenário PvP para uma base de dados PvE curada pela comunidade e redefine-se a função de avaliação (*fitness*) para capturar a sinergia entre Campeão, Relíquias e Chefes.

---

## 2. Alinhamento com o Artigo Base e com o Objetivo Proposto

No estudo original de Balbinot et al. (2024), o Algoritmo Genético foi projetado para compor *lineups* de 3 arquétipos $(d_1, d_2, d_3)$ segundo três estratégias de geração:
* **$E_1$ (Por taxa de vitória média):** Seleciona três arquétipos fortes considerando o desempenho geral;
* **$E_2$ (Excluindo um banimento fixo):** Desconsidera na avaliação um arquétipo $d_x$ que o jogador pretende banir;
* **$E_3$ (Focada em um arquétipo específico):** Otimiza a composição especificamente para vencer um arquétipo dominante do metagame.

Na presente extensão para o modo PvE (*The Path of Champions*), preservamos integralmente essa estrutura conceitual e algorítmica:

| Conceito no Artigo Base (PvP — SBGames 2024) | Extensão Desenvolvida (PvE — Path of Champions) |
|---|---|
| **Indivíduo (Cromossomo)** | Tripla de 3 Arquétipos $(d_1, d_2, d_3)$ | Tripla de 3 Relíquias equipadas $(r_1, r_2, r_3)$ |
| **Restrição de Viabilidade** | Regra *Riot Lock* (sem repetir campeões ou combinações de regiões) | Regra de *Stackability* (proibido repetir relíquias não acumuláveis ou Épicas) |
| **Crossover e Mutação** | Cruzamento posicional em 2 passos com inversão de pais + mutação pontual (Figura 4 do artigo base) | Mesma estrutura de cruzamento posicional em 2 passos com reparo de viabilidade + mutação pontual |
| **Estratégia $E_1$** | Otimização pelo desempenho médio geral | Otimização da sinergia geral Campeão + Relíquias |
| **Estratégia $E_2$** | Exclusão de um arquétipo fixo ($d_x$) | Exclusão de uma relíquia restrita ou indisponível ($r_x$) |
| **Estratégia $E_3$** | Contra-ataque a um arquétipo alvo | Adaptação da build para neutralizar os mutadores de um Chefe específico ($B_{oss}$) |
| **Base de Dados** | Partidas ranqueadas PvP da API da Riot | Base estruturada PvE com 60 Campeões, 34 Relíquias, 8 Combos e 8 Chefes |

---

## 3. Arquitetura do Algoritmo Genético

1. **Representação do Indivíduo:** Cada solução candidata $B$ é uma tupla de 3 relíquias $B = (r_1, r_2, r_3) \in \mathcal{R}^3$.
2. **Restrição de Acúmulo (*Stackability*):** Uma build é válida se e somente se nenhuma relíquia com atributo `stackable = False` aparece mais de uma vez na tripla. Indivíduos inválidos recebem penalidade $-9999.0$.
3. **Seleção:** Seleção por torneio ($k=3$) entre indivíduos da população atual.
4. **Cruzamento (Crossover — Figura 4 de Balbinot et al., 2024):** Dados dois progenitores $(ap_i, ap_j)$, o operador é executado duas vezes invertendo a ordem dos pais após a primeira passagem, gerando dois descendentes: o primeiro gene provém do primeiro progenitor, o segundo gene do segundo progenitor e o terceiro gene é sorteado com 50% de probabilidade entre ambos, seguido de reparo determinístico caso haja duplicação ilegal.
5. **Mutação:** Aplicada a uma posição aleatória do cromossomo $\{1, 2, 3\}$ respeitando a probabilidade relativa à taxa de mutação $TM$.
6. **Elitismo:** Preservação dos melhores indivíduos entre gerações sucessivas.

---

## 4. Função de Fitness Adaptada para o Modo PvE

Conforme proposto nos slides da primeira apresentação da disciplina, a função de avaliação substitui as taxas de vitória PvP ($TV, TVM, TJ$) pelos vetores de sinergia do modo PvE, avaliando o Campeão $C$, seu nível de Poder Estelar $S \in \{1, \dots, 6\}$ e o Chefe alvo $B_{oss}$:

$$f(B \mid C, S, B_{oss}) = w_1 f_{\text{base}}(B) + w_2 f_{\text{champ}}(B, C) + w_3 f_{\text{star}}(B, C, S) + w_4 f_{\text{combo}}(B) + w_5 f_{\text{boss}}(B, B_{oss})$$

Com pesos normalizados $\mathbf{w} = [0.15, 0.40, 0.15, 0.15, 0.15]$:
1. **Poder Base ($f_{\text{base}}$):** Soma do valor intrínseco de cada relíquia segundo sua raridade e impacto geral.
2. **Sinergia Campeão–Relíquia ($f_{\text{champ}}$):** Mede a afinidade mecânica e temática entre o campeão e cada relíquia, extraída das matrizes de *Best-in-Slot* (Tier Lists da comunidade PvE).
3. **Amplificação por Poder Estelar ($f_{\text{star}}$):** Modela o escalonamento do campeão conforme seu nível de estrelas ($1\star$ a $6\star$).
4. **Sinergia entre Relíquias ($f_{\text{combo}}$):** Bonifica interações diretas entre pares de relíquias equipadas simultaneamente na mesma build (ex.: *The Loose Cannon's Payload* + *Luden's Tempest*; *Tempest Blade* + *Crownguard Inheritance*).
5. **Efetividade vs. Chefe ($f_{\text{boss}}$ — Estratégia $E_3$):** Bonifica relíquias cujas tags mecânicas neutralizam as ameaças do chefe (`counter_tags`, $+3.0$) ou exploram suas vulnerabilidades (`vulnerable_tags`, $+2.0$), e penaliza relíquias punidas pelos mutadores do chefe (`penalized_tags`, $-3.5$).

---

## 5. Estudo Experimental e Resultados (Metodologia GQM)

Seguindo rigorosamente o modelo **GQM (*Goal-Question-Metric*)** de Basili & Weiss (1984) adotado na Seção 5 de Balbinot et al. (2024), avaliamos três Questões de Pesquisa:
* **RQ1 (Efetividade):** Quão próximo do ótimo global o Algoritmo Genético chega nas diferentes configurações de parâmetros?
* **RQ2 (Eficiência):** Qual é o custo computacional médio em tempo de execução (milissegundos)?
* **RQ3 (Representatividade):** As builds geradas pelo AG correspondem às estratégias *Best-in-Slot* utilizadas pela comunidade?

### 5.1. Configurações Experimentais (Tabela 2 do Artigo Base)
Replicamos exatamente as três configurações da Tabela 2 de Balbinot et al. (2024), executando **30 repetições independentes** para cada combinação:
* **`conf1`:** População $P = 10$, Taxa de Mutação $TM = 0.3$, Gerações $G = 10$
* **`conf2`:** População $P = 20$, Taxa de Mutação $TM = 0.5$, Gerações $G = 50$
* **`conf3`:** População $P = 30$, Taxa de Mutação $TM = 0.7$, Gerações $G = 100$

Para obter o valor máximo exato de referência (*Ground Truth*), um módulo de Busca Exaustiva avaliou todas as **6.188 combinações válidas** do espaço de busca.

### 5.2. Resultados de Efetividade (RQ1) e Eficiência (RQ2)

| Campeão | Configuração | $P$ | $TM$ | $G$ | Ótimo Global Exato | Fitness Médio AG | Taxa de Otimalidade | Tempo Médio (ms) |
|---|---|---|---|---|---|---|---|---|
| **Jinx** | `conf1` | 10 | 0.3 | 10 | 18.07 | 14.94 | 82.7% | 1.01 ms |
| **Jinx** | `conf2` | 20 | 0.5 | 50 | 18.07 | 18.07 | **100.0%** | 12.28 ms |
| **Jinx** | `conf3` | 30 | 0.7 | 100 | 18.07 | 18.07 | **100.0%** | 42.84 ms |
| **Yasuo** | `conf1` | 10 | 0.3 | 10 | 17.77 | 13.16 | 74.0% | 1.09 ms |
| **Yasuo** | `conf2` | 20 | 0.5 | 50 | 17.77 | 17.77 | **100.0%** | 12.81 ms |
| **Yasuo** | `conf3` | 30 | 0.7 | 100 | 17.77 | 17.77 | **100.0%** | 43.96 ms |
| **Aurelion Sol** | `conf1` | 10 | 0.3 | 10 | 19.57 | 14.67 | 75.0% | 1.31 ms |
| **Aurelion Sol** | `conf2` | 20 | 0.5 | 50 | 19.57 | 19.57 | **100.0%** | 13.22 ms |
| **Aurelion Sol** | `conf3` | 30 | 0.7 | 100 | 19.57 | 19.57 | **100.0%** | 47.00 ms |
| **Swain** | `conf1` | 10 | 0.3 | 10 | 18.73 | 14.37 | 76.7% | 1.15 ms |
| **Swain** | `conf2` | 20 | 0.5 | 50 | 18.73 | 18.72 | 99.9% | 14.78 ms |
| **Swain** | `conf3` | 30 | 0.7 | 100 | 18.73 | 18.73 | **100.0%** | 48.14 ms |

#### Discussão de RQ1 e RQ2:
* **Convergência (`RQ1`):** Corroborando os achados de Balbinot et al. (2024), a configuração `conf1` ($G=10$) apresenta fragilidade por convergência prematura, atingindo entre 74.0% e 82.7% do ótimo global. Em contrapartida, a partir de $G=50$ (`conf2`), o algoritmo alcança 99.9% a 100.0%, e na configuração **`conf3` ($P=30, TM=0.7, G=100$) atinge 100.0% do ótimo global em todos os campeões testados**.
* **Custo Computacional (`RQ2`):** Na configuração `conf3`, o tempo médio de execução situou-se entre **42.84 ms e 48.14 ms** (e cerca de **13 ms** em `conf2`), mantendo-se bem abaixo dos ~190 ms reportados no artigo base para o cenário PvP.

### 5.3. Análise de Representatividade (RQ3) e Adaptação ($E_1, E_2, E_3$)

1. **Alinhamento com a Comunidade ($E_1$):**
   * **Jinx (Tier S+):** O AG convergiu para `The Loose Cannon's Payload` + `Luden's Tempest` + `The Scourge Stash` (Fitness: $18.07$), reproduzindo exatamente a build *Best-in-Slot* da comunidade.
   * **Yasuo (Tier S+):** O AG convergiu para `Tempest Blade` + `Everfrost` + `Yasuo's Windblade` (Fitness: $17.77$), capturando o combo de atordoamento em massa no momento de subida de nível.
   * **Swain (Tier S):** O AG identificou autonomamente que `Gatebreaker` permite múltiplas cópias (`stackable = True`), gerando `Gatebreaker` + `Gatebreaker` + `Swain's Ravenous Flock` (Fitness: $18.73$).
2. **Restrição / Banimento Fixo ($E_2$):**
   * Ao restringir a relíquia principal de Jinx (`--ban-relic "The Loose Cannon's Payload"`), o AG recompõe automaticamente a estratégia para `Luden's Tempest` + `Luden's Tempest` + `The Scourge Stash`, preservando o potencial de dano direto sem violar as restrições.
3. **Adaptação Contra Chefes ($E_3$):**
   * Quando um campeão enfrenta **Teemo** (1★) ou **Aurelion Sol** (4★), o termo $f_{\text{boss}}$ prioriza relíquias de impacto imediato e dano ao Nexus (`burn`, `strike`, `rally`). Diante de **Lissandra** (5★), que pune severamente o uso repetido de feitiços baratos e sepulta unidades em tumbas de gelo, o fitness penaliza builds dependentes de *spell spam* e bonifica proteção (`SpellShield`) e *Overwhelm*.

---

## 6. Conclusão

A extensão desenvolvida cumpriu integralmente o objetivo proposto na disciplina: preservou a arquitetura do Algoritmo Genético de Balbinot et al. (SBGames 2024), transpôs o problema combinatório para uma base de dados PvE de *O Caminho dos Campeões* e validou a nova função de fitness segundo a metodologia GQM. Os resultados empíricos demonstraram 100% de convergência ao ótimo global na configuração `conf3` em menos de 50 milissegundos, com total aderência às builds de referência da comunidade.

---

## 7. Referências Bibliográficas

*(Todas as referências abaixo foram verificadas e constam no artigo base de Balbinot et al., 2024)*

* BALBINOT, R. A.; COSTA, L. M.; SOUZA, A. C. C.; SOUZA, F. C. M. Developing Competitive Strategies for Legends of Runeterra using Genetic Algorithm. In: *XXIII Simpósio Brasileiro de Jogos e Entretenimento Digital (SBGames 2024)*, Manaus/AM, 2024.
* BASILI, V.; WEISS, D. A methodology for collecting valid software engineering data. *IEEE Transactions on Software Engineering*, v. 10, n. 6, p. 728–738, 1984.
* CHEN, Z.; AMATO, C.; NGUYEN, T.-H. D.; COOPER, S.; SUN, Y.; EL-NASR, M. S. Q-deckrec: A fast deck recommendation system for collectible card games. In: *2018 IEEE Conference on Computational Intelligence and Games (CIG)*, p. 1–8, 2018.
* GARCÍA-SÁNCHEZ, P.; TONDA, A.; SQUILLERO, G.; MORA, A.; MERELO, J. J. Evolutionary deckbuilding in Hearthstone. In: *2016 IEEE Conference on Computational Intelligence and Games (CIG)*, p. 1–8, 2016.
* KRAMER, O. *Genetic Algorithm Essentials*. Springer, 2017.
* RIOT GAMES. *Legends of Runeterra*. 2024.
* WEISE, T. *Global Optimization Algorithms – Theory and Application*. 1st ed., 2008.
