from model.database import get_connection 
 
class ContaContabil: 
    def __init__(self, codigo, nome, tipo): 
        self.codigo = codigo 
        self.nome = nome 
        self.tipo = tipo 
        self.id = self._get_or_create_conta() 
 
    def _get_or_create_conta(self): 
        conn = get_connection() 
        cur = conn.cursor() 
        cur.execute("SELECT id FROM contas WHERE codigo = ?", (self.codigo,)) 
        row = cur.fetchone() 
        if row: 
            conta_id = row[0] 
        else: 
            cur.execute(""" 
                INSERT INTO contas (codigo, nome, tipo, saldo) 
                VALUES (?, ?, ?, 0) 
            """, (self.codigo, self.nome, self.tipo)) 
            conn.commit() 
            conta_id = cur.lastrowid 
        conn.close() 
        return conta_id 
 
    def creditar(self, valor): 
        conn = get_connection() 
        cur = conn.cursor() 
        cur.execute("UPDATE contas SET saldo = saldo + ? WHERE id = ?", (valor, self.id)) 
        cur.execute(""" 
            INSERT INTO transacoes (conta_id, tipo, valor, data) 
            VALUES (?, 'CREDITO', ?, datetime('now')) 
        """, (self.id, valor)) 
        conn.commit() 
        conn.close() 
 
    def debitar(self, valor): 
        raise NotImplementedError 
 
    def exibir_saldo(self): 
        conn = get_connection() 
        cur = conn.cursor() 
        cur.execute("SELECT saldo FROM contas WHERE id = ?", (self.id,)) 
        saldo = cur.fetchone()[0] 
        conn.close() 
        return saldo 
 
 
class ContaAtivo(ContaContabil): 
    def debitar(self, valor): 
        conn = get_connection() 
        cur = conn.cursor() 
        cur.execute("UPDATE contas SET saldo = saldo - ? WHERE id = ?", (valor, self.id)) 
        cur.execute(""" 
            INSERT INTO transacoes (conta_id, tipo, valor, data) 
            VALUES (?, 'DEBITO', ?, datetime('now')) 
        """, (self.id, valor)) 
        conn.commit() 
        conn.close() 
 
 
class ContaPassivo(ContaContabil): 
    def debitar(self, valor): 
        conn = get_connection() 
        cur = conn.cursor() 
        cur.execute("UPDATE contas SET saldo = saldo + ? WHERE id = ?", (valor, self.id)) 
        cur.execute(""" 
            INSERT INTO transacoes (conta_id, tipo, valor, data) 
            VALUES (?, 'DEBITO', ?, datetime('now')) 
        """, (self.id, valor)) 
        conn.commit() 
        conn.close() 