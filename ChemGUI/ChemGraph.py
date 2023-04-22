import numpy as np
from bokeh.io import output_notebook, show
from bokeh.plotting import figure, ColumnDataSource, output_file, reset_output
import pandas as pd
from bokeh.models import CustomJSHover, HoverTool
from rdkit import Chem
from rdkit.Chem import rdDepictor
from rdkit.Chem.Draw import rdMolDraw2D
from IPython.display import SVG
from bokeh.models import LinearColorMapper, CategoricalColorMapper
from bokeh import transform
from bokeh.models import ColorBar
from bokeh.io import save

scale_slider = 1


def make_svg(smiles: str):  # return SVG str from SMILES str
    x = rdMolDraw2D.MolDraw2DSVG(
        100*scale_slider, 100*scale_slider)
    x.DrawMolecule(Chem.MolFromSmiles(smiles))
    x.FinishDrawing()
    return x.GetDrawingText()


def export_html(df,
                x_w, y_w, label_w, smiles_w,
                filename="out.html"):

    sel_df = df[df[x_w] == df[x_w]]
    sel_df = sel_df[sel_df[y_w] == sel_df[y_w]]

    source = ColumnDataSource(data=dict(
        x=sel_df[x_w].astype(float),
        y=sel_df[y_w].astype(float),
        label=sel_df[label_w],
        svg=[make_svg(i) for i in sel_df[smiles_w]],
        SMILES=sel_df[smiles_w],
    ))

    TOOLTIPS = "@svg"+"\n"+"@label"+"\n" + "($x, $y)"+"\n"  # +"@SMILES"

    try:
        vmax = max(sel_df[label_w].fillna(0))
        vmin = min(sel_df[label_w].fillna(0))
        color_transformer = transform.linear_cmap(
            "label", "Inferno256", vmin, vmax)

    except:
        color_transformer = transform.factor_cmap("label",
                                                  "Spectral6",
                                                  sel_df[label_w].fillna(
                                                      0).unique().astype(str),
                                                  )

    p = figure(
        # plot_width=400*scale_slider,
        # plot_height=400*scale_slider,
        x_axis_label=x_w,
        y_axis_label=y_w,
        # tooltips=TOOLTIPS,
        tooltips=TOOLTIPS,
    )

    p.circle('x', 'y', size=10, fill_alpha=0.5, source=source,
             color=color_transformer,
             )

    color_bar = ColorBar(
        color_mapper=color_transformer['transform'], width=8,  location=(0, 0))
    p.add_layout(color_bar, 'right')
    save(p, filename=filename)
