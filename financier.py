import streamlit as st
from pymongo import MongoClient
import pandas as pd
import locale
import altair as alt
from fonctions import style_metric_cards

# Importar o módulo que contém a classe
from fonctions import FormularioContasAPagar

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
df_cap.drop(columns=['_id'], inplace=True)
df_cap['DataVencimento'] = pd.to_datetime(df_cap['DataVencimento'])

#df_cap['Dia'] = df_cap['DataVencimento'].dt.strftime('%d')
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

st.header("🪙 Financeiro Condomínio Ambassador - Contas a Pagar", divider="rainbow")

with st.container(border=True):
    
    st.markdown("""
    <div style='display: flex; align-items: center;'>
        <h3 style='font-size:24px; margin: 0;'>🔍<b>Filtros</b></h3>
        <hr style="flex-grow: 1; border: 2px solid #FF5733; margin-left: 10px;">
    </div> """, unsafe_allow_html=True)
    
    fil1,fil2,fil3,fil4,fil5,fil6,fil = st.columns([1.6,1.3,1.5,1.6,1.3,2,1])
    
    with fil1:
        with st.popover("📜 Nro. Título"): #with st.expander("📜 Nro. Título", expanded=False):
            with st.form("form_filtro"):
                filtro_id = st.text_input("Nro. Título")
                # Botão de submissão do formulário
                submittedFil = st.form_submit_button("🔎 Pesquisar")
                if submittedFil:
                    df_filtrado = df_cap[df_cap['NroTítulo'] == filtro_id]
                    df_cap = pd.DataFrame(df_filtrado)
    with fil2:
        with st.popover("📆 Data"): #with st.expander("📆 Data", expanded=False):
            with st.form("form_dtvenc"):
                data_venc = st.date_input("Data", pd.Timestamp.now().date())
                submittedFi2 = st.form_submit_button("🔎 Pesquisar")
                if submittedFi2:
                    df_filtrado = df_cap[df_cap['DataVencimento'] == data_venc]
                    df_cap = pd.DataFrame(df_filtrado)   
    with fil3:
        with st.popover("📅 Mês/Ano"): #with st.expander("📅 Mês/Ano", expanded=False):
            with st.form("form_mes_ano"):
                mes_ano = st.selectbox("Mês/Ano", df_cap['Mês/Ano'].unique(), placeholder="Selecione...")
                submittedFi3 = st.form_submit_button("🔎 Pesquisar")
                if submittedFi3:
                    df_filtrado = df_cap[df_cap['Mês/Ano'] == mes_ano]
                    df_cap = pd.DataFrame(df_filtrado)  
    with fil4:
        with st.popover("🗓️ Mês e Ano"): #with st.expander("🗓️ Mês e Ano", expanded=False):
            with st.form("form_mesano"):
                ano = st.selectbox("Ano", df_cap['Ano'].unique(), placeholder="Selecione...")
                mes = st.selectbox("Mês", df_cap['Mês'].unique(), placeholder="Selecione...")
                submittedFi4 = st.form_submit_button("🔎 Pesquisar")
                if submittedFi4:
                    df_filtrado = df_cap[(df_cap['Ano'] == ano) & (df_cap['Mês'] == mes)]
                    df_cap = pd.DataFrame(df_filtrado)
    with fil5:
        with st.popover("🔋Status"): #with st.expander("🔋Status", expanded=False):
            with st.form("form_Status"):
                status = st.radio("Status", ["Pago", "Programado", "Pendente", "Cancelado"],index=None)
                submittedFi5 = st.form_submit_button("🔎 Pesquisar")
                if submittedFi5:
                    df_filtrado = df_cap[df_cap['Status'] == status]
                    df_cap = pd.DataFrame(df_filtrado) 
    with fil6:
        with st.popover("💳 Nat. da Op."): #with st.expander("💳 Natureza da Operação", expanded=False):
            with st.form("form_Natop"):
                nat_op = st.selectbox("NaturezaOperacao", df_cap['NaturezaOperacao'].unique(), placeholder="Selecione...")
                submittedFi6 = st.form_submit_button("🔎 Pesquisar")
                if submittedFi6:
                    df_filtrado = df_cap[df_cap['NaturezaOperacao'] == nat_op]
                    df_cap = pd.DataFrame(df_filtrado)  
# -------------------------------------------------------------------------------------------------------------------------------------

