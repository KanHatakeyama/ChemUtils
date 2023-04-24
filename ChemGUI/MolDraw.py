import mols2grid


def df_to_html(df, smiles_col="smiles", file_path="table.html"):
    df = df.dropna(how="all", axis=1)
    # raw_html = mols2grid.display(df, smiles_col=smiles_col)._repr_html_()
    mols2grid.save(df, smiles_col=smiles_col, output=file_path)
    # raw_html = ""
    return
