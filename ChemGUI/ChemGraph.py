from bokeh.plotting import figure, ColumnDataSource
from rdkit import Chem
from rdkit.Chem.Draw import rdMolDraw2D
from bokeh import transform
from bokeh.models import ColorBar
from bokeh.io import save
import pandas as pd

scale_slider = 1


def make_svg(smiles: str):  # return SVG str from SMILES str
    x = rdMolDraw2D.MolDraw2DSVG(300 * scale_slider, 300 * scale_slider)
    try:
        x.DrawMolecule(Chem.MolFromSmiles(smiles))
    except:
        x.DrawMolecule(Chem.MolFromSmiles("C"))

    x.FinishDrawing()
    return x.GetDrawingText()


def export_html(
    df,
    x_w,
    y_w,
    label_w,
    smiles_w,
    filename="out.html",
    fill_val=None,
):
    df[x_w] = pd.to_numeric(df[x_w], errors="coerce")
    df[y_w] = pd.to_numeric(df[y_w], errors="coerce")

    if fill_val is None:
        sel_df = df[df[x_w] == df[x_w]]
        sel_df = sel_df[sel_df[y_w] == sel_df[y_w]]
    else:
        sel_df = df
        sel_df[x_w] = sel_df[x_w].fillna(fill_val)
        sel_df[y_w] = sel_df[y_w].fillna(fill_val)

    sel_df[smiles_w] = sel_df[smiles_w].fillna("C")
    smiles_list = list(sel_df[smiles_w].values)  # .tolist()

    # print(sel_df)
    # generate mol objects
    # mols = [Chem.MolFromSmiles(i) for i in sel_df[smiles_w]]
    # smiles_list = [sm for sm, mol in zip(smiles_list, mols) if mol is not None]

    source = ColumnDataSource(
        data=dict(
            x=sel_df[x_w].astype(float),
            y=sel_df[y_w].astype(float),
            label=sel_df[label_w],
            svg=[make_svg(i) for i in sel_df[smiles_w]],
            SMILES=smiles_list,
        )
    )

    TOOLTIPS = "@svg" + "\n" + "@label" + "\n" + "($x, $y)" + "\n"  # +"@SMILES"

    try:
        vmax = max(sel_df[label_w].fillna(0))
        vmin = min(sel_df[label_w].fillna(0))
        color_transformer = transform.linear_cmap("label", "Inferno256", vmin, vmax)

    except:
        color_transformer = transform.factor_cmap(
            "label",
            "Spectral6",
            sel_df[label_w].fillna(0).unique().astype(str),
        )

    p = figure(
        # plot_width=400*scale_slider,
        # plot_height=400*scale_slider,
        x_axis_label=x_w,
        y_axis_label=y_w,
        # tooltips=TOOLTIPS,
        tooltips=TOOLTIPS,
    )

    p.circle(
        "x",
        "y",
        size=10,
        fill_alpha=0.5,
        source=source,
        color=color_transformer,
    )

    color_bar = ColorBar(
        color_mapper=color_transformer["transform"], width=8, location=(0, 0)
    )
    p.add_layout(color_bar, "right")
    save(p, filename=filename)
