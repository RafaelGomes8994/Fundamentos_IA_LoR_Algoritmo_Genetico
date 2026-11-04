# 🎯 Manual Definitivo de Treinamento e Defesa da Apresentação
## Otimização de Builds em Legends of Runeterra via Algoritmo Genético
> **Disciplina:** Fundamentos de Inteligência Artificial — DCOMP / UFS  
> **Apresentador:** Rafael Gomes Oliveira Santos  
> **Meta:** Nota 5,0 / 5,0 + 2,0 Pontos Extras = **7,0 Pontos Máximos**  
> **Tempo Obrigatório:** Entre 5 e 9 minutos (Janela Alvo de Excelência: **6m30s a 7m30s**)

---

## 🏆 1. Estratégia de Apresentação e Critérios de Avaliação

Segundo o documento oficial de avaliação da disciplina (`Trabalho.pdf`), sua pontuação será distribuída nos seguintes pilares:

| Critério | Peso | O que a banca avalia | Como garantir a nota máxima |
| :--- | :---: | :--- | :--- |
| **Domínio do Assunto** | `1,0 pt` | Fluência conceitual sobre o Algoritmo Genético, a modelagem e os dados | Saber explicar a fórmula do fitness, os operadores genéticos e a tabela sem gaguejar ou hesitar. |
| **Controle de Tempo** | `1,5 pt` | Apresentar estritamente entre 5 e 9 minutos | Cronometrar **~45 a 50 segundos por slide**. Treinar com cronômetro para cravar entre 6m30s e 7m30s. |
| **Clareza dos Slides** | `1,5 pt` | Legibilidade, ausência de erros de português e organização visual | Seus slides (Canva/PDF) já possuem padrão visual profissional, sem poluição e 100% revisados. |
| **Postura e Firmeza** | `1,0 pt` | Contato visual com a banca, tom de voz seguro, postura ereta | Não ler o slide. O slide é guia visual para a banca; você conduz a narrativa olhando para o professor. |
| **Pontos Extras (Resultado)** | `até +2,0` | Qualidade do resultado, validação contra o ótimo global e relevância prática | Mostrar que a `conf3` atingiu **100,0% de otimalidade** em **~45 ms** e bateu com os guias competitivos mundiais. |

> [!TIP]
> **A Regra de Ouro da Postura:**  
> Mantenha os ombros relaxados, fale com voz firme e pausada. Nunca peça desculpas ou use expressões de incerteza ("eu acho que", "talvez seja"). Use afirmações técnicas diretas: *"Como modelamos...", "Os dados empíricos demonstram...", "A convergência na configuração 3 comprovou..."*.

---

## ⏱️ 2. Roteiro "Fala por Fala" Slide a Slide (Cronometrado: 7 Minutos)

Treine lendo este roteiro em voz alta com um cronômetro ao lado. Quando dominar as ideias, use suas próprias palavras mantendo as palavras-chave em negrito.

```
+---------------+---------------+---------------+---------------+---------------+---------------+---------------+---------------+---------------+
| Slide 1: Capa | Slide 2: Ext. | Slide 3: AG   | Slide 4: Fit. | Slide 5: GQM  | Slide 6: Qnt. | Slide 7: Qlt. | Slide 8: Cnc. | Slide 9: Rep. |
|   0m00-0m45   |   0m45-1m30   |   1m30-2m15   |   2m15-3m15   |   3m15-4m00   |   4m00-5m00   |   5m00-6m00   |   6m00-6m45   |   6m45-7m30   |
+---------------+---------------+---------------+---------------+---------------+---------------+---------------+---------------+---------------+
```

---

### 🖥️ Slide 1: Capa e Identificação
* **Tempo planejado:** `0m00s` a `0m45s` (45 segundos)
* **Tempo acumulado:** `0m45s`
* **O que apontar na tela:** O título do projeto, seu nome e o card com o QR Code no canto direito.