tab1, tab2 = st.tabs(["Registros", "Análises"])

with tab1:
    st.markdown("""
    <div style='display: flex; align-items: center;'>
        <h3 style='font-size:24px; margin: 0;'> 🪪 <b>Registros </b></h3>
        <hr style="flex-grow: 1; border: 2px solid #FF5733; margin-left: 10px;">
    </div> """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1.3,2,5])         
    
    with col1:
        with st.popover("➕ Novo Registro"): #with st.expander("➕ Novo Registro", expanded=False):
            form_cap = FormularioContasAPagar(collection_cap, lista_NatOp)
            form_cap.exibir_formulario()
    with col2:
        with st.popover("♻️ Atualizar Registro"): #with st.expander("♻️ Atualizar Registro", expanded=False):
            with st.form("form_att"):
                nrotitulo_at = st.text_input("Nro Título")
                fornec = st.text_input("Fornecedor")
                data_vencm = st.date_input("Data de Vencimento", pd.Timestamp.now().date())
                atualizacao = st.radio("Status", ["Pago", "Programado", "Pendente", "Cancelado","Excluir"],index=None)
                # Botão de submissão do formulário
                submitted2 = st.form_submit_button("Atualizar")

                if submitted2:
                    resultado2 = collection_cap.update_one({'NroTítulo': nrotitulo_at, 'Fornecedor': fornec},{'$set': {"Status": atualizacao}})
                    st.rerun()

    # DATAFRAME
    df_cap = df_cap[df_cap['Status'] != "Excluir"]   
    st.dataframe(df_cap, hide_index=True)
#--------------------------------------------------------------------------------------------------------
with tab2:
    st.markdown("""
    <div style='display: flex; align-items: center;'>
        <h3 style='font-size:24px; margin: 0;'> 📊 <b>Análises</b></h3>
        <hr style="flex-grow: 1; border: 2px solid #FF5733; margin-left: 10px;">
    </div> """, unsafe_allow_html=True)
    #with st.container(border=True):

    graf1, graf2, graf3  = st.columns(3)
    
    with graf1:    
# CARD ------------------------------------------------------------------------------------------------------------------------------------------------------
        # Calcular o somatório dos valores
        total_valor = df_cap['Valor'].sum()
        # Formatar o total para o formato de reais (com separador de milhar e vírgula para decimais)
        total_valor_formatado = f"R$ {total_valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        
        st.metric(label="💲Total a Pagar", value=total_valor_formatado)
        style_metric_cards()
        st.markdown("""
                    
                    """)
