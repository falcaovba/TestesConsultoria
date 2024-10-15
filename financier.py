import streamlit as st
from pymongo import MongoClient
import pandas as pd
# Importar o módulo que contém a classe
from fonctions import FormularioContasAPagar

from pymongo import ReturnDocument

# Conexão com Banco ---------------------------------------------------------------
#client = MongoClient('mongodb://192.168.1.15:27017/')
#client = MongoClient('mongodb://localhost:27017/')
db = client['ambassador']
# CONTAS A PAGAR ------------------------------------------------------------------
collection_cap = db['comptespayer']
resultado_cap = collection_cap.find()
dados_cap = list(resultado_cap)
df_cap = pd.DataFrame(dados_cap)
df_cap.drop(columns=['_id'], inplace=True)
df_cap['DataVencimento'] = pd.to_datetime(df_cap['DataVencimento'])
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



filtro1, col1, col2, col3 = st.columns(4)
with filtro1:
    st.write("Filtro")
with col1:
    with st.expander("Cadastro de contas a pagar", expanded=False):
        form_cap = FormularioContasAPagar(collection_cap, lista_NatOp)
        form_cap.exibir_formulario()
with col2:
    st.write("Col2")
    resultado2 = collection_cap.find_one_and_update({'name': "Raju"},
                            {'$set': {"Branch": 'ECE'}},
                            return_document=ReturnDocument.AFTER)
with col3:
    st.write("Col3")

st.dataframe(df_cap)