#### 🎙️ O Que Falar:
> *"Bom dia, professor. Bom dia a todos.*  
> *Meu nome é **Rafael Gomes** e hoje apresento o trabalho prático final da disciplina de Fundamentos de Inteligência Artificial, intitulado: **Otimização de Builds no Legends of Runeterra via Algoritmo Genético**.*  
> *Na primeira etapa da disciplina, analisamos o artigo de **Balbinot e colaboradores**, publicado no **SBGames 2024**, que utilizou Algoritmos Genéticos para otimizar seleções competitivas no formato PvP.*  
> *Naquela ocasião, propus como extensão adaptar essa inteligência evolutiva para o modo PvE **O Caminho dos Campeões**, reformulando a base de dados e a função de avaliação de acordo com as mecânicas do jogo, mas preservando rigorosamente a arquitetura do algoritmo genético.*  
> *No canto do slide há um QR Code que dá acesso direto ao repositório público no GitHub com todo o código-fonte, suíte de testes e instruções de execução."*

---

### 🖥️ Slide 2: Do Problema Original (PvP) ao Objetivo Proposto (PvE)
* **Tempo planejado:** `0m45s` a `1m30s` (45 segundos)
* **Tempo acumulado:** `1m30s`
* **O que apontar na tela:** O contraste entre a coluna esquerda (artigo base / PvP) e a coluna direita (sua extensão / PvE).

#### 🎙️ O Que Falar:
> *"Para compreendermos a transição: no artigo base, o cenário era estritamente **PvP no formato Riot Lock**, onde o jogador precisava selecionar uma trinca de baralhos para torneios, avaliados por uma matriz de winrate histórico entre arquétipos.*  
> *O objetivo que me comprometi a cumprir foi migrar essa meta-heurística para o modo **PvE 'O Caminho dos Campeões'**, que hoje é o modo principal do Legends of Runeterra. Nele, o jogador escolhe um Campeão e equipa **3 Relíquias passivas** para enfrentar desafios e chefes mundiais.*  
> *O ponto fundamental aqui é que **a arquitetura evolutiva do artigo base foi preservada integralmente**: mantivemos o torneio com k=3, o crossover em dois passos, o elitismo de 2 indivíduos e as taxas de teste.*  
> *Para alimentar esse algoritmo, construímos uma base estruturada com **60 Campeões, 34 Relíquias, 8 Combos e 8 Chefes**, mapeando diretamente as três estratégias táticas do artigo: E1 como Build Geral, E2 como Restrição de Inventário e E3 como Contra-Chefe Específico."*

---

### 🖥️ Slide 3: Modelagem Cromossômica e Operadores Evolutivos
* **Tempo planejado:** `1m30s` a `2m15s` (45 segundos)
* **Tempo acumulado:** `2m15s`
* **O que apontar na tela:** Os 4 blocos numerados (01 Indivíduo, 02 Espaço Factível, 03 Seleção/Elitismo, 04 Crossover/Mutação).

#### 🎙️ O Que Falar:
> *"Na modelagem cromossômica, cada indivíduo da população é representado por uma tripla de relíquias: **B = (r1, r2, r3)**, equipadas simultaneamente no campeão.*  
> *Aqui introduzimos uma restrição de domínio indispensável chamada **stackability**: no jogo real, relíquias Épicas e a maioria das Raras são únicas — só é permitido equipar 1 exemplar. Apenas algumas relíquias específicas permitem múltiplas cópias.*  
> *Considerando essa regra de acúmulo entre as 34 relíquias do catálogo, nosso **espaço de busca factível possui exatamente 6.188 combinações válidas**.*  
> *Os operadores genéticos seguem à risca o artigo original: a **seleção é por Torneio com k=3**; o **crossover reproduz fielmente a Figura 4 do artigo**, invertendo a ordem dos pais para gerar dois filhos; em seguida, atua um **operador determinístico de reparo** caso haja duplicação ilegal de relíquia única; e preservamos as 2 melhores soluções de cada geração via **elitismo**."*

---

### 🖥️ Slide 4: A Nova Função de Fitness Multidimensional
* **Tempo planejado:** `2m15s` a `3m15s` (60 segundos)
* **Tempo acumulado:** `3m15s`
* **O que apontar na tela:** A fórmula matemática no topo e a pizza com os 5 componentes ponderados.

