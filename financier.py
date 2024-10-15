import streamlit as st
from pymongo import MongoClient
import pandas as pd
# Importar o módulo que contém a classe
from fonctions import FormularioContasAPagar
import locale

# Definir o locale para português do Brasil
locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')


# Conexão com Banco ---------------------------------------------------------------
client = MongoClient('mongodb://localhost:27017/')
db = client['ambassador']
# CONTAS A PAGAR ------------------------------------------------------------------
collection_cap = db['comptespayer']
resultado_cap = collection_cap.find()
dados_cap = list(resultado_cap)
df_cap = pd.DataFrame(dados_cap)
#df_cap.drop(columns=['_id'], inplace=True)
df_cap['DataVencimento'] = pd.to_datetime(df_cap['DataVencimento'])

df_cap['Ano'] = df_cap['DataVencimento'].dt.strftime('%Y')
df_cap['Mês'] = df_cap['DataVencimento'].dt.strftime('%b')
df_cap['Mês/Ano'] = df_cap['Mês'] + df_cap['DataVencimento'].dt.strftime('/%Y') 
df_cap['DataVencimento'] = df_cap['DataVencimento'].dt.date



# DIMENSSÕES:
# Natureza da Operação
collection_NatOp = db['dNatOp']
resultado_NatOp = collection_NatOp.find({}, {"NaturezaOperacao": 1, "_id": 0})
dados_NatOp = list(resultado_NatOp)
df_NatOp = pd.DataFrame(dados_NatOp)
lista_NatOp = df_NatOp['NaturezaOperacao'].unique().tolist()


# --------------------------------------------------------------------------------

st.set_page_config(page_title='Condomínio Ambassador', page_icon='🪙', layout='wide')

st.header("🪙 Financeiro Condomínio Ambassador", divider="rainbow")
st.subheader("Contas a Pagar")

st.subheader("Filtros")
fil1,fil2,fil3,fil4,fil5,fil6 = st.columns(6)
with fil1:
    with st.expander("Nro. Título", expanded=False):
        with st.form("form_filtro"):
            filtro_id = st.text_input("Nro.")
            # Botão de submissão do formulário
            submittedFil = st.form_submit_button("Pesquisar")
            if submittedFil:
                df_filtrado = df_cap[df_cap['NroTítulo'] == filtro_id]
                df_cap = pd.DataFrame(df_filtrado)
with fil2:
    with st.expander("Data", expanded=False):
        with st.form("form_dtvenc"):
            data_venc = st.date_input("Data de Vencimento", pd.Timestamp.now().date())
            submittedFi2 = st.form_submit_button("Pesquisar")
            if submittedFi2:
                df_filtrado = df_cap[df_cap['DataVencimento'] == data_venc]
                df_cap = pd.DataFrame(df_filtrado)   
with fil3:
    with st.expander("Mês/Ano", expanded=False):
        with st.form("form_mes_ano"):
            mes_ano = st.selectbox("Mês/Ano", df_cap['Mês/Ano'].unique(), placeholder="Selecione...")
            submittedFi3 = st.form_submit_button("Pesquisar")
            if submittedFi3:
                df_filtrado = df_cap[df_cap['Mês/Ano'] == mes_ano]
                df_cap = pd.DataFrame(df_filtrado)  
with fil4:
    with st.expander("Mês e Ano", expanded=False):
        with st.form("form_mesano"):
            ano = st.selectbox("Ano", df_cap['Ano'].unique(), placeholder="Selecione...")
            mes = st.selectbox("Mês", df_cap['Mês'].unique(), placeholder="Selecione...")
            submittedFi4 = st.form_submit_button("Pesquisar")
            if submittedFi4:
                df_filtrado = df_cap[(df_cap['Ano'] == ano) & (df_cap['Mês'] == mes)]
                df_cap = pd.DataFrame(df_filtrado)
with fil5:
    with st.expander("Status", expanded=False):
        with st.form("form_Status"):
            status = st.radio("Status", ["Pago", "Programado", "Pendente", "Cancelado"],index=None)
            submittedFi5 = st.form_submit_button("Pesquisar")
            if submittedFi5:
                df_filtrado = df_cap[df_cap['Status'] == status]
                df_cap = pd.DataFrame(df_filtrado) 
with fil6:
    with st.expander("Natureza da Operação", expanded=False):
        with st.form("form_Natop"):
            nat_op = st.selectbox("NaturezaOperacao", df_cap['NaturezaOperacao'].unique(), placeholder="Selecione...")
            submittedFi6 = st.form_submit_button("Pesquisar")
            if submittedFi6:
                df_filtrado = df_cap[df_cap['NaturezaOperacao'] == nat_op]
                df_cap = pd.DataFrame(df_filtrado)  

st.divider()
col1, col2, col3 = st.columns(3)         
with col1:
    with st.expander("Cadastro de contas a pagar", expanded=False):
        form_cap = FormularioContasAPagar(collection_cap, lista_NatOp)
        form_cap.exibir_formulario()
with col2:
    with st.expander("Atualizar Registro", expanded=False):
        with st.form("form_att"):
            atualizacao = st.radio("Status", ["Pago", "Programado", "Pendente", "Cancelado"],index=None)
            # Botão de submissão do formulário
            submitted2 = st.form_submit_button("Atualizar")

            if submitted2:
                resultado2 = collection_cap.find_one_and_update({'Fornecedor': "Raju", 'NroTítulo':""},
                                {'$set': {"Status": atualizacao}})
                st.rerun()
with col3:
    st.write("Col3")    

# Exibindo os dados no Data Editor para edição da coluna 'Status'
df_editado = st.data_editor(df_cap, num_rows="dynamic")

# Botão para enviar as alterações para o MongoDB
if st.button("Atualizar Status no MongoDB"):
    # Iterar sobre o DataFrame editado e atualizar o MongoDB
    for index, row in df_editado.iterrows():
        novo_status = row['Status']
        _id = df_cap.loc[index, '_id']  # Supondo que você tenha uma coluna '_id' como chave primária

        # Atualizar o campo 'Status' no MongoDB
        collection_cap.update_one({'_id': _id}, {'$set': {'Status': novo_status}})