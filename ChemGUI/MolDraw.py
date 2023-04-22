import mols2grid


def df_to_html(df, smiles_col="smiles"):
    df = df.dropna(how="all", axis=1)
    raw_html = mols2grid.display(df, smiles_col=smiles_col)._repr_html_()
    # raw_html = mols2grid.display(df, smiles_col=smiles_col)
    return raw_html