#### 🎙️ O Que Falar:
> *"Como no modo PvE não existe uma matriz de taxa de vitória entre baralhos, o maior desafio foi desenhar uma **função de aptidão multidimensional representativa**.*  
> *Nossa função avalia cinco dimensões cujos pesos somam 100%:*  
> * **15% para o Poder Base:** reflete a raridade da relíquia — Comum, Rara ou Épica;*  
> * **40% para a Sinergia Campeão-Relíquia:** é o peso principal, calibrado pelas bases e tier lists de especialistas da comunidade. Por exemplo, a relíquia Loose Cannon's Payload descarta toda a mão do jogador; para a Jinx, que causa dano direto ao queimar cartas, a sinergia é máxima; para um campeão que precisa de cartas na mão, ela é prejudicial;*  
> * **15% para o Poder Estelar:** escalona os bônus conforme o nível de estrelas do campeão, de 1 a 6 estrelas;*  
> * **15% para Combos entre Relíquias:** bonifica pares que funcionam em sinergia mútua quando equipados juntos;*  
> * E **15% para a Efetividade Contra o Chefe:** utilizado na Estratégia E3, aplicando bônus de +3,0 pontos para relíquias que anulam mecânicas do chefe e penalidade severa de -3,5 para relíquias punidas pelos mutadores do chefe."*

---

### 🖥️ Slide 5: Metodologia Experimental (Modelo GQM)
* **Tempo planejado:** `3m15s` a `4m00s` (45 segundos)
* **Tempo acumulado:** `4m00s`
* **O que apontar na tela:** Os blocos RQ1, RQ2 e RQ3 e os parâmetros das três configurações.

#### 🎙️ O Que Falar:
> *"Para validar experimentalmente o algoritmo, seguimos com rigor o **paradigma GQM de Basili e Weiss (1984)** adotado por Balbinot et al., formulando três questões de pesquisa:*  
> * **RQ1 para Efetividade:** Quão próximo do ótimo global exato o AG converge?*  
> * **RQ2 para Eficiência:** Qual é o tempo de processamento em milissegundos?*  
> * **RQ3 para Representatividade:** As builds encontradas coincidem com o consenso dos jogadores especialistas?*  
> *Avaliamos as **mesmas três configurações de parâmetros** do artigo base: conf1 com baixa exploração (P=10, G=10), conf2 intermediária (P=20, G=50) e conf3 com alta exploração (P=30, G=100 e taxa de mutação de 0,7), cada uma executada por **30 repetições independentes**.*  
> *E aqui está o diferencial científico do nosso trabalho: como o espaço factível tem 6.188 combinações, implementamos uma **Busca Exaustiva Exata para servir como Ground Truth**, permitindo calcular com precisão matemática a taxa de otimalidade do Algoritmo Genético."*

---

### 🖥️ Slide 6: Resultados Quantitativos (RQ1 e RQ2)
* **Tempo planejado:** `4m00s` a `5m00s` (60 segundos)
* **Tempo acumulado:** `5m00s`
* **O que apontar na tela:** A linha da Jinx, a linha do Aurelion Sol e as colunas de 100% na conf3 em ~45 ms.

#### 🎙️ O Que Falar:
> *"Nesta tabela confrontamos o ótimo global exato com o desempenho médio do AG para quatro campeões representativos:*  
> *Na **conf1**, com apenas 10 gerações, observamos claramente o fenômeno de **convergência prematura**, onde o algoritmo atinge entre 74% e 82% do ótimo — exatamente o mesmo comportamento de estagnação relatado por Balbinot et al. no artigo original.*  
> *Na **conf2**, com 50 gerações, a precisão salta para praticamente 100% em cerca de 12 a 14 milissegundos.*  
> *E na **conf3**, com população 30, taxa de mutação 0,7 e 100 gerações, o Algoritmo Genético atingiu **100,0% de otimalidade com desvio padrão zero** em todas as 30 repetições para todos os campeões avaliados.*  
> *Em termos de eficiência (RQ2), o tempo médio de execução ficou em torno de **42 a 48 milissegundos**. Isso é cerca de **4 vezes mais rápido** do que a média de 190 milissegundos reportada no artigo base, mantendo um custo computacional extremamente baixo."*

---

