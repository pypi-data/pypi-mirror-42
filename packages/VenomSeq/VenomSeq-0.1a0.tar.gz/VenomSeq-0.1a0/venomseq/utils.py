import numpy as np

from cmapPy.pandasGEXpress.parse import parse

def read_gctx(fname, col_meta=True, row_meta=True, ignore_data_df=False):
  print("  Parsing GCTX file.")

  if ignore_data_df:
    print("  Loading row metadata.")
    rm = parse(fname, row_meta_only=True)
    fix_mangled_byte_literals(rm)
    print("  Loading column metadata.")
    cm = parse(fname, col_meta_only=True)
    fix_mangled_byte_literals(cm)
    cm['sig_num'] = list(range(cm.shape[0]))

    return (None, cm, rm)

  else:
    # Load everything
    print("  IGNORING EXPRESSION SIGNATURES; ONLY LOADING METADATA.")
    print("  If you did not intend to do this, re-run with different arguments.")
    tmp = parse(fname)
    data_df = tmp.data_df

    print("  Fixing mangled byte literals.")
    fix_mangled_byte_literals(data_df)

    if (col_meta):
      print("  Loading column metadata")
      cm = tmp.col_metadata_df
      fix_mangled_byte_literals(cm)
      cm['sig_num'] = list(range(cm.shape[0]))
    if (row_meta):
      print("Loading row metadata")
      rm = tmp.row_metadata_df
      fix_mangled_byte_literals(rm)

    return (data_df, cm, rm)


def fix_mangled_byte_literals(data_df):
  columns = data_df.columns
  idx = data_df.index

  if columns[0][:2] == "b'":
    data_df.columns = [c[2:-1] for c in columns]
  if idx[0][:2] == "b'":
    data_df.index = [i[2:-1] for i in idx]

  # check if byte literals exist in the cells (e.g., if the dataframe contains metadata)
  if data_df.shape != data_df.select_dtypes(np.number).shape:
    # At least one column is nonnumeric, and needs to be checked
    for col in data_df.columns:
      colvalues = np.array(data_df.loc[:,col])
      if not np.issubdtype(colvalues.dtype, np.number):
        if colvalues[0][:2] == "b'":
          data_df.loc[:,col] = [cv[2:-1] for cv in colvalues]