# BANCO ---------------------------------------------------------------------------------------------------------------------------------------------------
        df_agg_banco = df_cap.groupby(['Banco'])['Valor'].sum().reset_index()
        df_agg_banco_res = df_agg_banco.sort_values(by='Valor', ascending=False)
        df_agg_banco_res['ValorFormatado'] = df_agg_banco_res['Valor'].apply(lambda x: f"{x:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
        #st.dataframe(df_agg_banco_res, hide_index=True)
        
        # Calcular a porcentagem no DataFrame
        df_agg_banco_res['Porcentagem'] = (df_agg_banco_res['Valor'] / df_agg_banco_res['Valor'].sum()) * 100
        df_agg_banco_res['Label'] = df_agg_banco_res.apply(lambda row: f"{row['ValorFormatado']} ({row['Porcentagem']:.1f}%)", axis=1)
        # Exibir o gráfico em um bloco seguro no Streamlit

        # Exibir o gráfico em um bloco seguro no Streamlit
        with st.container(border=True):
            st.markdown("📶 Comparativo de bancos")

            # Criar gráfico de barras horizontais
            grafico = alt.Chart(df_agg_banco_res).mark_bar().encode(
                y=alt.Y('Banco', sort=None, title=''),  # Mover TipoPagamento para o eixo y
                x=alt.X('Valor', title='Valor em R$'),  # Mover Valor para o eixo x
                color=alt.Color('Banco', legend=None),
                tooltip=['Banco:O', 'Banco:N', 'Valor:Q']  # Remover a legenda
            ).properties(
                width=670,
                height=300,
            )
            # Adicionar rótulos de dados
            text = grafico.mark_text(
                align='left',  # Alinhar o texto à esquerda
                baseline='middle',
                dx=3,  # Deslocamento horizontal para evitar sobreposição
                color='black', 
                size=13
            ).encode(text='ValorFormatado')
            # Exibir gráfico no Streamlit
            st.altair_chart(grafico + text, use_container_width=True)
            
        
    with graf2:
# METÓDO DE PAGAMENTO -------------------------------------------------------------------------------------------------------------------------------------------------
        df_agg_tipoPgto = df_cap.groupby(['TipoPagamento'])['Valor'].sum().reset_index()
        df_agg_tipoPgto_res = df_agg_tipoPgto.sort_values(by='Valor', ascending=False)
        # Formatar a coluna 'Valor' para exibir com vírgulas como separador decimal
        df_agg_tipoPgto_res['ValorFormatado'] = df_agg_tipoPgto_res['Valor'].apply(lambda x: f"{x:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
        #st.dataframe(df_agg_tipoPgto_res, hide_index=True)
        
        # Exibir o gráfico em um bloco seguro no Streamlit
        with st.container(border=True):
            st.markdown("📶 Métodos de Pagamento")

            # Criar gráfico de barras horizontais
            grafico = alt.Chart(df_agg_tipoPgto_res).mark_bar().encode(
                y=alt.Y('TipoPagamento', sort=None, title=''),  # Mover TipoPagamento para o eixo y
                x=alt.X('Valor', title='Valor em R$'),  # Mover Valor para o eixo x
                color=alt.Color('TipoPagamento', legend=None),
                tooltip=['TipoPagamento:O', 'TipoPagamento:N', 'Valor:Q']  # Remover a legenda
            ).properties(
                width=670,
                height=300,
            )
            # Adicionar rótulos de dados
            text = grafico.mark_text(
                align='left',  # Alinhar o texto à esquerda
                baseline='middle',
                dx=3,  # Deslocamento horizontal para evitar sobreposição
                color='black', 
                size=13
            ).encode(text='ValorFormatado')
            # Exibir gráfico no Streamlit
            st.altair_chart(grafico + text, use_container_width=True)
 

# STATUS -----------------------------------------------------------------------------------------------------------------------------------------------
        df_agg_status = df_cap.groupby(['Status'])['Valor'].sum().reset_index()
        df_agg_status_res = df_agg_status.sort_values(by='Valor', ascending=False)
        # Formatar a coluna 'Valor' para exibir com vírgulas como separador decimal
        df_agg_status_res['ValorFormatado'] = df_agg_status_res['Valor'].apply(lambda x: f"{x:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
        #st.dataframe(df_agg_tipoPgto_res, hide_index=True)
        
        # Exibir o gráfico em um bloco seguro no Streamlit
        with st.container(border=True):
            st.markdown("📶 Status")

            # Criar gráfico de barras horizontais
            grafico = alt.Chart(df_agg_status_res).mark_bar().encode(
                y=alt.Y('Status', sort=None, title=''),  # Mover TipoPagamento para o eixo y
                x=alt.X('Valor', title='Valor em R$'),  # Mover Valor para o eixo x
                color=alt.Color('Status', legend=None),
                tooltip=['Status:O', 'Status:N', 'Valor:Q']  # Remover a legenda
            ).properties(
                width=670,
                height=200,
            )
            # Adicionar rótulos de dados
            text = grafico.mark_text(
                align='left',  # Alinhar o texto à esquerda
                baseline='middle',
                dx=3,  # Deslocamento horizontal para evitar sobreposição
                color='black', 
                size=13
            ).encode(text='ValorFormatado')
            # Exibir gráfico no Streamlit
            st.altair_chart(grafico + text, use_container_width=True)       

    with graf3:
# NATUREZA DA OPERAÇÃO -----------------------------------------------------------------------------------------------------------------------------------------------------
        df_agg_natop = df_cap.groupby(['NaturezaOperacao'])['Valor'].sum().reset_index()
        df_agg_natop_res = df_agg_natop.sort_values(by='Valor', ascending=False)
        df_agg_natop_res['ValorFormatado'] = df_agg_natop_res['Valor'].apply(lambda x: f"{x:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
        #st.dataframe(df_agg_natop_res, hide_index=True)
        
                # Exibir o gráfico em um bloco seguro no Streamlit
        with st.container(border=True):
            st.markdown("📶 Natureza da Operação")

            # Criar gráfico de barras horizontais
            grafico = alt.Chart(df_agg_natop_res).mark_bar().encode(
                y=alt.Y('NaturezaOperacao', sort=None, title=''),  # Mover TipoPagamento para o eixo y
                x=alt.X('Valor', title='Valor em R$'),  # Mover Valor para o eixo x
                color=alt.Color('NaturezaOperacao', legend=None),
                tooltip=['NaturezaOperacao:O', 'NaturezaOperacao:N', 'Valor:Q']  # Remover a legenda
            ).properties(
                width=900,
                height=600,
            )
            # Adicionar rótulos de dados
            text = grafico.mark_text(
                align='left',  # Alinhar o texto à esquerda
                baseline='middle',
                dx=3,  # Deslocamento horizontal para evitar sobreposição
                color='black', 
                size=13
            ).encode(text='ValorFormatado')
            # Exibir gráfico no Streamlit
            st.altair_chart(grafico + text, use_container_width=True)
        
    # ACOMPANHAMENTO POR DIA---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    df_agg_dia_res = df_cap.groupby(['DataVencimento'])['Valor'].sum().reset_index()
    df_agg_dia_res['DataVencimento'] = pd.to_datetime(df_agg_dia_res['DataVencimento'])
    df_agg_dia_res = df_agg_dia_res.sort_values(by='DataVencimento')
    df_agg_dia_res['Dia'] = df_agg_dia_res['DataVencimento'].dt.strftime('%d')  # Extraindo apenas o dia
    df_agg_dia_res['ValorFormatado'] = df_agg_dia_res['Valor'].apply(lambda x: f"{x:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))

    #st.dataframe(df_agg_dia_res, hide_index=True)

    # Exibir o gráfico em um bloco seguro no Streamlit
    with st.container(border=True):
        st.markdown("📶 Acompanhamento por dia")

        # Criar gráfico de linha
        grafico = alt.Chart(df_agg_dia_res).mark_bar().encode(
            x=alt.X('Dia:O', title='Dia de Vencimento'),  # Eixo x agora mostra apenas o dia
            y=alt.Y('Valor:Q', title='Valor em R$'),  # Eixo y como valor agregado
            #color=alt.Color('DataVencimento:T', legend=None),
            tooltip=[alt.Tooltip('DataVencimento:T', title='Data'), alt.Tooltip('Valor:Q', title='Valor', format=',.2f')]
        ).properties(
            width=600,
            height=450,
        )

        # Adicionar rótulos de dados   
        text = grafico.mark_text(
            align='center',  # Alinhar o texto à esquerda
            baseline='bottom', # ['top', 'middle', 'bottom']
            dx=-17,  # Deslocamento horizontal para evitar sobreposição
            color='white',
            size=14
        ).encode(text='ValorFormatado')

        # Exibir gráfico no Streamlit
        st.altair_chart(grafico + text, use_container_width=True)



 



 
 
 
 
 
 
 
 
 
 
 
    # chart = alt.Chart(df_agg_banco_res).mark_bar().encode(
    #     x='Valor:Q',
    #     y=alt.Y('NaturezaOperacao:O', sort='-x')
    # ).properties(width=350,height=400,title='Natureza da Operação').interactive()
    
    # text = chart.mark_text(align='left', baseline='middle',dy=25,  # deslocamento vertical para cima
    #                          color='white', size=15  # cor dos rótulos de dados
    #      ).encode(text='Valor:Q',x='NaturezaOperacao:O',y='Valor:Q')
    
    # st.altair_chart(chart + text, theme="streamlit", use_container_width=True)
 
 
 
    
    # chart = alt.Chart(df_cap).mark_bar().encode(
    #         x=alt.X('NaturezaOperacao:O'), #title='Data'),
    #         y=alt.Y('Valor:Q', title='Banco'),
    #         #color='Data:N',  # Define as cores por métrica
    #         tooltip=['DataVencimento:O', 'Banco:N', 'Valor:Q']
    #     ).properties(width=350,height=250,title='Valor').interactive()
    #     # Adiciona rótulos aos pontos no gráfico
    # text = chart.mark_text(align='center', baseline='middle',dy=25,  # deslocamento vertical para cima
    #                         color='black', size=15  # cor dos rótulos de dados
    #     ).encode(text='Valor:Q',x='DataVencimento:O',y='Banco:Q')
    #     # Exibe o gráfico no Streamlit
    # st.altair_chart(chart + text, use_container_width=False)