### 🖥️ Slide 7: Resultados Qualitativos (RQ3 e Estratégias)
* **Tempo planejado:** `5m00s` a `6m00s` (60 segundos)
* **Tempo acumulado:** `6m00s`
* **O que apontar na tela:** Os cards da Jinx, do Swain e da adaptação contra a Lissandra.

#### 🎙️ O Que Falar:
> *"Quanto à representatividade qualitativa (RQ3), os resultados demonstraram que o algoritmo não apenas converge matematicamente, mas toma decisões táticas corretas:*  
> *Na **Estratégia E1**, para a Jinx, o AG encontrou a build com Loose Cannon's Payload, Luden's Tempest e Scourge's Stash — **100% idêntica à build Best-in-Slot** recomendada pelas planilhas competitivas mundiais.*  
> *Um comportamento emergente notável ocorreu no **Swain**: o algoritmo explorou autonomamente a regra de stackability e descobriu que equipar **duas cópias de Gatebreaker** combinadas ao Ravenous Flock maximiza o dano direto no nexo do oponente.*  
> *Na **Estratégia E2**, quando simulamos a indisponibilidade da relíquia principal da Jinx, o AG reconfigurou a tripla de forma inteligente para Scourge's Stash com duas cópias de Luden's Tempest.*  
> *E na **Estratégia E3**, enfrentando a chefe Lissandra de 5 estrelas — cujo mutador encarece feitiços jogados repetidamente —, o algoritmo penalizou relíquias de spam e priorizou proteção com SpellShield e atributos brutos."*

---

### 🖥️ Slide 8: Conclusões e Referências Bibliográficas
* **Tempo planejado:** `6m00s` a `6m45s` (45 segundos)
* **Tempo acumulado:** `6m45s`
* **O que apontar na tela:** As duas conclusões principais e as referências acadêmicas SBC.

#### 🎙️ O Que Falar:
> *"Em conclusão:*  
> *Primeiro: **o objetivo proposto na Etapa 1 foi integralmente cumprido**. Conseguimos transpor a abordagem evolutiva do PvP para o modo PvE O Caminho dos Campeões para todos os 60 campeões do jogo.*  
> *Segundo: comprovamos experimentalmente que a combinação dos operadores genéticos com a nova função de fitness atinge **100,0% de precisão em menos de 50 milissegundos**, validada matematicamente contra o Ground Truth da busca exaustiva.*  
> *Todas as referências teóricas aqui utilizadas constam diretamente no artigo base de Balbinot et al. no SBGames, na metodologia GQM de Basili e Weiss e nos fundamentos clássicos de Oliver Kramer."*

---

### 🖥️ Slide 9: Repositório no GitHub, Código Aberto e Q&A
* **Tempo planejado:** `6m45s` a `7m30s` (45 segundos)
* **Tempo acumulado:** `7m30s` (Perfeito na janela de 5 a 9 minutos!)
* **O que apontar na tela:** O QR Code central grande e os comandos de teste no terminal.

#### 🎙️ O Que Falar:
> *"Para finalizar, deixo em tela o slide de encerramento com o **QR Code para o repositório público no GitHub**.*  
> *O projeto foi construído em Python 3.10 utilizando exclusivamente a biblioteca padrão, com zero dependências externas pesadas no núcleo do algoritmo.*  
> *O repositório possui uma **suíte de 31 testes unitários automatizados** cobrindo todas as regras de negócio, além dos scripts prontos para reproduzir a busca exaustiva, o benchmark GQM e a CLI interativa.*  
> *Muito obrigado pela atenção, professor e colegas, e fico à disposição para perguntas!"*

---

## 🛡️ 3. "O Guarda-Costas Técnico": Conceitos Fundamentais Explicados

Se o professor pedir para você abrir o código ou explicar a teoria por trás de uma função, tenha estas respostas na ponta da língua:

### 1. Como o Indivíduo é codificado? (`src/models.py`)
* **Estrutura:** Tupla de 3 strings com os nomes das relíquias: `Build(relics=(r1, r2, r3))`.
* **Validação (`is_valid_build`):**
  1. Verifica se tem exatamente 3 relíquias.
  2. Verifica se todas existem no catálogo de 34 relíquias.
  3. Checa duplicatas: se uma relíquia aparece mais de uma vez e tem `stackable = False`, a build é considerada inválida. Se for Épica, é sempre de uso único (`is_epic = True` $\rightarrow$ máximo 1 cópia).

