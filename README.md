# ⚛️ Laboratório Quântico Interativo v1.0

**Explore os mistérios da computação quântica com este laboratório interativo. Construa circuitos, visualize superposição, emaranhamento e interferência em tempo real com análises automáticas que explicam os resultados para você.**

---

![Demo do Laboratório Quântico](https://i.imgur.com/gKkISq4.png) 
*(Exemplo de imagem da interface. Um GIF mostrando a interação seria ainda melhor!)*

## 🔷 Sobre o Projeto

Este projeto nasceu da vontade de tornar os conceitos da computação quântica, muitas vezes abstratos e complexos, em algo visual, interativo e compreensível para todos. Em vez de apenas ler sobre superposição, aqui você pode criá-la com um clique e ver o resultado. Em vez de imaginar o emaranhamento, você pode construir um Estado de Bell e comprovar a "ação fantasmagórica à distância".

Este laboratório serve como uma ponte entre a teoria e a prática, oferecendo uma ferramenta educacional poderosa tanto para iniciantes curiosos quanto para estudantes da área.

### Principais Funcionalidades

* **Construtor de Circuitos Intuitivo:** Adicione portas quânticas e medições em múltiplos qubits com uma interface simples.
* **Exemplos Didáticos:** Carregue circuitos pré-programados para observar os fenômenos mais importantes:
    * Superposição
    * Emaranhamento
    * Interferência Quântica
* **Visualização Completa:** Obtenha resultados de simulação em dois formatos:
    * **Contagens de Medição:** Um histograma que mostra os resultados de "experimentos" repetidos, simulando um computador quântico real.
    * **Análise de Estado:** Visualize o estado quântico puro com o "City Plot" e a **Esfera de Bloch** (para 1 qubit).
* **Análise por IA:** Uma seção que analisa automaticamente seus resultados e os explica em linguagem simples, com analogias, para facilitar o aprendizado.

## 🛠️ Tecnologias Utilizadas

Este projeto foi construído com as seguintes tecnologias e bibliotecas:

* **Python:** A linguagem base do projeto.
* **Streamlit:** Para a criação da interface web interativa.
* **Qiskit:** O framework da IBM para computação quântica, usado para criar, simular e visualizar os circuitos.
* **Qiskit Aer:** O motor de simulação de alta performance do Qiskit.
* **NumPy & Matplotlib:** Para manipulação de dados e geração de gráficos.

## 🧠 Principais Conceitos Explorados

* **Qubit:** A unidade fundamental da informação quântica.
* **Superposição:** A capacidade de um qubit existir em múltiplos estados (`|0⟩` e `|1⟩`) simultaneamente.
* **Emaranhamento:** O fenômeno onde múltiplos qubits se tornam interligados de uma forma que seus destinos são dependentes um do outro, independentemente da distância.
* **Medição Quântica:** O processo de observar um qubit, que o força a "colapsar" para um dos estados clássicos (0 ou 1).
* **Interferência Quântica:** O mecanismo pelo qual as probabilidades de certos resultados são aumentadas (construtiva) ou diminuídas/canceladas (destrutiva), sendo a chave para a vantagem dos algoritmos quânticos.

## 🚀 Começando

Para executar este projeto localmente, siga os passos abaixo.

### Pré-requisitos

Você precisa ter o Python 3.8+ e o pip instalados na sua máquina.

### Instalação e Execução

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/](https://github.com/)<SEU-NOME-DE-USUARIO>/laboratorio-quantico-streamlit.git
    ```
2.  **Navegue até a pasta do projeto:**
    ```bash
    cd laboratorio-quantico-streamlit
    ```
3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Execute o aplicativo Streamlit:**
    ```bash
    streamlit run quantum_app.py
    ```
    Seu navegador abrirá automaticamente com o aplicativo em execução!

## 🕹️ Como Usar

1.  **Use os Circuitos de Exemplo:** A forma mais fácil de começar. Selecione um teste na barra lateral e clique em "Carregar" para ver um circuito famoso em ação.
2.  **Construa Manualmente:** Use a seção "Construtor Manual" para criar seus próprios circuitos. Selecione o número de qubits, adicione portas lógicas (`H`, `X`, `CNOT`...) e, **como passo final**, adicione as operações de medição.
3.  **Execute e Analise:** Use os botões na área principal para "Executar Medições" ou "Calcular Vetor de Estado" e veja os resultados aparecerem, junto com a análise explicativa da IA.

## 🌟 Futuras Melhorias

* [ ] Adicionar mais portas quânticas (SWAP, Toffoli, etc.).
* [ ] Permitir salvar e carregar circuitos construídos manualmente.
* [ ] Integrar com hardware quântico real através do IBM Quantum Experience.
* [ ] Criar um "modo desafio", onde o usuário precisa construir um circuito para atingir um estado final específico.

## 🤝 Contribuição

Contribuições são o que tornam a comunidade de código aberto um lugar incrível para aprender, inspirar e criar. Qualquer contribuição que você fizer será **muito bem-vinda**.

1.  Faça um Fork do projeto
2.  Crie sua Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Faça um Commit de suas alterações (`git commit -m 'Add some AmazingFeature'`)
4.  Faça um Push para a Branch (`git push origin feature/AmazingFeature`)
5.  Abra um Pull Request

## 📜 Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.

## 📬 Contato

Seu Nome - [@SeuTwitter](https://twitter.com/SeuTwitter) - seuemail@exemplo.com

Link do Projeto: [https://github.com/<SEU-NOME-DE-USUARIO>/laboratorio-quantico-streamlit](https://github.com/<SEU-NOME-DE-USUARIO>/laboratorio-quantico-streamlit)
