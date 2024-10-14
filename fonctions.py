import streamlit as st
import pandas as pd

class FormularioContasAPagar:
    def __init__(self, collection_cap, lista_NatOp):
        self.collection_cap = collection_cap
        self.lista_NatOp = lista_NatOp

    def exibir_formulario(self):
        with st.form("form_cap"):
            st.write("Cadastro de contas a pagar")

            # Inputs do formulário
            data_venc = st.date_input("Data de Vencimento", pd.Timestamp.now().date())
            banco = st.selectbox("Banco", ("ASAAS", "INTER", "ITAÚ"), placeholder="Selecione o banco...")
            nro_doc = st.text_input("Nro do Título", "NF Nro.")
            fornecedor = st.text_input("Fornecedor")
            nat_operacao = st.selectbox("Operação", self.lista_NatOp, placeholder="Selecione a natureza...")
            tipo_pgto = st.selectbox("Tipo de Pagamento", ("PIX", "Boleto", "Cartão Crédito", "Cartão Débito", "Transferência", "Dinheiro"), placeholder="Selecione o método de pagamento...")
            status = st.selectbox("Status", ("Pago", "Programado", "Pendente", "Cancelado"), placeholder="Informe o status...")
            valor = st.number_input("Valor", min_value=0.0, step=0.01, format="%.2f", placeholder="Inserir o valor do documento...")
            observacao = st.text_input("Observação")

            # Dicionário com os dados preenchidos
            novo_documento = {
                "DataVencimento": data_venc.isoformat(),  # Converter a data para formato ISO (YYYY-MM-DD)
                "Banco": banco,
                "NroTítulo": nro_doc,
                "Fornecedor": fornecedor,
                "NaturezaOperacao": nat_operacao,
                "TipoPagamento": tipo_pgto,
                "Status": status,
                "Valor": valor,
                "Observacoes": observacao
            }

            # Botão de submissão do formulário
            submitted = st.form_submit_button("Registrar")

            if submitted:
                # Exemplo de operação com banco de dados fictício
                resultado = self.collection_cap.insert_one(novo_documento)
                st.success('Operação salva com sucesso!', icon="✅")
                st.rerun()