### 2. Como o Cruzamento (Crossover) funciona? (`src/genetic_algorithm.py`)
* **Tipo:** Cruzamento Posicional em 2 Passos com Inversão de Pais (fiel à Seção 4.3 e Figura 4 de Balbinot et al.).
* **Passo 1 (Filho 1):** Slot 0 vem do Pai 1, Slot 1 vem do Pai 2, Slot 2 tem 50% de probabilidade de vir do Pai 1 ou do Pai 2.
* **Passo 2 (Filho 2):** Inverte-se a ordem: Slot 0 vem do Pai 2, Slot 1 vem do Pai 1, Slot 2 vem do pai alternativo.
* **Reparo (`_repair_build`):** Se o crossover juntar duas relíquias iguais não acumuláveis, o algoritmo detecta o conflito deterministicamente e sorteia uma relíquia legal do catálogo que respeite as regras de acumulação.

### 3. Como a Mutação funciona? (`src/genetic_algorithm.py`)
* Para cada indivíduo filho gerado, sorteia-se um número aleatório entre 0 e 1.
* Se for menor ou igual à taxa $TM$ (0.3 em `conf1`, 0.5 em `conf2`, 0.7 em `conf3`), um dos 3 slots é sorteado e substituído por outra relíquia válida do catálogo.
* **Objetivo:** Introduzir novo material genético na população e impedir que o algoritmo fique preso em máximos locais.

### 4. Por que Elitismo ($E=2$)?
* Em cada geração, os 2 indivíduos com maior fitness da população atual são clonados diretamente para a próxima geração sem sofrer crossover ou mutação.
* **Garantia matemática:** O fitness máximo da população nunca decresce ao longo das gerações ($f_{\max}(G+1) \ge f_{\max}(G)$).

---

## ❓ 4. Super Simulador de Sabatina da Banca (15 Perguntas e Respostas)

Aqui estão as 15 perguntas que professores de Inteligência Artificial mais gostam de fazer em defesas práticas de Algoritmos Genéticos.

---

#### ❓ Pergunta 1: *"Por que a `conf1` convergiu prematuramente e obteve apenas ~75% a 82% do ótimo?"*
* **A Armadilha do Professor:** Quer ver se você entende a relação entre tamanho populacional, gerações e espaço de busca.
* **Sua Resposta Ideal:**
  > *"Excelente pergunta, professor. Na `conf1`, temos população $P=10$ e apenas $G=10$ gerações. Em 10 gerações com população 10, o algoritmo realiza no máximo cerca de 100 avaliações de fitness. Como nosso espaço factível tem 6.188 combinações, 100 avaliações cobrem menos de 1,6% do espaço de busca. Devido à seleção por torneio e ao elitismo, a população homogeneizou rapidamente em torno de um ótimo local antes que a taxa de mutação relativamente baixa ($TM=0.3$) pudesse explorar bacias de atração mais promissoras. Esse comportamento foi exatamente o mesmo reportado por Balbinot et al. no artigo original."*
* **O que NÃO falar:** *"Acho que foi azar na semente aleatória."*

---

#### ❓ Pergunta 2: *"Se o espaço de busca tem apenas 6.188 combinações e a Busca Exaustiva roda rápido, por que usar Algoritmo Genético?"*
* **A Armadilha do Professor:** Questionar a utilidade da meta-heurística frente à força bruta.
* **Sua Resposta Ideal:**
  > *"Utilizamos a Busca Exaustiva especificamente neste experimento como um instrumento metodológico de controle — ou seja, para estabelecer o Ground Truth científico e provar matematicamente a taxa de otimalidade do AG. No cenário simplificado de 3 relíquias dentre 34, a força bruta ainda é tratável em poucos segundos. Porém, no jogo real completo, um setup de combate envolve escolher 3 relíquias, 4 poderes mutadores de partida e a seleção de suporte de cartas, elevando o espaço combinatório para a ordem de $10^9$ a $10^{12}$ estados. Em um espaço dessa magnitude, a busca exaustiva é computacionalmente proibitiva, tornando meta-heurísticas populacionais como o Algoritmo Genético a única solução viável em tempo real."*
