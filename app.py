import streamlit as st
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.visualization import plot_bloch_multivector, plot_histogram
import numpy as np

# --- Funções Auxiliares para Visualização e Simulação ---

def get_bloch_sphere(circuit):
    """Retorna a esfera de Bloch para o estado final de um circuito de 1 qubit."""
    simulator = Aer.get_backend('statevector_simulator')
    job = simulator.run(circuit)
    result = job.result()
    statevector = result.get_statevector()
    fig = plot_bloch_multivector(statevector)
    return fig

def get_state_probabilities(circuit, num_qubits):
    """Retorna as probabilidades de medição para um circuito, adequado para 1 ou 2 qubits."""
    simulator = Aer.get_backend('qasm_simulator')
    # Adiciona medições para todos os qubits
    qc_measure = circuit.copy()
    if num_qubits == 1:
        qc_measure.measure(0, 0)
    else:
        qc_measure.measure([0, 1], [0, 1])

    transpiled_circuit = transpile(qc_measure, simulator)
    job = simulator.run(transpiled_circuit, shots=1024)
    result = job.result()
    counts = result.get_counts(qc_measure)

    # Garante que todos os estados possíveis estejam no dicionário para a visualização
    all_possible_states = [format(i, '0' + str(num_qubits) + 'b') for i in range(2**num_qubits)]
    full_counts = {state: counts.get(state, 0) for state in all_possible_states}

    fig = plot_histogram(full_counts, title="Probabilidades de Medição")
    return fig

def initialize_circuit(num_qubits):
    """Inicializa ou reinicia o circuito com o número especificado de qubits."""
    st.session_state.qc = QuantumCircuit(num_qubits, num_qubits) # Medição para todos os qubits
    st.session_state.history = [] # Limpa o histórico de operações
    st.success(f"Circuito reiniciado com {num_qubits} qubit(s) no estado |0...0⟩.")

# --- Interface Streamlit ---

st.set_page_config(layout="wide")
st.title("CirQuant: Explorando Portas Quânticas e Entrelaçamento")

st.markdown("""
Bem-vindo ao **CirQuant**! Esta aplicação interativa permite que você visualize o impacto das portas quânticas em qubits e entenda o fenômeno do entrelaçamento de forma simples.
""")

st.sidebar.header("Configurações do Circuito")
num_qubits = st.sidebar.slider("Número de Qubits", 1, 2, 1, key="num_qubits_slider")

# Inicializa o circuito na primeira vez ou se o número de qubits mudar
if 'qc' not in st.session_state or st.session_state.qc.num_qubits != num_qubits:
    initialize_circuit(num_qubits)

if st.sidebar.button("Reiniciar Circuito"):
    initialize_circuit(num_qubits)

# --- Seção Principal de Simulação e Visualização ---
st.header("Simulador de Circuito Quântico")

col_circuit, col_viz = st.columns([1, 2]) # Ajusta a largura das colunas

