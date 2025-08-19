from PyQt5.QtWidgets import ( 
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, 
    QComboBox, QMessageBox, QTabWidget, QListWidget, QFormLayout 
) 
 
class MainView(QWidget): 
    def __init__(self): 
        super().__init__() 
        self.setWindowTitle("Sistema Contábil Expandido") 
        self.resize(400, 300) 
        self.init_ui() 
 
    def init_ui(self): 
        self.tabs = QTabWidget() 
 
        # ----- Aba 1: Cadastro e Movimentações ----- 
        self.tab_operacoes = QWidget() 
        layout1 = QVBoxLayout() 
 
        # Cadastro de conta 
        self.input_nome_conta = QLineEdit() 
        self.combo_tipo_conta = QComboBox() 
        self.combo_tipo_conta.addItems(["Ativo", "Passivo"]) 
        self.btn_criar_conta = QPushButton("Criar Conta") 
 
        layout_cadastro = QFormLayout() 
        layout_cadastro.addRow("Nome da Conta:", self.input_nome_conta) 
        layout_cadastro.addRow("Tipo de Conta:", self.combo_tipo_conta) 
        layout_cadastro.addWidget(self.btn_criar_conta) 
 
        # Operações 
        self.combo_contas = QComboBox() 
        self.input_valor = QLineEdit() 
        self.btn_creditar = QPushButton("Creditar") 
        self.btn_debitar = QPushButton("Debitar") 
 
        layout_operacao = QFormLayout() 
        layout_operacao.addRow("Selecionar Conta:", self.combo_contas) 
        layout_operacao.addRow("Valor:", self.input_valor) 
        layout_operacao.addRow(self.btn_creditar, self.btn_debitar) 
 
        layout1.addLayout(layout_cadastro) 
        layout1.addSpacing(20) 
        layout1.addLayout(layout_operacao) 
        self.tab_operacoes.setLayout(layout1) 
 
        # ----- Aba 2: Consulta ----- 
        self.tab_consulta = QWidget() 
        layout2 = QVBoxLayout() 
        self.lista_saldos = QListWidget() 
        self.btn_atualizar = QPushButton("Atualizar Saldos") 
        layout2.addWidget(self.lista_saldos) 
        layout2.addWidget(self.btn_atualizar) 
        self.tab_consulta.setLayout(layout2) 
 
        self.tabs.addTab(self.tab_operacoes, "Operações") 
        self.tabs.addTab(self.tab_consulta, "Saldos") 
 
        main_layout = QVBoxLayout() 
        main_layout.addWidget(self.tabs) 
        self.setLayout(main_layout) 
 
    def mostrar_mensagem(self, texto): 
        QMessageBox.information(self, "Info", texto) 
 
    def limpar_campos(self): 
        self.input_nome_conta.clear() 
        self.input_valor.clear() 
 
    def obter_valor(self): 
        try: 
            valor = float(self.input_valor.text()) 
            self.input_valor.clear() 
            return valor 
        except ValueError: 
            self.mostrar_mensagem("Digite um valor válido.") 
            return None