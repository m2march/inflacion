def task_correlaciones():
    'Genera un tex con las correlaciones de cpi vs m'
    return {
        'file_dep': [
            'correlacion_inflacion.tex.tpl'
        ],
        'actions': [
            'template_fill correlacion_inflacion.tex.tpl imgs/cpi_vs_m.json > correlacion_inflacion.tex.done'
        ],
        'targets': [
            'correlacion_inflacion.tex.done'
        ]
    }

def task_paper():
    'Produce el paper'
    return {
        'file_dep': [
            'inflacion_mundo.tex',
            'correlacion_inflacion.tex.done',
            'imgs/cpi_vs_m.pdf'
        ],
        'actions': [
            'pdflatex inflacion_mundo.tex',
        ],
        'targets': ['inflacion_mundo.pdf']
    }
