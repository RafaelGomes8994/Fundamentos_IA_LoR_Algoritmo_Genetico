# Guia de Uso: Otimizador de Builds — Path of Champions (LoR)

Instruções práticas para executar os testes, os experimentos científicos (RQ1, RQ2 e RQ3) e a interface de linha de comando (CLI) do projeto.

---

## 1. Pré-requisitos

* **Python:** 3.10 ou superior.
* **Dependências:** Nenhuma biblioteca externa é necessária (100% biblioteca padrão do Python).

---

## 2. Executar os Testes Automatizados

Para validar as regras de *stackability*, o carregamento da base de dados, os componentes da função de fitness, os operadores genéticos e as três estratégias ($E_1, E_2, E_3$):

```powershell
python -m unittest discover tests -v
```

Saída esperada:
```text
Ran 31 tests in ~0.15s
OK
```

---

## 3. Reproduzir o Estudo Experimental (SBGames 2024 / GQM)

Para executar o experimento que compara as três configurações do artigo base (`conf1`, `conf2` e `conf3`, com 30 repetições cada) contra o **Ótimo Global Exato** (busca exaustiva sobre as 6.188 combinações válidas):

```powershell
python examples/benchmark_vs_exact.py
```

---

## 4. Executar o Otimizador via Linha de Comando (`examples/demo_cli.py`)

### 4.1. Estratégia $E_1$ — Otimização Geral para um Campeão
```powershell
python examples/demo_cli.py --champion Jinx --stars 3 --top_k 3
```

### 4.2. Estratégia $E_2$ — Otimização com Exclusão/Banimento Fixo de Relíquia
Exclui uma relíquia específica do espaço de busca (ex.: quando o jogador não possui a relíquia ou deseja testar alternativas):
```powershell
python examples/demo_cli.py --champion Jinx --stars 3 --ban-relic "The Loose Cannon's Payload"
```

### 4.3. Estratégia $E_3$ — Otimização Contra um Chefe Específico
Adapta a escolha de relíquias para responder aos mutadores de um chefe (ex.: *Lissandra*, *Aurelion Sol*, *Swain*, *Teemo*):
```powershell
python examples/demo_cli.py --champion Jinx --stars 3 --boss Lissandra --top_k 3
```

### 4.4. Comparar Adaptação Diante de Múltiplos Chefes
```powershell
python examples/demo_cli.py --champion Yasuo --stars 3 --compare-bosses
```

### 4.5. Verificar Otimalidade Individual contra Busca Exaustiva
```powershell
python examples/demo_cli.py --champion "Aurelion Sol" --benchmark
```

### 4.6. Listar Campeões e Chefes Cadastrados
```powershell
python examples/demo_cli.py --list-champions
python examples/demo_cli.py --list-bosses
```

---

## 5. Gerar Catálogo para Todos os 60 Campeões

Para rodar o Algoritmo Genético para todos os 60 campeões e atualizar a tabela em `Docs/ALL_CHAMPIONS_BUILDS.md`:

```powershell
python examples/run_all_champions.py
```
