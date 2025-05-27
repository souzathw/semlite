# 📊 SEMLITE — Modelagem de Equações Estruturais Descomplicada

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![R Compatible](https://img.shields.io/badge/R-Compatible-success?logo=r)](https://cran.r-project.org/)
[![Status](https://img.shields.io/badge/status-Beta-yellow)]()

---

## 🎯 O que é o SEMLITE?

**SEMLITE** é um pacote Python criado para **facilitar análises de Modelagem de Equações Estruturais (MEE)** — como **mediação**, **moderação** e **análise fatorial confirmatória (CFA)** — de maneira simples e intuitiva.

O foco principal é permitir que **pesquisadores da Psicologia, Educação e Ciências Humanas** usem essas análises **diretamente do R**, sem precisar escrever código complexo.

---

## 🧰 Funcionalidades

- ✅ `run_cfa()` – análise fatorial confirmatória
- ✅ `run_mediation()` – modelagem com variável mediadora
- ✅ `run_moderation()` – modelagem com variável moderadora (interação média ou item-a-item)
- ✅ Mensagens amigáveis para quem está começando
- ✅ Pronto para ser usado no **RStudio** com o pacote [`reticulate`](https://rstudio.github.io/reticulate/)

---

## 📦 Instalação

### 🔹 Instalação no **R**

> ⚠️ É necessário já ter o **Python** instalado no seu sistema.

1️⃣ No console do R, instale o pacote `reticulate`:

```r
install.packages("reticulate")
```

2️⃣ Em seguida, execute as importações necessárias:

```r
library(reticulate)

py_install("git+https://github.com/souzathw/semlite.git")
sem <- import("semlite.moderation")
```

3️⃣ Carregue seu arquivo CSV:

```r
caminho_csv <- file.choose()
df <- read.csv(caminho_csv, sep = ",")
```

4️⃣ Rode o modelo de moderação (edite as variáveis conforme seu banco de dados):

```r
result <- sem$run_moderation(
  data_path = caminho_csv,
  iv = "SAUFAM",
  dv = "CULPA",
  moderator = "SSF",
  interaction_type = "mean",  # ou "product" para interação produto
  indicators = dict(
    SAUFAM = c("SAUFAM1", "SAUFAM2", "SAUFAM3", "SAUFAM4", "SAUFAM5"),
    SSF = c("SSF1", "SSF2", "SSF3", "SSF4"),
    CULPA = c("CULPA1", "CULPA2", "CULPA3", "CULPA4", "CULPA5",
              "CULPA6", "CULPA7", "CULPA8", "CULPA9", "CULPA10")
  )
)

cat("Modelo de Moderação construído:\n")
cat(result$model_description, "\n\n")

cat("Estimativas dos parâmetros:\n")
print(result$estimates)
```

---

### 🔹 Instalação no **Python** (localmente)

```bash
git clone https://github.com/souzathw/semlite.git
cd semlite
pip install .
```

---

## 🧠 Licença

Este projeto está licenciado sob a licença MIT — veja o arquivo [LICENSE](LICENSE) para detalhes.