with col_circuit:
    st.subheader("Controles do Circuito")

    st.markdown("### Aplique Portas:")
    if num_qubits == 1:
        if st.button("H (Hadamard)", help="Cria superposição."):
            st.session_state.qc.h(0)
            st.session_state.history.append("H(0)")
        if st.button("X (Pauli-X/NOT)", help="Vira o estado (0 para 1, 1 para 0)."):
            st.session_state.qc.x(0)
            st.session_state.history.append("X(0)")
        if st.button("Y (Pauli-Y)", help="Rotação em Y de 180 graus."):
            st.session_state.qc.y(0)
            st.session_state.history.append("Y(0)")
        if st.button("Z (Pauli-Z)", help="Vira a fase se o estado for |1⟩."):
            st.session_state.qc.z(0)
            st.session_state.history.append("Z(0)")

        st.markdown("---")
        st.markdown("#### Portas de Rotação (ângulos em graus):")
        theta_x = st.slider("Ângulo Rx (graus)", 0, 360, 90, key="rx_angle")
        if st.button(f"Rx({theta_x}°)", help="Rotação em torno do eixo X da Esfera de Bloch."):
            st.session_state.qc.rx(np.deg2rad(theta_x), 0)
            st.session_state.history.append(f"Rx({theta_x}°, 0)")
        theta_y = st.slider("Ângulo Ry (graus)", 0, 360, 90, key="ry_angle")
        if st.button(f"Ry({theta_y}°)", help="Rotação em torno do eixo Y da Esfera de Bloch."):
            st.session_state.qc.ry(np.deg2rad(theta_y), 0)
            st.session_state.history.append(f"Ry({theta_y}°, 0)")
        theta_z = st.slider("Ângulo Rz (graus)", 0, 360, 90, key="rz_angle")
        if st.button(f"Rz({theta_z}°)", help="Rotação em torno do eixo Z da Esfera de Bloch."):
            st.session_state.qc.rz(np.deg2rad(theta_z), 0)
            st.session_state.history.append(f"Rz({theta_z}°, 0)")

    elif num_qubits == 2:
        st.markdown("#### Portas de 1 Qubit (Qubit 0):")
        if st.button("H(0)", key="h0_2q"): st.session_state.qc.h(0); st.session_state.history.append("H(0)")
        if st.button("X(0)", key="x0_2q"): st.session_state.qc.x(0); st.session_state.history.append("X(0)")
        st.markdown("#### Portas de 1 Qubit (Qubit 1):")
        if st.button("H(1)", key="h1_2q"): st.session_state.qc.h(1); st.session_state.history.append("H(1)")
        if st.button("X(1)", key="x1_2q"): st.session_state.qc.x(1); st.session_state.history.append("X(1)")

        st.markdown("---")
        st.markdown("### Portas de 2 Qubits:")
        if st.button("CNOT (0, 1)", help="Controla o Qubit 1 com o Qubit 0."):
            st.session_state.qc.cx(0, 1)
            st.session_state.history.append("CNOT(0,1)")
        if st.button("SWAP (0, 1)", help="Troca os estados dos qubits 0 e 1."):
            st.session_state.qc.swap(0, 1)
            st.session_state.history.append("SWAP(0,1)")

    st.markdown("### Circuitos Pré-definidos:")
    selected_preset = st.selectbox(
        "Selecione um circuito:",
        ["Nenhum", "Estado Bell", "Teletransporte Quântico", "Gerador de Bits Aleatórios (Qubit 0)"]
    )

    if selected_preset == "Estado Bell" and num_qubits == 2:
        if st.button("Carregar Estado Bell"):
            initialize_circuit(2) # Reinicia para garantir um estado limpo
            st.session_state.qc.h(0)
            st.session_state.qc.cx(0, 1)
            st.session_state.history = ["H(0)", "CNOT(0,1)"]
            st.success("Circuito de Estado Bell carregado!")
    elif selected_preset == "Teletransporte Quântico" and num_qubits == 2:
        if st.button("Carregar Teletransporte"):
            st.error("O teletransporte quântico, como um processo completo, geralmente requer 3 qubits e medição. Esta é uma versão simplificada para 2 qubits onde o 'teletransporte' é mais sobre a correlação de estados.")
            initialize_circuit(2)
            # Para simular o teletransporte com 2 qubits (Alice e Bob),
            # precisamos simular a preparação de um estado a ser teletransportado por Alice
            # e o par emaranhado. Aqui faremos uma versão mais ilustrativa.
            # Qubit 0 = Qubit a ser teletransportado (Alice)
            # Qubit 1 = Qubit do par emaranhado (Alice)
            # Qubit 2 = Qubit do par emaranhado (Bob)
            # Como temos apenas 2 qubits, faremos uma simplificação.
            # O estado que Alice quer teletransportar é o Qubit 0
            # O estado do par emaranhado que Bob tem é o Qubit 1
            # Para visualizar o conceito, criamos um estado emaranhado entre Q0 e Q1,
            # onde Q0 seria o qubit de Alice e Q1 de Bob
            st.session_state.qc.h(0) # Suponha que Alice quer teletransportar |+>
            st.session_state.qc.cx(0, 1) # Isto cria um par emaranhado entre Q0 e Q1
            st.session_state.qc.h(0) # Alice aplica H no seu qubit
            st.session_state.qc.cx(0,1) # Alice aplica CNOT em seu qubit e Bob (Q1)
            # Para simular o 'teletransporte', Alice teria que medir seus qubits
            # e Bob aplicaria correções. A visualização abaixo mostrará o estado final
            # antes das medições e correções de Bob, que não são diretamente implementadas aqui.
            st.session_state.history = ["H(0)", "CNOT(0,1)", "H(0)", "CNOT(0,1) (Simulação Teletransporte)"]
            st.success("Circuito de Teletransporte Quântico (simplificado) carregado!")
    elif selected_preset == "Gerador de Bits Aleatórios (Qubit 0)" and num_qubits == 1:
        if st.button("Carregar Gerador de Bits Aleatórios"):
            initialize_circuit(1)
            st.session_state.qc.h(0)
            st.session_state.history = ["H(0)"]
            st.success("Circuito Gerador de Bits Aleatórios carregado!")
    elif selected_preset != "Nenhum":
        st.warning(f"O circuito '{selected_preset}' requer {2 if selected_preset == 'Estado Bell' or selected_preset == 'Teletransporte Quântico' else 1} qubit(s). Por favor, ajuste o slider.")


