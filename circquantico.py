import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import qiskit
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram, circuit_drawer, plot_state_city, plot_bloch_multivector

# --- CONSTANTE DE VERSÃO ---
APP_VERSION = "v9.1_Fix_Inicializacao"

# --- FUNÇÃO DE ANÁLISE DA IA ---

def interpret_results(counts: dict, num_qubits: int):
    """Analisa o dicionário de contagens e retorna uma explicação detalhada e didática."""
    if not counts: return ""
    total_shots = sum(counts.values())
    interpretation = ""
    # Análise para 1 Qubit
    if num_qubits == 1:
        prob_0 = counts.get('0', 0) / total_shots
        prob_1 = counts.get('1', 0) / total_shots
        if 0.4 < prob_0 < 0.6 and 0.4 < prob_1 < 0.6:
            interpretation = """### Fenômeno Observado: Superposição! 🌌\n* **O que aconteceu?** Você aplicou uma porta Hadamard (`H`), colocando o qubit em uma combinação de 0 e 1 ao mesmo tempo.\n* **O que o gráfico mostra?** Aproximadamente 50% de chance para cada resultado, como uma moeda girando no ar."""
        elif prob_0 > 0.99:
            interpretation = """### Fenômeno Observado: Interferência Destrutiva! 🎯\n* **O que aconteceu?** Provavelmente você aplicou uma porta `H` duas vezes. A segunda desfez a superposição da primeira.\n* **O que o gráfico mostra?** O resultado é sempre 0. A 'chance' de medir 1 foi cancelada, provando que a computação quântica é sobre controle, não aleatoriedade."""
        elif prob_1 > 0.99:
            interpretation = "### Estado Determinístico |1⟩! 🎯\nO resultado é sempre 1. Isso geralmente acontece após a aplicação de uma porta `X` (NOT) em um qubit no estado `|0⟩`."
        else:
            interpretation = "O qubit está em uma superposição com probabilidades desiguais, provavelmente criada por uma porta de rotação como a `RZ`."
    # Análise para 2 Qubits
    elif num_qubits == 2:
        prob_00 = counts.get('00', 0) / total_shots
        prob_11 = counts.get('11', 0) / total_shots
        prob_others = 1 - (prob_00 + prob_11)
        if prob_00 > 0.4 and prob_11 > 0.4 and prob_others < 0.1:
            interpretation = """### Fenômeno Observado: Emaranhamento! 🔗\n* **O que aconteceu?** Você criou um Estado de Bell (`H` + `CNOT`).\n* **O que o gráfico mostra?** Os resultados estão perfeitamente correlacionados: só aparecem `00` e `11`. Medir um qubit afeta instantaneamente o outro, não importa a distância."""
        else:
            interpretation = "Os resultados mostram uma distribuição de probabilidades entre os quatro possíveis estados finais do seu circuito de 2 qubits."
    return interpretation

# --- FUNÇÕES DE BACKEND (Estáveis) ---

def run_measurement_simulation(qc: QuantumCircuit, shots: int):
    try:
        if qc.num_clbits == 0 or not any(instr.operation.name == 'measure' for instr in qc.data):
            st.warning("Para ver as contagens, adicione operações de 'Medir' ao seu circuito."); return None
        simulator = AerSimulator(); result = simulator.run(transpile(qc, simulator), shots=shots).result(); return result.get_counts()
    except Exception as e:
        st.error(f"Erro na Simulação de Medição: {e}"); return None

def calculate_statevector(qc: QuantumCircuit):
    try:
        sv_qc = qc.copy(); sv_qc.data = [gate for gate in sv_qc.data if gate.operation.name != 'measure']
        simulator = AerSimulator(method='statevector'); sv_qc.save_statevector(); result = simulator.run(transpile(sv_qc, simulator)).result(); return result.get_statevector()
    except Exception as e:
        st.error(f"Erro no Cálculo do Vetor de Estado: {e}"); return None

# --- FUNÇÕES DA INTERFACE (FRONTEND) ---

def initialize_app_state():
    """Inicializa as variáveis da sessão se elas não existirem."""
    if 'num_qubits' not in st.session_state:
        st.session_state.num_qubits = 1
    if 'circuit' not in st.session_state or st.session_state.circuit.num_qubits != st.session_state.num_qubits:
        force_reset_circuit(show_toast=False) # Não mostra o toast na primeira carga

def force_reset_circuit(show_toast=True):
    """Força a limpeza e recriação do circuito, limpando todos os resultados."""
    num_q = st.session_state.get('num_qubits', 1)
    st.session_state.circuit = QuantumCircuit(num_q, num_q)
    st.session_state.counts = None; st.session_state.statevector = None
    if show_toast:
        st.toast("Circuito resetado!", icon="✨")

