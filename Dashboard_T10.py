
import streamlit as st
import pandas as pd
import plotly.express as px
import json
import numpy as np
import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import threading
import streamlit.components.v1 as components
from PIL import Image


st.set_page_config(
    page_title="Análise Visual do Homicídio de Mulheres no Brasil",
    page_icon=":bar_chart:"
)


st.markdown(
    """
    <style>
    .titulo-cabecalho {
    background-color: #4B0082; /* Azul Médio (Indigo) */
    color: white; /* Cor do texto */
    padding: 10px; /* Espaçamento interno */
    text-align: center;
    font-size: 24px;
}
    .grafico-titulo {
        margin-top: 30px; /* Espaçamento acima dos títulos dos gráficos */
    }
    .titulo-treemap {
        font-size: 24px;
        color: #333;
        text-align: center;
    }
    .quadrado {
        background-color: purple;
        color: white;
        padding: 10px;
        text-align: center;
        font-size: 20px;
        margin: 10px 0;
    }
    </style>
    
    """,
    unsafe_allow_html=True
)
st.markdown("<div class='titulo-cabecalho'>Análise Visual de Homicídios de Mulheres no Brasil<p>Disciplina: Computação Visual- Discente: Alex Gondim</p></div>", unsafe_allow_html=True)
#
@st.cache_data
def load_df1():
    return pd.read_excel('homicidios-mulheres-nao-negras.xlsx')

# Função para carregar 'homicidios-mulheres-negras.xlsx'
@st.cache_data
def load_df2():
    return pd.read_excel('homicidios-mulheres-negras.xlsx')

# Carregando os DataFrames usando as funções
df1 = load_df1()
df2 = load_df2()

# Função para gerar o gráfico do mês com mais vítimas

st.sidebar.image("vestibular-ufba-2020.jpg", use_column_width=True, output_format="PNG", width=150)
st.sidebar.markdown("<h2>Painel para Análise Visual</h2>", unsafe_allow_html=True)
selected_chart = st.sidebar.selectbox("Selecione o Tipo de Gráfico", ["EAHMB- Mapa de Calor", "HMB - Sunburst", "HMB-Treemap", "HMB- Gráfico de Linhas","EVAHMNN- Mapa de Calor", "EVAHMN - Mapa de Calor", "HMBM-Gráf.Barra"])


#selected_year = st.sidebar.selectbox("Selecione o Ano", [2019, 2020, 2021, 2022])
selected_year = st.sidebar.radio("Total de Vitimas Por Ano  - Selecione o Ano: ", [2019, 2020, 2021, 2022], index=0)
#selected_year = st.sidebar.slider("Selecione o Ano", 2019, 2022, value=2019)


st.sidebar.image("download.png", use_column_width=True, output_format="PNG", width=150)
st.sidebar.markdown("## Legenda")
st.sidebar.markdown("- EAHMB: Evolução Anual de Homicidios de Mulheres no Brasil")
st.sidebar.markdown("- HMB: Homicídios de Mulheres no Brasil")
st.sidebar.markdown("- EVAHMNN: Evolução Anual de Homicidios de Mulheres Não Negras no Brasil")
st.sidebar.markdown("- EVAHMN: Evolução Anual de Homicidios de Mulheres Negras no Brasil")
st.sidebar.markdown("- HMBM: Homicídios de Mulheres Por Mês")


@st.cache_data
def carregar_dados(caminho_arquivo):
    df_vitimas = pd.read_excel(caminho_arquivo)
    return df_vitimas

def processar_dados(df_vitimas):
    estados = df_vitimas['UF'].unique()
    anos = df_vitimas['Ano'].unique()
    meses = df_vitimas['Mês'].unique()

    data = []
    for estado in estados:
        for ano in anos:
            for mes in meses:
                filtro = (df_vitimas['UF'] == estado) & (df_vitimas['Ano'] == ano) & \
                         (df_vitimas['Mês'] == mes) & (df_vitimas['Sexo da Vítima'] == 'Feminino')
                vitimas = df_vitimas[filtro]['Vítimas'].sum()
                data.append([estado, 'Homicídio doloso', ano, mes, 'Feminino', vitimas])

    df_homicidios = pd.DataFrame(data, columns=['UF', 'Tipo de Crime', 'Ano', 'Mês', 'Sexo da Vítima', 'Vítimas'])
    df_homicidios['Vítimas'] = df_homicidios['Vítimas'].astype(int)
    return df_homicidios