* **O que NÃO falar:** *"Usei AG só porque o professor pediu no trabalho."*

---

#### ❓ Pergunta 3: *"De onde saíram os pesos da função de fitness: 0,15, 0,40, 0,15, 0,15, 0,15? Por que não pesos iguais de 0,20?"*
* **A Armadilha do Professor:** Testar se os pesos foram chutados sem critério ou se há fundamentação de domínio.
* **Sua Resposta Ideal:**
  > *"Os pesos foram definidos com base na importância relativa de cada dimensão na dinâmica do jogo: a Sinergia Campeão-Relíquia recebeu o peso dominante de 40% porque no Path of Champions uma relíquia com atributos altos, mas sem afinidade mecânica com o campeão, torna a partida inviável em dificuldades altas. Os outros quatro componentes — Poder Base (15%), Poder Estelar (15%), Combos entre Relíquias (15%) e Efetividade Contra o Chefe (15%) — atuam como moduladores balanceados. Essa distribuição foi validada empiricamente na Questão de Pesquisa RQ3, onde as builds ótimas produzidas pela função convergiram com 100% de precisão para as recomendações de consenso dos guias de elite da comunidade."*

---

#### ❓ Pergunta 4: *"Como você tratou indivíduos inválidos que violavam a regra de stackability durante o cruzamento?"*
* **A Armadilha do Professor:** Quer saber se você usou penalização por morte súbita ou operador de reparo.
* **Sua Resposta Ideal:**
  > *"Adotamos uma abordagem robusta em duas camadas: na camada evolutiva, implementamos um operador de reparo determinístico chamado `_repair_build`. Assim que o crossover gera um cromossomo que duplica uma relíquia única, o reparo substitui imediatamente a cópia excedente por uma relíquia válida do catálogo antes da inserção na população. Na camada de fitness, como redundância defensiva, qualquer build que porventura chegasse inválida receberia uma penalidade drástica de fitness igual a -9.999,0, garantindo que indivíduos ilegais fossem imediatamente extintos na seleção por torneio."*

---

#### ❓ Pergunta 5: *"Por que a taxa de mutação na `conf3` é tão alta ($TM=0.7$)? 70% não destrói as boas soluções?"*
* **A Armadilha do Professor:** Conceito clássico de AG onde mutação costuma ser de 1% a 5% em codificação binária.
* **Sua Resposta Ideal:**
  > *"Em Algoritmos Genéticos clássicos de representação binária longa, taxas de mutação costumam ser baixas (1% a 5%) para evitar deriva genética aleatória. No entanto, no trabalho de Balbinot et al. e na nossa extensão, o cromossomo é discreto e muito curto — tem apenas 3 genes. Com um cromossomo de 3 posições, uma taxa de mutação de 0,7 significa que há 70% de chance de alterar apenas um dos três genes. Além disso, temos o operador de Elitismo com $E=2$: os dois melhores indivíduos nunca sofrem mutação, o que protege a melhor solução absoluta contra destruição enquanto a alta mutação garante diversidade contínua no restante da população."*

---

#### ❓ Pergunta 6: *"Qual é a diferença entre a Estratégia E1, E2 e E3 na prática?"*
* **Sua Resposta Ideal:**
  > *"A Estratégia E1 busca a build ótima geral para o campeão, sem considerar restrições de inventário nem chefes específicos. A Estratégia E2 simula uma restrição prática: o jogador não possui determinada relíquia (por exemplo, Loose Cannon's Payload da Jinx); o algoritmo exclui essa relíquia do catálogo factível e encontra a melhor build alternativa. Já a Estratégia E3 é a otimização contra um chefe específico: a função de fitness ativa o componente $f_{\text{boss}}$, bonificando relíquias que anulam mecânicas daquele chefe e penalizando severamente estratégias que caem em suas armadilhas."*

---