def setup_sidebar():
    """Configura e exibe todos os controles na barra lateral."""
    st.sidebar.header("🏗️ Painel de Controle");

    st.sidebar.subheader("🔬 Circuitos de Exemplo")
    example_circuit = st.sidebar.selectbox("Selecione um teste:", ["Nenhum", "Teste 1: Superposição", "Teste 2: Emaranhamento", "Teste 3: Interferência"])
    if st.sidebar.button("Carregar Circuito de Exemplo", use_container_width=True):
        st.session_state.counts = None; st.session_state.statevector = None
        if example_circuit == "Teste 1: Superposição":
            st.session_state.num_qubits = 1; qc = QuantumCircuit(1, 1); qc.h(0); qc.measure(0, 0); st.session_state.circuit = qc
        elif example_circuit == "Teste 2: Emaranhamento":
            st.session_state.num_qubits = 2; qc = QuantumCircuit(2, 2); qc.h(0); qc.cx(0, 1); qc.measure_all(); st.session_state.circuit = qc
        elif example_circuit == "Teste 3: Interferência":
            st.session_state.num_qubits = 1; qc = QuantumCircuit(1, 1); qc.h(0); qc.h(0); qc.measure(0, 0); st.session_state.circuit = qc
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.subheader("🛠️ Construtor Manual")
    
    num_qubits_options = [1, 2, 3, 4]
    new_num_qubits = st.sidebar.selectbox("Número de Qubits:", options=num_qubits_options, index=st.session_state.num_qubits - 1)
    if new_num_qubits != st.session_state.num_qubits:
        st.session_state.num_qubits = new_num_qubits; initialize_app_state(); st.rerun()

    gate_type = st.sidebar.selectbox("Selecione a Operação:", ["H", "X", "Z", "RZ", "CNOT", "Medir Qubit", "Medir Todos"])
    params = {'gate': gate_type}
    qubit_indices = list(range(st.session_state.num_qubits))
    
    if gate_type in ["H", "X", "Z", "RZ", "Medir Qubit"]:
        params['target'] = st.sidebar.selectbox("No Qubit de Índice:", qubit_indices)
    elif gate_type == "CNOT":
        if st.session_state.num_qubits > 1:
            params['control'] = st.sidebar.selectbox("Qubit de Controle (Índice):", qubit_indices)
            target_options = [q for q in qubit_indices if q != params['control']]
            params['target'] = st.sidebar.selectbox("Qubit Alvo (Índice):", target_options) if target_options else None
        else: params = None
    if gate_type == "RZ": params['theta'] = st.sidebar.slider("Ângulo θ (graus):", -180, 180, 0)

    if st.sidebar.button("Adicionar Operação", use_container_width=True) and params:
        qc = st.session_state.circuit
        gate, target = params.get('gate'), params.get('target')
        if gate in ["H", "X", "Z"]: qc.h(target) if gate == "H" else qc.x(target) if gate == "X" else qc.z(target)
        elif gate == "RZ": qc.rz(np.deg2rad(params['theta']), target)
        elif gate == "CNOT" and target is not None: qc.cx(params['control'], target)
        elif gate == "Medir Qubit": qc.measure(target, target)
        elif gate == "Medir Todos": qc.measure_all(inplace=True)
        st.session_state.counts = None; st.session_state.statevector = None
        st.rerun()
        
    st.sidebar.markdown("---")
    if st.sidebar.button("Resetar Circuito", type="primary", use_container_width=True):
        force_reset_circuit(); st.rerun()

def display_main_area():
    st.header("🔷 Diagrama do Circuito"); st.info("Esta é a representação visual do seu programa quântico.", icon="👀")
    fig_circ, ax_circ = plt.subplots(); circuit_drawer(st.session_state.circuit, output='mpl', ax=ax_circ, style={'fold': 25}, initial_state=True); st.pyplot(fig_circ, use_container_width=True)
    
    st.markdown("---"); st.header("🔬 Resultados e Visualizações")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Contagens de Medição")
        if st.button("Executar Medições", use_container_width=True):
            with st.spinner("Executando 1024 'shots'..."): st.session_state.counts = run_measurement_simulation(st.session_state.circuit, 1024)
            st.rerun()
    with col2:
        st.subheader("🧭 Análise de Estado Quântico")
        if st.button("Calcular Vetor de Estado", use_container_width=True):
            with st.spinner("Analisando estado quântico..."): st.session_state.statevector = calculate_statevector(st.session_state.circuit)
            st.rerun()
            
    counts = st.session_state.get('counts'); statevector = st.session_state.get('statevector')
    
    # Exibe os gráficos principais
    if counts: st.pyplot(plot_histogram(counts, title="Resultados da Medição"))
    if statevector is not None:
        if st.session_state.num_qubits > 1: st.pyplot(plot_state_city(statevector, title="Vetor de Estado (City Plot)"))
    
    # Exibe a Esfera de Bloch e a Análise da IA
    analysis_col, bloch_col = st.columns([2, 1])
    with analysis_col:
        if counts:
            st.markdown("---"); st.subheader("🤖 Análise da Medição: O que este resultado significa?")
            st.markdown(interpret_results(counts, st.session_state.num_qubits))
    with bloch_col:
        if st.session_state.num_qubits == 1 and statevector is not None:
            st.subheader("🌐 Esfera de Bloch"); st.pyplot(plot_bloch_multivector(statevector, title=""))

# --- EXECUÇÃO PRINCIPAL DO APP ---
# Este é o bloco que foi corrigido.
st.set_page_config(layout="wide", page_title="Laboratório Quântico Interativo")
st.title("⚛️ Laboratório Quântico Interativo")

# GARANTE que o estado seja inicializado ANTES de qualquer tentativa de desenhar a UI.
initialize_app_state()

# Agora que o estado está garantido, podemos desenhar as seções da página.
setup_sidebar()
display_main_area()