def total_vitimas_por_estado_ano(df_homicidios):
    df_total_vitimas_femininas = df_homicidios.groupby(['UF', 'Ano'])['Vítimas'].sum().reset_index()
    return df_total_vitimas_femininas


    
# Funções para processar dados de homicídios
caminho_do_arquivo = 'vitimas.xlsx' 
df_vitimas = carregar_dados(caminho_do_arquivo)
df_homicidios = processar_dados(df_vitimas)
df_total_vitimas_femininas = total_vitimas_por_estado_ano(df_homicidios)

state_to_abbreviation = {
    'Acre': 'AC', 'Alagoas': 'AL', 'Amapá': 'AP', 'Amazonas': 'AM', 'Bahia': 'BA',
    'Ceará': 'CE', 'Distrito Federal': 'DF', 'Espírito Santo': 'ES', 'Goiás': 'GO',
    'Maranhão': 'MA', 'Mato Grosso': 'MT', 'Mato Grosso do Sul': 'MS', 'Minas Gerais': 'MG',
    'Pará': 'PA', 'Paraíba': 'PB', 'Paraná': 'PR', 'Pernambuco': 'PE', 'Piauí': 'PI',
    'Rio de Janeiro': 'RJ', 'Rio Grande do Norte': 'RN', 'Rio Grande do Sul': 'RS',
    'Rondônia': 'RO', 'Roraima': 'RR', 'Santa Catarina': 'SC', 'São Paulo': 'SP',
    'Sergipe': 'SE', 'Tocantins': 'TO'
}


# Correção: substituir 'UF' por 'UF'
df_total_vitimas_femininas['UF'] = df_total_vitimas_femininas['UF'].replace(state_to_abbreviation)



total_vitimas = df_total_vitimas_femininas[df_total_vitimas_femininas['Ano'] == selected_year]['Vítimas'].sum()


if selected_year > 2019:
    total_vitimas_ano_anterior = df_total_vitimas_femininas[df_total_vitimas_femininas['Ano'] == (selected_year - 1)]['Vítimas'].sum()
    variacao_ano_anterior = total_vitimas - total_vitimas_ano_anterior
    variacao_percentual = ((total_vitimas - total_vitimas_ano_anterior) / total_vitimas_ano_anterior) * 100
else:
    variacao_ano_anterior = 0
    variacao_percentual = 0

col1, col2 = st.columns(2)
col1.markdown(f"<div class='quadrado'>Quantidade Total de Vítimas em {selected_year}: {total_vitimas}</div>", unsafe_allow_html=True)
col2.markdown(f"<div class='quadrado'>Variação em Relação ao Ano Anterior: {variacao_ano_anterior} ({variacao_percentual:.2f}%)</div>", unsafe_allow_html=True)

df1.columns = df1.columns.str.strip()
df2.columns = df2.columns.str.strip()


df1.fillna(0, inplace=True)
df2.fillna(0, inplace=True)


df_filtered_black = df2[(df2['ANO'] >= 2015) & (df2['ANO'] <= 2022)]
df_grouped_black = df_filtered_black.groupby(['UF', 'ANO'])['VITIMAS_NEGRAS'].sum().reset_index()


df_filtered_non_black = df1[(df1['ANO'] >= 2015) & (df1['ANO'] <= 2022)]
df_grouped_non_black = df_filtered_non_black.groupby(['UF', 'ANO'])['VITIMAS_NAO_NEGRAS'].sum().reset_index()


df_filtrado = df1[df1['ANO'].between(2015, 2019)]
df_grouped_total = df_filtrado.groupby('UF')['VITIMAS_NAO_NEGRAS'].sum().reset_index()


###### gerar_grafico_vitimas_mes ################################

def gerar_grafico_vitimas_mes(df_vitimas, estado, ano):
    # Filtrando os dados
    df_filtrado = df_vitimas[(df_vitimas['UF'] == estado) & (df_vitimas['Ano'] == ano) & (df_vitimas['Sexo da Vítima'] == 'Feminino')]
    vitimas_por_mes = df_filtrado.groupby('Mês')['Vítimas'].sum().reset_index()

    # Ordenando os dados por mês
    meses = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 
             'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
    vitimas_por_mes['Mês'] = pd.Categorical(vitimas_por_mes['Mês'], categories=meses, ordered=True)
    vitimas_por_mes = vitimas_por_mes.sort_values('Mês')

    # Criando o gráfico
    if not vitimas_por_mes.empty:
        fig = px.bar(vitimas_por_mes, x='Mês', y='Vítimas',
                     title=f'Número de Vítimas Femininas por Mês em {estado} - {ano}',
                     labels={'Mês': 'Mês', 'Vítimas': 'Número de Vítimas'})
        return fig
    else:
        return "Não há dados suficientes para o estado e ano selecionados."