#### ❓ Pergunta 7: *"Como o Algoritmo Genético descobriu que o Swain ficava melhor com duas cópias de Gatebreaker?"*
* **Sua Resposta Ideal:**
  > *"Essa foi uma das descobertas emergentes mais fascinantes da RQ3. O catálogo define o Gatebreaker com a flag `stackable = True`. O poder do Gatebreaker faz o campeão golpear o nexo inimigo ao ser invocado. Como o Swain tem custo de mana e mecânicas de dano direto, o fitness composto calculou que equipar dois Gatebreakers gerava um dano acumulado superior a qualquer combinação com relíquias de uso único. O AG identificou essa sinergia sem nenhuma regra hardcoded, apenas explorando o espaço factível."*

---

#### ❓ Pergunta 8: *"Como você garante a reprodutibilidade dos resultados?"*
* **Sua Resposta Ideal:**
  > *"Seguindo o protocolo científico da Seção 5 de Balbinot et al., todas as três configurações foram executadas através do script `examples/benchmark_vs_exact.py` em 30 repetições independentes com controle de sementes aleatórias. Além disso, implementamos 31 testes unitários automatizados em `tests/` que validam cada operador genético, cada termo do fitness e o carregador de dados com 100% de aprovação no runner padrão `unittest` do Python."*

---

#### ❓ Pergunta 9: *"O que aconteceria se você usasse seleção por Roleta em vez de Torneio?"*
* **Sua Resposta Ideal:**
  > *"A seleção proporcional por roleta é vulnerável a duas falhas clássicas: primeiro, quando há indivíduos com fitness desproporcionalmente dominante no início, ela provoca convergência prematura extrema; segundo, quando a população homogeneíza e os valores de fitness ficam muito próximos, ela perde a pressão seletiva e vira uma amostragem quase aleatória. A seleção por Torneio com $k=3$, adotada por Balbinot et al., mantém uma pressão seletiva constante, independente da escala absoluta do fitness, e lida perfeitamente com fitness que contenha penalidades negativas."*

---

#### ❓ Pergunta 10: *"Como os dados de sinergia da comunidade foram coletados e estruturados?"*
* **Sua Resposta Ideal:**
  > *"Estruturamos duas bases em `data/`: o arquivo `poe_legends_of_runeterra_builds.csv`, compilado a partir de guias de jogadores de torneio e das planilhas comunitárias de consenso do Reddit/Discord oficial da Riot Games, contendo as builds Tier S+, S e A; e o arquivo `lor_genetic_algorithm_base.csv`, que modela os 60 campeões com seus poderes estelares, arquétipos e as tags de mecânicas de 8 chefes mundiais."*

---

#### ❓ Pergunta 11: *"Por que o tempo na `conf3` ficou em ~45 ms, sendo 4 vezes mais rápido que os 190 ms do artigo original?"*
* **Sua Resposta Ideal:**
  > *"No artigo original de Balbinot et al., para avaliar uma tripla de decks no PvP era necessário realizar consultas a matrizes de winrate entre todos os arquétipos do torneio. Na nossa modelagem PvE, a avaliação da função de fitness opera em memória com estruturas de dados vetorizadas em tempo $O(1)$, com tabelas hash para verificação de tags e stackability. Isso permitiu reduzir o tempo médio de ~190 ms para ~45 ms, mesmo processando 100 gerações."*

---

#### ❓ Pergunta 12: *"Quais são as limitações do seu modelo atual?"*
* **Sua Resposta Ideal:**
  > *"Uma limitação consciente de escopo foi modelar o inventário fixo em 3 slots de relíquias. No jogo real, o jogador desbloqueia o 1º slot no nível 1, o 2º no nível 8 e o 3º no nível 19. Como o objetivo do trabalho era otimizar a build final de desempenho máximo, focamos no estado de nível 30 com os 3 slots disponíveis. Como trabalho futuro, o cromossomo poderia ter tamanho variável para recomendar builds de progressão inicial de campanha."*

---

#### ❓ Pergunta 13: *"O algoritmo funcionaria para novos campeões ou novas relíquias adicionadas em futuras expansões?"*
* **Sua Resposta Ideal:**
  > *"Sim, com total escalabilidade. O código foi desacoplado de valores fixos. Para adicionar novos campeões, novas relíquias ou novos chefes, basta inserir uma nova linha na planilha CSV correspondente em `data/`. O módulo `src/data_loader.py` recalcula dinamicamente o catálogo factível e os novos combos sem necessidade de modificar uma única linha do motor do Algoritmo Genético."*

