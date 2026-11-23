from pathlib import Path
import html
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

BASE = Path(__file__).resolve().parent
DADOS = BASE / 'dados'
st.set_page_config(page_title='Dashboard – Plataforma de Instrutores de Direção', page_icon='🚘', layout='wide', initial_sidebar_state='collapsed')
st.markdown(f'<style>{(BASE / "style.css").read_text(encoding="utf-8")}</style>', unsafe_allow_html=True)

@st.cache_data
def carregar_aulas():
    excel = DADOS / 'Autoescola.xlsx'
    csv = DADOS / 'Autoescola_Aulas.csv'
    if excel.exists():
        df = pd.read_excel(excel, sheet_name='Aulas')
    elif csv.exists():
        df = pd.read_csv(csv, sep=';', encoding='utf-8-sig')
    else:
        st.error('Coloque Autoescola.xlsx ou Autoescola_Aulas.csv na pasta dados/.')
        st.stop()
    df.columns = df.columns.str.strip()
    df['Data'] = pd.to_datetime(df['Data'], dayfirst=True, errors='coerce')
    for col in ['Quantidade_Aulas', 'Avaliacao']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

@st.cache_data
def carregar_senatran():
    path = DADOS / 'dados_senatran_tratados - acessos nos meses de agosto-set-out-2026.xlsx'
    return pd.read_excel(path, sheet_name='Acessos') if path.exists() else None

def texto(v):
    return html.escape(str(v))

def painel(titulo):
    st.markdown(f'<div class="panel-heading">{texto(titulo)}</div>', unsafe_allow_html=True)

def grafico(fig, altura=235):
    cor_texto='#26364d'
    fig.update_layout(
        height=altura,
        margin=dict(l=4,r=4,t=10,b=8),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Arial', color=cor_texto, size=11),
        hoverlabel=dict(bgcolor='#ffffff', bordercolor='#dce5f0', font=dict(color=cor_texto)),
        showlegend=False
    )
    fig.update_xaxes(
        color=cor_texto,
        tickfont=dict(color=cor_texto),
        title_font=dict(color=cor_texto),
        gridcolor='#e4ebf3',
        linecolor='#9ba9bc'
    )
    fig.update_yaxes(
        color=cor_texto,
        tickfont=dict(color=cor_texto),
        title_font=dict(color=cor_texto),
        gridcolor='#e4ebf3',
        linecolor='#9ba9bc'
    )
    fig.update_traces(textfont=dict(color=cor_texto))
    fig.update_annotations(font=dict(color=cor_texto))
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar':False})

def barras_progresso(serie, modo='aulas', limite=5):
    serie=serie.head(limite)
    if serie.empty:
        st.info('Sem dados disponíveis.'); return
    maximo=float(serie.max()) or 1
    for nome, valor in serie.items():
        pct=max(2,100*float(valor)/maximo)
        rotulo=f'{int(valor):,} aulas'.replace(',','.') if modo=='aulas' else f'{float(valor):.1f} ★'
        st.markdown(f'''<div class="progress-entry"><div class="progress-line"><span>{texto(nome)}</span><strong>{texto(rotulo)}</strong></div><div class="track"><div class="fill" style="width:{pct:.1f}%"></div></div></div>''',unsafe_allow_html=True)

raw=carregar_aulas()
anos=sorted(raw['Data'].dropna().dt.year.unique().tolist())
with st.expander('Filtros dos dados', expanded=False):
    ca,cb,cc=st.columns(3)
    ano=ca.selectbox('Ano', ['Todos']+anos, index=0)
    cidades=cb.multiselect('Cidades',sorted(raw['Cidade'].dropna().unique().tolist()))
    instrutores=cc.multiselect('Instrutores',sorted(raw['Instrutor'].dropna().unique().tolist()))
df=raw.copy()
if ano!='Todos': df=df[df['Data'].dt.year==ano]
if cidades: df=df[df['Cidade'].isin(cidades)]
if instrutores: df=df[df['Instrutor'].isin(instrutores)]