# Carregar os dados

df_vitimas = pd.read_excel("vitimas.xlsx")


########################################################################
with open('uf.json', 'r', encoding='ISO-8859-1') as file:
    brazil_geojson = json.load(file)


if selected_chart == "EVAHMNN- Mapa de Calor":
    st.markdown("<h3 style='text-align: center;'>Evolução Anual de Homicídios de Mulheres Não Negras-UF</h3>", unsafe_allow_html=True)
   
   
    total_vitimas_por_ano = df_grouped_non_black.groupby('ANO')['VITIMAS_NAO_NEGRAS'].sum()

  
    color_scale = px.colors.diverging.Portland

    fig_general = px.choropleth(df_grouped_non_black,
                                 geojson=brazil_geojson,
                                 locations='UF',
                                 featureidkey="properties.UF_05",
                                 color='VITIMAS_NAO_NEGRAS',
                                 animation_frame='ANO',
                                 scope='south america',
                                 color_continuous_scale=color_scale)

    
    for ano in df_grouped_non_black['ANO'].unique():
        total_vitimas = total_vitimas_por_ano[ano]
        titulo = f"Total de Vítimas em {ano}: {total_vitimas}"
        fig_general.layout.sliders[0].steps[ano - df_grouped_non_black['ANO'].min()].label = titulo

    fig_general.update_layout(
            width=900,  
            height=600,   
            margin=dict(t=100)
    
    )
    fig_general.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig_general, use_container_width=True)

elif selected_chart == "EVAHMN - Mapa de Calor":
    st.markdown("<h3 style='text-align: center;'>Evolução Anual de Homicidios de Mulheres Negras-UF</h3>", unsafe_allow_html=True)
    color_scale = px.colors.diverging.Portland
    fig_black = px.choropleth(df_grouped_black,
                              geojson=brazil_geojson,
                              locations='UF',
                              featureidkey="properties.UF_05",
                              color='VITIMAS_NEGRAS',
                              animation_frame='ANO',
                              scope='south america',
                              color_continuous_scale=color_scale)
    fig_black.update_layout(
        
        geo=dict(showframe=False, showcoastlines=False, projection_type='equirectangular')
    )
    fig_black.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig_black, use_container_width=True)

elif selected_chart == "EAHMB- Mapa de Calor":
    st.markdown("<h4 style='text-align: center;'>Evolução Anual de Homicídios de Mulheres no Brasil:2019-2022</h4>", unsafe_allow_html=True)

    with open('uf.json', 'r', encoding='ISO-8859-1') as file:
            brazil_geojson = json.load(file)
    df_filtrado = df_total_vitimas_femininas[df_total_vitimas_femininas['Ano'] >= 2019]

# Agrupar os dados filtrados
    df_grouped = df_filtrado.groupby(['UF', 'Ano'])['Vítimas'].sum().reset_index() 

    #df_grouped = df_total_vitimas_femininas.groupby(['UF', 'Ano'])['Vítimas'].sum().reset_index()
    color_scale = px.colors.sequential.Plasma_r

    fig2 = px.choropleth(df_grouped,
                            geojson=brazil_geojson,
                            locations='UF',
                            featureidkey="properties.UF_05",
                            color='Vítimas',
                            animation_frame='Ano',
                            scope='south america',
                            color_continuous_scale=color_scale)

    fig2.update_layout(
            geo=dict(
                showframe=False,
                showcoastlines=False,
                projection_type='equirectangular'
            )
        )

    fig2.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig2, use_container_width=True)
    
elif selected_chart == "HMB - Sunburst":
    st.markdown("<h4 style='text-align: center;'>Homicídios de Mulheres no Brasil : 2019-2022</h4>", unsafe_allow_html=True)
   
    # Supondo que df_total_vitimas_femininas já esteja definido
    df_filtrado = df_total_vitimas_femininas[df_total_vitimas_femininas['Ano'] >= 2019]

