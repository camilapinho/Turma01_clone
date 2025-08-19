from model.contamodel import ContaAtivo, ContaPassivo 
from model.database import get_connection 
 
class ContaController: 
    def __init__(self, view): 
        self.view = view 
        self._conectar_sinais() 
        self.atualizar_lista_contas() 
 
    def _conectar_sinais(self): 
        self.view.btn_criar_conta.clicked.connect(self.criar_conta) 
        self.view.btn_creditar.clicked.connect(self.creditar_conta) 
        self.view.btn_debitar.clicked.connect(self.debitar_conta) 
        self.view.btn_atualizar.clicked.connect(self.atualizar_lista_saldos) 
 
    def criar_conta(self): 
        nome = self.view.input_nome_conta.text().strip() 
        tipo = self.view.combo_tipo_conta.currentText().upper() 
 
        if not nome: 
            self.view.mostrar_mensagem("Digite o nome da conta.") 
            return 
 
        # Código gerado automaticamente baseado no próximo ID 
        conn = get_connection() 
        cur = conn.cursor() 
        cur.execute("SELECT MAX(id) FROM contas") 
        max_id = cur.fetchone()[0] or 0 
        conn.close() 
 
        codigo = f"C{max_id + 1:03d}" 
 
        if tipo == "ATIVO": 
            ContaAtivo(codigo, nome, tipo) 
        else: 
            ContaPassivo(codigo, nome, tipo) 
 
        self.view.mostrar_mensagem(f"Conta '{nome}' criada com sucesso!") 
        self.view.limpar_campos() 
        self.atualizar_lista_contas() 
 
    def atualizar_lista_contas(self): 
        conn = get_connection() 
        cur = conn.cursor() 
        cur.execute("SELECT nome FROM contas") 
        contas = [row[0] for row in cur.fetchall()] 
        conn.close() 
 
        self.view.combo_contas.clear() 
        self.view.combo_contas.addItems(contas) 
 
    def _buscar_conta(self, nome): 
        conn = get_connection() 
        cur = conn.cursor() 
        cur.execute("SELECT codigo, nome, tipo FROM contas WHERE nome = ?", (nome,)) 
        row = cur.fetchone() 
        conn.close() 
        if not row: 
            return None 
        codigo, nome, tipo = row 
        if tipo == "ATIVO": 
            return ContaAtivo(codigo, nome, tipo) 
        else: 
            return ContaPassivo(codigo, nome, tipo) 
 
    def creditar_conta(self): 
        conta_nome = self.view.combo_contas.currentText() 
        valor = self.view.obter_valor() 
        if valor is None: 
            return 
 
        conta = self._buscar_conta(conta_nome) 
        if conta: 
            conta.creditar(valor) 
            self.view.mostrar_mensagem(f"Valor creditado na conta '{conta_nome}'.") 
            self.atualizar_lista_saldos() 
 
    def debitar_conta(self): 
        conta_nome = self.view.combo_contas.currentText() 
        valor = self.view.obter_valor() 
        if valor is None: 
            return 
 
        conta = self._buscar_conta(conta_nome) 
        if conta: 
            conta.debitar(valor) 
            self.view.mostrar_mensagem(f"Valor debitado na conta '{conta_nome}'.") 
            self.atualizar_lista_saldos() 
 
    def atualizar_lista_saldos(self): 
        conn = get_connection() 
        cur = conn.cursor() 
        cur.execute("SELECT nome, saldo FROM contas") 
        contas = cur.fetchall() 
        conn.close() 
 
        self.view.lista_saldos.clear() 
        for nome, saldo in contas: 
            self.view.lista_saldos.addItem(f"{nome}: R$ {saldo:,.2f}")