st.markdown('''<div class="topbar"><h1>Dashboard – Plataforma de Instrutores de Direção</h1><span>Projeto Integrador • Monitoramento de Operações e Qualidade</span></div>''',unsafe_allow_html=True)
total=int(df['Quantidade_Aulas'].sum())
alunos=df['Aluno'].nunique()
media=df['Avaliacao'].mean()
cidades_total=df.groupby('Cidade')['Quantidade_Aulas'].sum().sort_values(ascending=False)
cidade=cidades_total.index[0] if len(cidades_total) else 'Sem dados'
indicadores=[('Total de Aulas Realizadas',f'{total:,}'.replace(',','.')),('Total de Alunos Cadastrados',str(alunos)),('Média Geral de Satisfação',f'{media:.1f}'.replace('.',',')+' / 5' if pd.notna(media) else 'Sem dados'),('Cidade com Maior Demanda',cidade)]
cols=st.columns(4,gap='medium')
for c,(titulo,valor) in zip(cols,indicadores):
    with c:
        st.markdown(f'<div class="kpi"><div class="kpi-title">{texto(titulo)}</div><div class="kpi-value">{texto(valor)}</div></div>',unsafe_allow_html=True)

left,center,right=st.columns([1.08,1.06,.95],gap='medium')
with left:
    with st.container(border=True):
        painel('Evolução Mensal das Aulas')
        mensal=df.dropna(subset=['Data']).groupby(df['Data'].dt.to_period('M'))['Quantidade_Aulas'].sum().sort_index()
        if mensal.empty: st.info('Sem datas de aulas disponíveis.')
        else:
            labels=[p.strftime('%m/%Y') for p in mensal.index]
            fig=go.Figure()
            fig.add_trace(go.Bar(x=labels,y=mensal.values,marker_color='#f1edfb',width=.34,hovertemplate='%{x}: %{y} aulas<extra></extra>'))
            fig.add_trace(go.Scatter(x=labels,y=mensal.values,mode='lines+markers',line=dict(color='#8122d8',width=3),marker=dict(size=8,color='#8122d8'),hovertemplate='%{x}: %{y} aulas<extra></extra>'))
            fig.update_xaxes(showgrid=False,showline=False,zeroline=False)
            fig.update_yaxes(visible=False)
            grafico(fig,255)
    with st.container(border=True):
        painel('Quantidade de Aulas por Cidade')
        st.markdown(f'<div class="panel-note">Total: {total:,} aulas</div>'.replace(',','.'),unsafe_allow_html=True)
        cid=cidades_total.head(5)
        if cid.empty: st.info('Sem dados de cidades.')
        else:
            fig=go.Figure(go.Bar(x=list(cid.index),y=list(cid.values),marker_color=['#6820aa','#8725d6','#a24bf0','#c184fa','#d9b5fb'][:len(cid)],text=[str(int(x)) for x in cid.values],textposition='outside',cliponaxis=False))
            fig.update_xaxes(showgrid=False,tickfont=dict(size=10))
            fig.update_yaxes(visible=False,range=[0,max(cid.values)*1.27])
            grafico(fig,225)
with center:
    with st.container(border=True):
        painel('Quantidade de Aulas por Instrutor')
        qtd=df.groupby('Instrutor')['Quantidade_Aulas'].sum().sort_values(ascending=False)
        barras_progresso(qtd,limite=8)
