import pandas as pd
import json
import seaborn as sns
import dfply as df
import matplotlib.pyplot as plt
import scipy.stats

s_spearmanr = df.make_symbolic(scipy.stats.spearmanr)

def task_cpi_vs_m_data():
    '''
    Genera tabla comparando variación de base monetaria con inflación.
    '''
    def action(targets):
        m1 = pd.read_csv('data/m1.csv')
        m3 = pd.read_csv('data/m3.csv')
        cpi = pd.read_csv('data/cpi.csv')

        m = pd.concat([m1, m3])

        m_delta = (
            m 
            >> df.group_by('LOCATION', 'MEASURE', 'SUBJECT', 'INDICATOR')
            >> df.mutate(value_delta=df.X.Value.diff() / df.X.Value)
            >> df.mask(~df.X.value_delta.isna())
            >> df.rename(monetary_diff=df.X.value_delta)
        )

        cpi_filtered = (
            cpi
            >> df.mutate(CPI=df.X.Value)
            >> df.mask(df.X.CPI.abs() < 100, df.X.FREQUENCY == 'A',
                       df.X.MEASURE == 'AGRWTH', df.X.SUBJECT == 'TOT'
                      )
            >> df.drop('INDICATOR')
        )

        joined = pd.merge(m_delta, cpi_filtered, on=['LOCATION', 'TIME',
                                                     'FREQUENCY'])
        joined.to_csv(targets[0])

    return {
        'file_dep': ['data/m1.csv', 'data/m3.csv', 'data/cpi.csv'],
        'actions': [action],
        'targets': ['outputs/cpi_vs_m.csv']
    }

def task_cpi_vs_m_plot():
    'Produce scatter de base monetaria vs inflación para todo el mundo.'
    def action(targets):
        joined = pd.read_csv('outputs/cpi_vs_m.csv')

        sns.relplot(data=joined, x='monetary_diff', y='CPI', col='INDICATOR',
                    hue='LOCATION')
        plt.savefig(targets[0])

    return {
        'file_dep': ['outputs/cpi_vs_m.csv'],
        'actions': [action],
        'targets': ['outputs/cpi_vs_m.pdf']
    }

def task_cpi_vs_m_corr():
    'Produce un json con las correlaciones de ambos gráficos en cpi_vs_m_plot'
    def action(targets):
        joined = pd.read_csv('outputs/cpi_vs_m.csv')

        corrs = (
            joined 
            >> df.group_by('INDICATOR')
            >> df.summarize(corr=s_spearmanr(df.X.monetary_diff,
                                                 df.X.CPI))
            >> df.mutate(p=df.X['corr'].apply(lambda x: x[1]),
                         r=df.X['corr'].apply(lambda x: x[0]))
        )

        with open(targets[0], 'w') as f:
            d = {
                '{}_corr'.format(r['INDICATOR']): 
                '{:.3f}'.format(r['r'])
                for k, r in corrs.iterrows()
            }
            print(d)
            json.dump(d, f)

    return {
        'file_dep': ['outputs/cpi_vs_m.csv'],
        'actions': [action],
        'targets': ['outputs/cpi_vs_m.json']
    } 


def task_cpi_vs_m_plot_param():
    'Produce scatter de base monetaria vs inflación para todo el mundo.'
    def action(country, targets):
        joined = pd.read_csv('outputs/cpi_vs_m.csv')
        if country != '':
            joined = (
                joined >>
                df.mask(df.X.LOCATION == country)
            )

        sns.relplot(data=joined, x='monetary_diff', y='CPI', col='INDICATOR',
                    hue='LOCATION')
        plt.savefig(targets[0])

    for country in ['', 'USA']:
        target_base = 'outputs/cpi_vs_m-{}.pdf'
        target = target_base.format(country)
        yield {
            'name': country,
            'file_dep': ['outputs/cpi_vs_m.csv'],
            'actions': [(action, [country])],
            'targets': [target]
        }