---

#### ❓ Pergunta 14: *"Qual biblioteca externa você usou para rodar o Algoritmo Genético? Deap? PyGAD?"*
* **Sua Resposta Ideal:**
  > *"Nenhuma biblioteca externa de terceiros, professor. O motor evolutivo inteiro em `src/genetic_algorithm.py`, a função de aptidão em `src/fitness.py` e a busca exata em `src/comparison.py` foram implementados do zero utilizando exclusivamente a biblioteca padrão do Python (`random`, `math`, `itertools`, `dataclasses`). Isso demonstra domínio completo da implementação dos operadores genéticos e garante portabilidade imediata sem dependências."*

---

#### ❓ Pergunta 15: *"Se você tivesse mais duas semanas de projeto, o que implementaria a seguir?"*
* **Sua Resposta Ideal:**
  > *"Implementaria duas extensões: primeiro, uma modelagem multi-objetivo via NSGA-II para equilibrar simultaneamente a taxa de vitória e a velocidade de finalização da partida (tempo de run); segundo, a integração da seleção de Poderes Mutadores que o jogador adquire durante os nós da trilha roguelike, expandindo o espaço de busca para otimização sequencial de rotas."*

---

## 📊 5. "Cola Rápida" (Cheat Sheet) de Números e Métricas para Decorar

Tenha estes números gravados na memória antes de entrar na sala:

```
+---------------------------------------------------------------------------------------+
| NÚMEROS CHAVE DO PROJETO                                                              |
| • 60 Campeões catalogados na base                                                     |
| • 34 Relíquias modeladas (Comuns, Raras, Épicas)                                      |
| • 8 Chefes Mundiais (Teemo, Swain, Lissandra, Aurelion Sol, etc.)                      |
| • 6.188 combinações válidas no Espaço Factível (regra de stackability)                |
| • 31 Testes Unitários Automatizados (100% aprovados em ~0,3s)                         |
+---------------------------------------------------------------------------------------+
| CONFIGURAÇÕES DE PARÂMETROS (30 Repetições cada)                                      |
| • conf1: P = 10,  TM = 0.3, G = 10   -> 74% a 82% do ótimo (convergência prematura)   |
| • conf2: P = 20,  TM = 0.5, G = 50   -> 99.9% a 100% do ótimo em ~13 ms               |
| • conf3: P = 30,  TM = 0.7, G = 100  -> 100.0% do ótimo global em ~45 ms (σ = 0,00)   |
|                                                                                       |
| • Benchmark do Artigo Base: 190 ms  ->  Nosso Tempo Médio: ~45 ms (4x mais rápido!)  |
+---------------------------------------------------------------------------------------+
| PESOS DA FUNÇÃO DE FITNESS (Total = 100%):                                            |
| • 15% Poder Base da Relíquia (raridade)                                               |
| • 40% Sinergia Campeão-Relíquia (afinidade mecânica e dados da comunidade)            |
| • 15% Poder Estelar (escalonamento 1★ a 6★)                                           |
| • 15% Combos entre Relíquias equipadas                                                |
| • 15% Efetividade Contra o Chefe (Estratégia E3: +3.0 counter / -3.5 penalidade)       |
+---------------------------------------------------------------------------------------+
```

---

## 🚀 6. Checklist de Última Hora Antes da Apresentação

- [ ] **Slide 1:** O QR Code está legível na tela inicial.
- [ ] **Slide 6:** Saber apontar com o mouse a linha da Jinx e do Aurelion Sol na tabela.
- [ ] **Slide 7:** Destacar o combo de Swain com duas cópias de *Gatebreaker* (descoberta autônoma).
- [ ] **Slide 9:** Manter este slide projetado durante as perguntas da banca.
- [ ] **Repositório GitHub:** Garantir que o repositório está marcado como **Public** nas configurações do GitHub.
- [ ] **Terminal aberto em segundo plano:** Deixar o terminal pronto com `python examples/demo_cli.py --champion Jinx --stars 3` caso o professor peça uma demonstração ao vivo!
