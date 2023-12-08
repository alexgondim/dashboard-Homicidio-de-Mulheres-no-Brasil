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


st.sidebar.image("vestibular-ufba-2020.jpg", use_column_width=True, output_format="PNG", width=150)
st.sidebar.markdown("<h2>Painel para Análise Visual</h2>", unsafe_allow_html=True)
selected_chart = st.sidebar.selectbox("Selecione o Tipo de Gráfico", ["EAHMB- Mapa de Calor", "HMB - Sunburst", "HMB-Treemap", "HMB- Gráfico de Linhas","EVAHMNN- Mapa de Calor", "EVAHMN - Mapa de Calor"])


selected_year = st.sidebar.selectbox("Selecione o Ano", [2019, 2020, 2021, 2022])
st.sidebar.image("download.png", use_column_width=True, output_format="PNG", width=150)
st.sidebar.markdown("## Legenda")
st.sidebar.markdown("- EAHMB: Evolução Anual de Homicidios de Mulheres no Brasil")
st.sidebar.markdown("- HMB: Homicídios de Mulheres no Brasil")
st.sidebar.markdown("- EVAHMNN: Evolução Anual de Homicidios de Mulheres Não Negras no Brasil")
st.sidebar.markdown("- EVAHMN: Evolução Anual de Homicidios de Mulheres Negras no Brasil")

caminho_do_arquivo = 'vitimas.xlsx' 
df = pd.read_excel(caminho_do_arquivo)  
df1 = pd.read_excel(r'homicidios-mulheres-nao-negras.xlsx')
df2 = pd.read_excel(r'homicidios-mulheres-negras.xlsx')


estados = [
    'Acre', 'Alagoas', 'Amapá', 'Amazonas', 'Bahia', 'Ceará', 'Distrito Federal', 'Espírito Santo',
    'Goiás', 'Maranhão', 'Mato Grosso', 'Mato Grosso do Sul', 'Minas Gerais', 'Pará', 'Paraíba', 'Paraná',
    'Pernambuco', 'Piauí', 'Rio de Janeiro', 'Rio Grande do Norte', 'Rio Grande do Sul', 'Rondônia', 'Roraima',
    'Santa Catarina', 'São Paulo', 'Sergipe', 'Tocantins'
]
anos = [2019, 2020, 2021, 2022]
meses = [
    'janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro',
    'outubro', 'novembro', 'dezembro'
]

data = []
for estado in estados:
    for ano in anos:
        for mes in meses:
            vitimas = np.random.randint(0, 20)
            data.append([estado, 'Homicídio doloso', ano, mes, 'Feminino', vitimas])

df_homicidios = pd.DataFrame(data, columns=['UF', 'Tipo Crime', 'Ano', 'Mês', 'Sexo da Vítima', 'Vítimas'])
df_homicidios['Vítimas'] = df_homicidios['Vítimas'].astype(int)

df_total_vitimas_femininas = df_homicidios.groupby(['UF', 'Ano'])['Vítimas'].sum().reset_index()

state_to_abbreviation = {
    'Acre': 'AC', 'Alagoas': 'AL', 'Amapá': 'AP', 'Amazonas': 'AM', 'Bahia': 'BA',
    'Ceará': 'CE', 'Distrito Federal': 'DF', 'Espírito Santo': 'ES', 'Goiás': 'GO',
    'Maranhão': 'MA', 'Mato Grosso': 'MT', 'Mato Grosso do Sul': 'MS', 'Minas Gerais': 'MG',
    'Pará': 'PA', 'Paraíba': 'PB', 'Paraná': 'PR', 'Pernambuco': 'PE', 'Piauí': 'PI',
    'Rio de Janeiro': 'RJ', 'Rio Grande do Norte': 'RN', 'Rio Grande do Sul': 'RS',
    'Rondônia': 'RO', 'Roraima': 'RR', 'Santa Catarina': 'SC', 'São Paulo': 'SP',
    'Sergipe': 'SE', 'Tocantins': 'TO'
}
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

    df_grouped = df_total_vitimas_femininas.groupby(['UF', 'Ano'])['Vítimas'].sum().reset_index()
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
    df_grouped = df_total_vitimas_femininas.groupby(['UF', 'Ano'])['Vítimas'].sum().reset_index()

    # Convertendo a coluna 'Vítimas' para inteiro para remover casas decimais
    df_grouped['Vítimas'] = df_grouped['Vítimas'].astype(int)

    try:
        color_scale = px.colors.diverging.Portland
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
    df_grouped = df_total_vitimas_femininas.groupby(['UF', 'Ano'])['Vítimas'].sum().reset_index()
    fig_treemap = px.treemap(df_grouped,
                             path=[px.Constant('Brasil'), 'Ano', 'UF'],
                             values='Vítimas',
                             color='Vítimas',
                             color_continuous_scale=px.colors.sequential.Agsunset[::-1])
    fig_treemap.update_layout(
    )
    fig_treemap.data[0].hovertemplate = '%{label}<br>Vítimas: %{value}<extra></extra>'  
    st.plotly_chart(fig_treemap, use_container_width=True)

elif selected_chart == "HMB- Gráfico de Linhas":   
     
    st.markdown("<h4 style='text-align: center;'>Homicídios de Mulheres no Brasil : 2019-2022</h4>", unsafe_allow_html=True)

    st.write("Selecione os estados abaixo:")

    def run_dash_app():
        app = dash.Dash(__name__)

        app.layout = html.Div([
            html.Div([
                dcc.Dropdown(
                    id='state-selector',
                    options=[{'label': uf, 'value': uf} for uf in df_total_vitimas_femininas['UF'].unique()],
                    value=['SP', 'RJ'],
                    multi=True
                )
            ], style={'width': '100%', 'display': 'block', 'margin-bottom': '10px'}),

            html.Div([
                dcc.Graph(id='feminicidio-graph')
            ], style={'width': '100%', 'display': 'inline-block'})
        ])

        @app.callback(
            Output('feminicidio-graph', 'figure'),
            [Input('state-selector', 'value')]
        )
        def update_graph(selected_states):
            traces = []
            for state in selected_states:
                df_filtered = df_total_vitimas_femininas[df_total_vitimas_femininas['UF'] == state]
                traces.append(
                    go.Scatter(
                        x=df_filtered['Ano'],
                        y=df_filtered['Vítimas'],
                        mode='lines+markers',
                        name=state
                    )
                )

            return {
                'data': traces,
                'layout': go.Layout(
                    title='',
                    xaxis={'title': 'Ano', 'tickmode': 'array', 'tickvals': [2019, 2020, 2021, 2022]},
                    yaxis={'title': 'Número de Vítimas'}
                )
            }

        app.run_server(debug=False, port=8050)

    if 'dash_thread' not in st.session_state or not st.session_state.dash_thread.is_alive():
        st.session_state.dash_thread = threading.Thread(target=run_dash_app)
        st.session_state.dash_thread.start()

  
    components.iframe("http://localhost:8050", width=720, height=600) 
