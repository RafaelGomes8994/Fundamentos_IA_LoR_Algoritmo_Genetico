# Formulação Matemática do Algoritmo Genético (Modo PvE — Path of Champions)

Este documento formaliza o modelo matemático implementado em `src/fitness.py` e `src/genetic_algorithm.py`, estendendo a formulação de **Balbinot et al. (SBGames 2024)** para o modo PvE *O Caminho dos Campeões* (*The Path of Champions*).

---

## 1. Espaço de Busca e Representação do Cromossomo

Seja $\mathcal{R} = \{r_1, r_2, \dots, r_M\}$ o conjunto finito de $M = 34$ relíquias catalogadas no banco de dados (`data/lor_genetic_algorithm_base.csv` e `data/poe_legends_of_runeterra_builds.csv`). Cada relíquia $r \in \mathcal{R}$ possui os atributos:
$$r = \langle \text{rarity}(r), \text{base}(r), \text{stackable}(r), \text{tags}(r) \rangle$$

* $\text{rarity}(r) \in \{\text{Common}, \text{Rare}, \text{Epic}\}$
* $\text{base}(r) \in \mathbb{R}^+$ é a pontuação intrínseca da relíquia
* $\text{stackable}(r) \in \{\text{True}, \text{False}\}$ indica se múltiplas cópias podem ser equipadas simultaneamente
* $\text{tags}(r) \subseteq \mathcal{T}$ é o conjunto de descritores mecânicos da relíquia

### Indivíduo (Cromossomo)
Analogamente ao *lineup* de 3 arquétipos $(d_1, d_2, d_3)$ do artigo base, um indivíduo $B$ é um vetor de 3 relíquias:
$$B = (r_1, r_2, r_3) \in \mathcal{R}^3$$

### Restrições de Viabilidade ($\Omega_{\text{valid}}$)
Substituindo a regra *Riot Lock* do modo PvP pela regra de acúmulo (*stackability*) do modo PvE (e eventual exclusão fixa $r_{\text{ban}}$ na Estratégia $E_2$), o subespaço viável $\Omega_{\text{valid}} \subset \mathcal{R}^3$ (com $|\Omega_{\text{valid}}| = 6.188$ combinações únicas sem banimento) é definido por:
$$\Omega_{\text{valid}} = \left\{ B = (r_1, r_2, r_3) \in (\mathcal{R} \setminus \{r_{\text{ban}}\})^3 \;\middle|\; \forall r \in \mathcal{R}, \; \sum_{i=1}^3 \mathbb{I}(r_i = r) > 1 \implies \text{stackable}(r) = \text{True} \right\}$$
onde $\mathbb{I}(\cdot)$ é a função indicadora booleana.

---

## 2. Função de Avaliação (Fitness Function)

Para um indivíduo $B$, dado um Campeão $C$, nível de Poder Estelar $S \in \{1, \dots, 6\}$ e um Chefe alvo opcional $B_{oss}$, a função objetivo $f(B \mid C, S, B_{oss})$ é definida por:

$$f(B \mid C, S, B_{oss}) = 
\begin{cases} 
-9999.0, & \text{se } B \notin \Omega_{\text{valid}} \\
w_1 f_{\text{base}}(B) + w_2 f_{\text{champ}}(B, C) + w_3 f_{\text{star}}(B, C, S) + w_4 f_{\text{combo}}(B) + w_5 f_{\text{boss}}(B, B_{oss}), & \text{se } B \in \Omega_{\text{valid}}
\end{cases}$$

com pesos calibrados $\mathbf{w} = [0.15, 0.40, 0.15, 0.15, 0.15]$ ($\sum_{k=1}^5 w_k = 1.0$).

### Detalhamento dos Termos:

1. **Poder Base das Relíquias ($f_{\text{base}}$):**
   $$f_{\text{base}}(B) = \sum_{i=1}^3 \text{base}(r_i)$$

2. **Sinergia Campeão–Relíquia ($f_{\text{champ}}$):**
   Seja $\mathbf{\Sigma}_{C, r} \ge 0$ a pontuação de sinergia entre o Campeão $C$ e a relíquia $r$:
   $$f_{\text{champ}}(B, C) = \sum_{i=1}^3 \mathbf{\Sigma}_{C, r_i}$$

3. **Sinergia com Poder Estelar ($f_{\text{star}}$):**
   $$f_{\text{star}}(B, C, S) = \sum_{i=1}^3 \left( 0.1 \cdot S \cdot \mathbf{\Sigma}_{C, r_i} \cdot \mathbb{I}(\mathbf{\Sigma}_{C, r_i} \ge 5.0) + \min(1.0 \cdot S, 5.0) \cdot \mathbb{I}(r_i \in \text{Milestones}(C, S)) \right)$$

4. **Sinergia entre Relíquias / Combos ($f_{\text{combo}}$):**
   Seja $\mathcal{K} = \{(K_j, \beta_j)\}$ o catálogo de combos sinérgicos entre relíquias:
   $$f_{\text{combo}}(B) = \sum_{(K_j, \beta_j) \in \mathcal{K}} \beta_j \cdot \mathbb{I}(K_j \sqsubseteq B)$$

5. **Efetividade vs. Chefe ($f_{\text{boss}}$ — Estratégia $E_3$):**
   Dados os conjuntos de tags do chefe $\mathcal{T}_{\text{counter}}(B_{oss})$, $\mathcal{T}_{\text{vuln}}(B_{oss})$ e $\mathcal{T}_{\text{penalized}}(B_{oss})$:
   $$f_{\text{boss}}(B, B_{oss}) = \sum_{i=1}^3 \sum_{t \in \text{tags}(r_i)} \left( 3.0 \cdot \mathbb{I}(t \in \mathcal{T}_{\text{counter}}) + 2.0 \cdot \mathbb{I}(t \in \mathcal{T}_{\text{vuln}}) - 3.5 \cdot \mathbb{I}(t \in \mathcal{T}_{\text{penalized}}) \right)$$

---

## 3. Operadores Evolutivos (Conforme Figura 4 de Balbinot et al., 2024)

1. **Seleção por Torneio ($k=3$):** Amostra 3 candidatos da população e seleciona $\arg\max_{B} f(B)$.
2. **Cruzamento Posicional em Dois Passos:** Dados dois pais $(ap_i, ap_j)$, gera dois filhos invertendo a ordem dos pais na segunda passagem:
   $$c^{(1)} = \left( ap_{i,1}, \; ap_{j,2}, \; \text{Choice}_{0.5}(ap_{i,3}, ap_{j,3}) \right)$$
   $$c^{(2)} = \left( ap_{j,1}, \; ap_{i,2}, \; \text{Choice}_{0.5}(ap_{j,3}, ap_{i,3}) \right)$$
   seguido do operador de reparação $\rho: \mathcal{R}^3 \to \Omega_{\text{valid}}$ caso ocorra duplicação de relíquia não acumulável.
3. **Mutação Pontual ($TM$):** Com probabilidade $TM \in \{0.3, 0.5, 0.7\}$, sorteia uma posição $idx \in \{1, 2, 3\}$ do indivíduo e substitui por uma relíquia válida de $\mathcal{R}$.
4. **Elitismo ($E=2$):** Preserva os 2 melhores indivíduos da geração $t$ na geração $t+1$, garantindo monotonicidade do melhor fitness: $\max_{B \in \mathcal{P}_{t+1}} f(B) \ge \max_{B \in \mathcal{P}_t} f(B)$.