with right:
    with st.container(border=True):
        painel('Desempenho dos Instrutores')
        aval=df.dropna(subset=['Avaliacao']).groupby('Instrutor')['Avaliacao'].mean().sort_values(ascending=False)
        barras_progresso(aval,modo='estrelas',limite=8)
    with st.container(border=True):
        painel('Satisfação dos alunos')
        nomes=['Muito Satisfeito','Satisfeito','Neutro','Insatisfeito','Muito Insatisfeito']
        cores=['#42116f','#68209b','#8828d4','#ad5cf0','#d7adfa']
        if 'Perfil' in df.columns and df['Perfil'].notna().any():
            perf=df['Perfil'].astype(str).str.strip().str.casefold()
            categorias={n: int((perf==n.casefold()).sum()) for n in nomes}
            # Nomes alternativos não são convertidos silenciosamente em categorias.
            desconhecidos=int((~perf.isin([n.casefold() for n in nomes])).sum())
            if desconhecidos: categorias['Outros / não classificados']=desconhecidos;cores.append('#b8bdc9')
        else:
            a=df['Avaliacao'].dropna()
            categorias={n:int((a==v).sum()) for n,v in zip(nomes,[5,4,3,2,1])}
        categorias={k:v for k,v in categorias.items() if v>0}
        if not categorias: st.info('Sem avaliações disponíveis.')
        else:
            fig=go.Figure(go.Pie(labels=list(categorias),values=list(categorias.values()),hole=.65,marker=dict(colors=cores[:len(categorias)]),textinfo='none',hovertemplate='%{label}: %{value} (%{percent})<extra></extra>'))
            fig.update_layout(
                margin=dict(l=0,r=0,t=0,b=0),
                height=195,
                showlegend=False,
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Arial', color='#26364d', size=11),
                hoverlabel=dict(bgcolor='#ffffff', bordercolor='#dce5f0', font=dict(color='#26364d'))
            )
            fig.update_traces(textfont=dict(color='#26364d'))
            st.plotly_chart(fig,use_container_width=True,config={'displayModeBar':False})
            total_resp=sum(categorias.values())
            st.markdown('<div class="satisfaction-list">'+''.join(f'<div><span>{texto(n)}</span><b>{100*v/total_resp:.0f}%</b></div>' for n,v in categorias.items())+'</div>',unsafe_allow_html=True)

with st.expander('Dados complementares – Acessos SENATRAN (2026)',expanded=False):
    sen=carregar_senatran()
    if sen is None: st.info('Arquivo de acessos SENATRAN não encontrado.')
    else:
        sen.columns=sen.columns.str.strip()
        sen['Data']=pd.to_datetime(sen['Data'],errors='coerce')
        sen['Mes']=sen['Data'].dt.to_period('M')
        acesso=sen.groupby('Mes').size().sort_index()
        st.caption('Acessos de 2026 são uma base distinta das aulas de 2025; não são somados às aulas.')
        st.metric('Total de acessos',f'{len(sen):,}'.replace(',','.'))
        fig=go.Figure(go.Bar(x=[str(m) for m in acesso.index],y=acesso.values,marker_color='#8122d8',text=acesso.values,textposition='outside'))
        grafico(fig,260)
        a,b=st.columns(2)
        with a:
            st.subheader('Dispositivos')
            dispositivos=sen['Dispositivo'].dropna().value_counts()
            if dispositivos.empty:
                st.info('Sem dados de dispositivos disponíveis.')
            else:
                fig=go.Figure(go.Pie(
                    labels=dispositivos.index,
                    values=dispositivos.values,
                    hole=.62,
                    marker=dict(colors=['#8122d8','#b86cf3','#e2c6fb','#dce5f0']),
                    textinfo='label+percent',
                    textposition='outside',
                    hovertemplate='%{label}: %{value:,} acessos (%{percent})<extra></extra>'
                ))
                fig.update_layout(showlegend=False)
                grafico(fig,285)
        with b:
            st.subheader('Origem do tráfego')
            origens=sen['Origem do tráfego'].dropna().value_counts().head(8).sort_values()
            if origens.empty:
                st.info('Sem dados de origem do tráfego disponíveis.')
            else:
                fig=go.Figure(go.Bar(
                    x=origens.values,
                    y=origens.index,
                    orientation='h',
                    marker_color='#8122d8',
                    text=[f'{valor:,}'.replace(',', '.') for valor in origens.values],
                    textposition='outside',
                    cliponaxis=False,
                    hovertemplate='%{y}: %{x:,} acessos<extra></extra>'
                ))
                fig.update_xaxes(visible=False, range=[0, max(origens.values)*1.18])
                fig.update_yaxes(showgrid=False, tickfont=dict(size=11))
                grafico(fig,285)

st.caption('Fonte: Autoescola.xlsx / Autoescola_Aulas.csv • Os indicadores refletem os filtros selecionados. Acessos SENATRAN são apresentados separadamente.')