with col_viz:
    st.subheader("Visualização do Estado do Qubit")
    st.text("Histórico de Operações: " + " -> ".join(st.session_state.history))

    if num_qubits == 1:
        fig_bloch = get_bloch_sphere(st.session_state.qc)
        st.pyplot(fig_bloch)
        st.markdown("""
        A **Esfera de Bloch** representa o estado de um único qubit.
        Os pólos Norte e Sul correspondem aos estados $|0⟩$ e $|1⟩$, respectivamente.
        Pontos na superfície são superposições.
        """)
        fig_hist = get_state_probabilities(st.session_state.qc, num_qubits)
        st.pyplot(fig_hist)
    elif num_qubits == 2:
        # Para 2 qubits, a esfera de Bloch não é aplicável diretamente.
        # Mostramos o circuito e as probabilidades.
        st.pyplot(st.session_state.qc.draw(output='mpl'))
        st.markdown("Acima está a representação do seu circuito quântico.")
        fig_hist_2q = get_state_probabilities(st.session_state.qc, num_qubits)
        st.pyplot(fig_hist_2q)
        st.markdown("""
        Para 2 qubits, as probabilidades de medição mostram a chance de cada combinação (00, 01, 10, 11).
        No **entrelaçamento**, certas combinações terão probabilidades muito altas, enquanto outras serão nulas.
        """)

# --- Seção de Explicações Detalhadas ---
st.markdown("---")
st.header("Conceitos e Portas Quânticas: Entenda o CirQuant")

st.markdown("### O que é um Qubit?")
st.markdown("""
Ao contrário do **bit clássico**, que pode ser 0 ou 1, um **qubit** (quantum bit) pode ser 0, 1, ou uma **superposição** de ambos.
Imagine um ponto em uma esfera: ele pode estar no polo norte (0), no polo sul (1), ou em qualquer lugar na superfície (superposição de 0 e 1).
Quando medimos um qubit em superposição, ele "colapsa" para 0 ou 1 com uma certa probabilidade.
""")

st.markdown("### O que são Portas Quânticas?")
st.markdown("""
Portas quânticas são operações que modificam o estado de um ou mais qubits. Elas são análogas às portas lógicas clássicas (AND, OR, NOT), mas operam em estados quânticos.
""")

st.markdown("#### Principais Portas de 1 Qubit:")
st.markdown("""
* **Porta Hadamard (H):** É a porta mais famosa para criar **superposição**. Se um qubit está em $|0⟩$, a porta H o coloca em um estado onde ele tem 50% de chance de ser 0 e 50% de chance de ser 1 ao ser medido. É como girar a Esfera de Bloch em 90 graus em torno do eixo Y e depois 180 graus em torno do eixo X.
* **Porta Pauli-X (X):** Funciona como um **NOT** clássico. Se o qubit está em $|0⟩$, vira para $|1⟩$; se está em $|1⟩$, vira para $|0⟩$. Na Esfera de Bloch, é uma rotação de 180 graus em torno do eixo X.
* **Porta Pauli-Y (Y):** Similar à X, mas com uma mudança de fase adicional. Rotaciona o qubit em 180 graus em torno do eixo Y da Esfera de Bloch.
* **Porta Pauli-Z (Z):** Não muda o estado de 0 ou 1 diretamente, mas inverte a **fase** do estado $|1⟩$. Na Esfera de Bloch, é uma rotação de 180 graus em torno do eixo Z.
* **Portas de Rotação (Rx, Ry, Rz):** Permitem rotações arbitrárias em torno dos eixos X, Y e Z da Esfera de Bloch, respectivamente. O ângulo de rotação é especificado.
""")

st.markdown("#### Principais Portas de 2 Qubits:")
st.markdown("""
* **Porta CNOT (Controlled-NOT):** Esta porta tem um **qubit de controle** e um **qubit alvo**. Se o qubit de controle é $|1⟩$, a porta aplica uma operação NOT no qubit alvo. Se o qubit de controle é $|0⟩$, nada acontece ao qubit alvo. É essencial para criar **entrelaçamento**.
* **Porta SWAP:** Troca os estados de dois qubits. Se o Qubit 0 está em $|0⟩$ e o Qubit 1 em $|1⟩$, após a porta SWAP, o Qubit 0 estará em $|1⟩$ e o Qubit 1 em $|0⟩$.
""")

st.markdown("### O que é Entrelaçamento (Entanglement)?")
st.markdown("""
O entrelaçamento é um dos conceitos mais fascinantes e estranhos da mecânica quântica.
Quando dois qubits estão **entrelaçados**, o estado de um qubit depende instantaneamente do estado do outro, mesmo que eles estejam separados por grandes distâncias.
Se você medir um qubit entrelaçado e ele for 0, você sabe instantaneamente que o outro qubit entrelaçado também será 0 (ou 1, dependendo de como foram entrelaçados), sem precisar medi-lo diretamente.
Um **estado Bell**, por exemplo, é um par de qubits entrelaçados onde as medições sempre darão resultados correlacionados (00 ou 11, mas nunca 01 ou 10).
""")

st.markdown("---")
st.sidebar.header("Para saber mais:")
st.sidebar.markdown("""
* [Qiskit Documentation](https://qiskit.org/documentation/)
* [IBM Quantum Experience](https://quantum.ibm.com/)
* [Vídeos explicativos sobre computação quântica](https://www.youtube.com/results?search_query=computacao+quantica+explicada)
""")