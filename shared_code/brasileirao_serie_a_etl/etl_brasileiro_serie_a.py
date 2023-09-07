import logging
import requests
from shared_code.variables import URL, HEADER, PRLM_BRA_A
from pandas import read_html, to_numeric


def extract(temporada, rodada):
    url = f'{URL}/schedule/bra-serie-a-{temporada}-spieltag/{rodada}/'
    r = requests.get(url, headers=HEADER)

    dfs = read_html(r.text, header=0)
    if len(dfs[3]) != 0:
        df_rw = dfs[3].copy()
        df_rw['temporada'] = temporada

        logging.info("extraction inicialized")
        logging.info("parm1={0} \nparm2={1}".format(temporada, rodada))
        return df_rw


def transform(input):
    df = input.copy()
    df.drop(['Team'], inplace=True, axis=1)  # null values, escudo do time
    df.rename(index=str, columns={
        '#': 'posicao',
        'Team.1': 'time',
        'M.': 'rodada',
        'W': 'vitoria',
        'D': 'empate',
        'L': 'derrota',
        'goals': 'gols',
        'Dif.': 'diferenca_gols',
        'Pt.': 'pontos'
    }, inplace=True)

    df[['gols', 'gols_sofridos']] = df['gols'].str.split(':', n=1, expand=True)

    df = df.apply(to_numeric, errors='ignore')
    df['posicao'] = to_numeric(df.index) + 1

    df = df.reindex(columns=[
        'posicao',
        'time',
        'rodada',
        'vitoria',
        'empate',
        'derrota',
        'gols',
        'gols_sofridos',
        'diferenca_gols',
        'pontos',
        'temporada'
    ])
    logging.info("transform: {0}".format(PRLM_BRA_A))
    return df


def load():
    ...