# Agrupar os dados filtrados
    df_grouped = df_filtrado.groupby(['UF', 'Ano'])['Vítimas'].sum().reset_index()
    # Convertendo a coluna 'Vítimas' para inteiro para remover casas decimais
    df_grouped['Vítimas'] = df_grouped['Vítimas'].astype(int)

    try:
        
        color_scale = px.colors.diverging.Portland
        if df_grouped['Vítimas'].sum() > 0:
            fig_sunburst = px.sunburst(
                df_grouped,
                path=['UF', 'Ano'],  # Caminhos do gráfico Sunburst
                values='Vítimas',  # Valores a serem exibidos
                color='Vítimas',  # Base da escala de cores
                color_continuous_scale=color_scale
            )

        # Atualizando as dicas de ferramentas para exibir corretamente os rótulos renomeados e formatados
        fig_sunburst.update_traces(
            hovertemplate="<b>Estado:</b> %{label}<br><b>Vítimas:</b> %{value}<extra></extra>"
        )

        fig_sunburst.update_layout(
            width=900,
            height=600,
            uniformtext=dict(minsize=10)  # Ajustando o tamanho do texto para melhor visibilidade
        )

        st.plotly_chart(fig_sunburst, use_container_width=True)
    except ValueError as e:
        st.error(f"Erro ao criar gráfico Sunburst: {e}")

elif selected_chart == "HMB-Treemap":
    st.markdown("<h4 style='text-align: center;'>Homicídios de Mulheres no Brasil : 2019-2022</h4>", unsafe_allow_html=True)

    # Gráfico Treemap
    
    df_filtrado = df_total_vitimas_femininas[df_total_vitimas_femininas['Ano'] >= 2019]

# Agrupar os dados filtrados
    df_grouped = df_filtrado.groupby(['UF', 'Ano'])['Vítimas'].sum().reset_index()
    
    if df_grouped['Vítimas'].sum() > 0:
        fig_treemap = px.treemap(df_grouped,
                                path=[px.Constant('Brasil'), 'Ano', 'UF'],
                                values='Vítimas',
                                color='Vítimas',
                                color_continuous_scale=px.colors.sequential.Agsunset[::-1])
        fig_treemap.update_layout(
        )
        fig_treemap.data[0].hovertemplate = '%{label}<br>Vítimas: %{value}<extra></extra>'  
        st.plotly_chart(fig_treemap, use_container_width=True)

# Assuming df_total_vitimas_femininas is your DataFrame containing the data


elif selected_chart == "HMB- Gráfico de Linhas":
    st.markdown("<h4 style='text-align: center;'>Homicídios de Mulheres no Brasil: 2019-2022</h4>", unsafe_allow_html=True)

    # Selecionar estados
    st.write("Selecione os estados abaixo:")
    selected_states = st.multiselect("Estados", options=df_total_vitimas_femininas['UF'].unique(), default=['SP', 'RJ'])

    # Filtrando o DataFrame para incluir apenas dados de 2019 em diante
    df_filtrado = df_total_vitimas_femininas[df_total_vitimas_femininas['Ano'] >= 2019]

    # Criando o gráfico de linhas com base nos estados selecionados
    if selected_states:
        fig = go.Figure()

        for state in selected_states:
            df_estado_filtrado = df_filtrado[df_filtrado['UF'] == state]
            fig.add_trace(go.Scatter(
                x=df_estado_filtrado['Ano'],
                y=df_estado_filtrado['Vítimas'],
                mode='lines+markers',
                name=state
            ))

        # Configurando layout do gráfico
        fig.update_layout(
            title='',
            xaxis={'title': 'Ano', 'tickmode': 'array', 'tickvals': [2019, 2020, 2021, 2022]},
            yaxis={'title': 'Número de Vítimas'}
        )

        st.plotly_chart(fig, use_container_width=True)
        
elif selected_chart == "HMBM-Gráf.Barra":
    st.markdown("<h4 style='text-align: center;'>Homicídios de Mulheres no Brasil: 2015-2022</h4>", unsafe_allow_html=True)

    # Seletores de Estado e Ano no Streamlit
    estado_selecionado = st.selectbox("Selecione o Estado", options=df_vitimas['UF'].unique())
    ano_selecionado = st.selectbox("Selecione o Ano", options=df_vitimas['Ano'].unique())

    # Gerando e exibindo o gráfico no Streamlit
    grafico = gerar_grafico_vitimas_mes(df_vitimas, estado_selecionado, ano_selecionado)
    if isinstance(grafico, str):
        st.write(grafico)
    else:
        st.plotly_chart(grafico)

        

