import numpy as np
import scipy as sp
from tqdm import tqdm
import time
from collections import defaultdict

import ipdb

# Default metaparameters
BLOCK_NCOLS = 1000

class Algorithm(object):
  """Base class stub for all algorithms for analyzing VenomSeq data.
  """
  def __init__(self, venomseq):
    self.venomseq = venomseq


class Connectivity(Algorithm):
  """Connectivity Analysis algorithm for VenomSeq data.
  """
  def __init__(self,
               venomseq,
               block_ncols=BLOCK_NCOLS,
               verbose=True):
    super(Connectivity, self).__init__(venomseq=venomseq)
    self.verbose = verbose

    self.block_ncols = block_ncols

  def run(self):
    if self.verbose:
      print("Beginning connectivity analysis algorithm.")

    self.venoms = []
    #self.dim_cmap = self.venomseq.cmap.data.shape
    self.dim_cmap = (self.venomseq.cmap.rows.shape[0], self.venomseq.cmap.cols.shape[0])

    self.chunk_idxs = self.get_col_blocks(self.dim_cmap, (self.dim_cmap[0], self.block_ncols))

    # Perform main steps of the algorithm
    self.compute_wcs()
    self.compute_genewise_statistics()
    self.normalize_connectivities()
    self.tau_quantize()

    # Copy data to VenomSeq instance
    self.venomseq.connectivity = self.venomseq.connectivity._replace(wcs=self.wcs)
    self.venomseq.connectivity = self.venomseq.connectivity._replace(ncs=self.ncs)
    self.venomseq.connectivity = self.venomseq.connectivity._replace(tau=self.tau)

  def compute_wcs(self):
    if self.verbose:
      print("Computing weighted connectivity scores (WCSs); this may take a while.")

    wcs_start = time.time()
    wcs = np.zeros((self.dim_cmap[1], len(self.venomseq.signatures)))

    # For each venom...
    for v_idx, v_sig in tqdm(enumerate(self.venomseq.signatures), disable=(not self.verbose)):
      self.venoms.append(v_sig['venom'])

      # One venom's worth of WCSs
      scores = np.zeros(self.dim_cmap[1])

      up_ids = self.symbols_2_ids(v_sig['up_list'])
      down_ids = self.symbols_2_ids(v_sig['down_list'])

      # If a gene isn't in the CMap data, remove it
      up_ids_filter = self.filter_cmap_genes(up_ids)
      down_ids_filter = self.filter_cmap_genes(down_ids)

      # For each block of reference signatures...
      for chunk_col_idx in tqdm(self.chunk_idxs, disable=(not self.verbose)):
        c_start, c_end = chunk_col_idx
        chunk = np.array(self.venomseq.cmap.data.iloc[:,c_start:(c_end+1)])

        # For each signatures within the chunk...
        for i in range(chunk.shape[-1]):
          ranks = self.ranked_ids(chunk[:,i])
          ss = self.score_signature(ranks, up_ids_filter, down_ids_filter)
          scores[chunk_col_idx[0]+i] = ss

      wcs[:,v_idx] = scores

    wcs_end = time.time()
    wcs_delta = wcs_end - wcs_start

    if self.verbose:
      print("Computed {0} WCSs in {1} second(s).".format(wcs.shape[0]*wcs.shape[1], wcs_delta))

    # TODO: Make the transpose unnecessary to alleviate future confusion
    self.wcs = wcs.T

  def compute_genewise_statistics(self):
    if self.verbose:
      print("Computing means for cell type and perturbagen type combinations")

    mu = defaultdict(dict)
    all_cell_types = set(self.venomseq.cmap.cols['cell_id'])
    all_pert_types = set(self.venomseq.cmap.cols['pert_type'])
    for c in tqdm(all_cell_types, disable=(not self.verbose)):
      for t in all_pert_types:
        sub_df = self.venomseq.cmap.cols[ \
          (self.venomseq.cmap.cols['cell_id']==c) & \
          (self.venomseq.cmap.cols['pert_type']==t)]

        if sub_df.shape[0] == 0:
          mu[c][t] = (None, None)
        else:
          #ipdb.set_trace()
          sub_idxs = np.array(sub_df['sig_num'])
          sub = self.wcs[:,sub_idxs]
          mu_pos = np.mean(sub[sub > 0.])
          mu_neg = np.mean(sub[sub < 0.])
          mu[c][t] = (mu_pos, mu_neg)
    self.mu = mu

  def normalize_connectivities(self):
    if self.verbose:
      print("Normalizing connectivities by cell line and perturbagen type.")

    ncs_ct = np.zeros(self.wcs.shape)

    # x: CMap signature index
    for x in tqdm(range(self.wcs.shape[-1]), total=self.wcs.shape[-1]):
      cell_type = self.venomseq.cmap.cols.iloc[x]['cell_id']
      pert_type = self.venomseq.cmap.cols.iloc[x]['pert_type']
      mus = self.mu[cell_type][pert_type]

      #normalized_col = [] <-- Did I need this...?
      # y: venom number
      for y in range(self.wcs.shape[0]):
        w = self.wcs[y,x]
        if w > 0.:
          ncs_ct[y,x] = w / mus[0] # positive
        elif w < 0.:
          ncs_ct[y,x] = -(w / mus[1]) # negative

    self.ncs = ncs_ct

  def tau_quantize(self):

    if self.verbose:
      print("Computing Tau scores from normalized connectivity scores.")

    x, y = np.unique(self.venomseq.cmap.cols['cell_id'], return_counts=True)
    kept_cell_lines = list(x[y >= 10])

    all_taus = {}

    for cl in tqdm(kept_cell_lines, disable=(not self.verbose)):
      cur_cell_idxs = np.array((self.venomseq.cmap.cols.loc[self.venomseq.cmap.cols['cell_id'] == cl].sig_num))
      cur_cell_ncs = self.ncs[:,cur_cell_idxs]
      cur_cell_abs = np.abs(cur_cell_ncs).flatten() # Scipy's quantile score freaks out if you don't flatten
      cur_cell_taus = np.zeros_like(cur_cell_ncs)

      for i in tqdm(range(0, cur_cell_ncs.shape[0]), leave=False, disable=(not self.verbose)):
        for j in tqdm(range(0, cur_cell_ncs.shape[1]), leave=False, disable=(not self.verbose)):
          sgn = np.sign(cur_cell_ncs[i,j])
          tau = sgn * sp.stats.percentileofscore(cur_cell_abs, np.abs(cur_cell_ncs[i,j]))
          cur_cell_taus[i,j] = tau

      all_taus[cl] = {
        'idxs': cur_cell_idxs,
        'taus': cur_cell_taus
      }

    t = np.zeros_like(self.ncs)
    for _, data in all_taus.items():
      t[:,data['idxs']] = data['taus']

    self.tau = t


  def ranked_ids(self, drug_arr, desc=True):
    """Obtain a list of ranked genes for a drug in Connectivity Map. The values
    of the array returned by this function are the Entrez gene ids in the
    ranked order.

    Keyword arguments:
    drug_arr -- a numpy.array of normalized gene values (e.g., Level 5 data)
    desc -- Boolean; return with descending ranks (if false, return ascending)
    """
    assert (len(drug_arr.shape) == 1)

    rankidxs = np.argsort(drug_arr)
    ranked = np.empty_like(rankidxs, dtype=int)
    ranked[rankidxs] = self.venomseq.cmap_genes

    if desc:
      ranked = np.flip(ranked, axis=0)
    return ranked

  def enrichment_score(self, drug_ranked, enrichment_set, up=True):
    """Compute an enrichment score, as done by Sirota et al and Lamb et al."""
    r = len(drug_ranked)     # 'probe set'; aka `n`
    s = len(enrichment_set)  # 'tags'; aka `t`
    # V: the indexes of the reference set that are in the enrichment set
    V = np.empty_like(enrichment_set)

    # for each gene in the enrichment set...
    for j in range(s):
      # find the index of that gene in the reference set
      matched = np.argwhere(drug_ranked == enrichment_set[j])
      assert (len(matched) == 1)
      # insert that value into V
      V[j] = matched[0]

    V.sort

    a = 0.
    b = 0.
    # in Lamb et al's definition of a and b, be careful with redefined variables
    for j2 in range(s):
      a_tmp = (j2/s) - (V[j2]/r)
      b_tmp = (V[j2]/r) - ((j2-1)/s)
      a = max(a, a_tmp)
      b = max(b, b_tmp)

    if a > b:
      return a
    else:
      return -b

  def symbols_2_ids(self, symbols):
    vsm = self.venomseq.hsap_symbol_map
    return [int(np.squeeze(vsm[vsm[:,0] == x,:])[1]) for x in symbols]

  def filter_cmap_genes(self, comp_ids):
    mask = np.in1d(comp_ids, self.venomseq.cmap_genes)
    ids_filter = np.extract(mask, comp_ids)
    return ids_filter

  def score_signature(self, drug_ranked, up, down):
    """Given a CMap drug and a comparison signature, compute a connectivity score
    as described in Sirota et al and Lamb et al.

    Keyword arguments:
    drug_ranked -- An int-valued numpy array of rank-sorted Entrez gene ids
    comp_sig -- A dictionary containing a signature to compare, formatted as
                shown above (in `sigs`)
    """
    assert (len(drug_ranked.shape) == 1)

    up_c = np.copy(up)
    down_c = np.copy(down)

    es_up = self.enrichment_score(drug_ranked, up_c)
    es_down = self.enrichment_score(drug_ranked, down_c)

    if (((es_up== es_down) & (es_up==0)) | (es_up*es_down>0)):
      return 0
    else:
      return (es_up - es_down)

  def get_col_blocks(self, total_shape, block_shape):
    """Return indices corresponding to blocks that iterate
    over columns."""
    out_shape_tups = []

    block_ncols = block_shape[-1]
    #total_shape = cmap_data.shape
    block_shape = (total_shape[0], block_ncols)
    total_shape = np.array(total_shape)
    block_shape = np.array(block_shape)

    remainder = 0

    if (total_shape % block_shape).sum() != 0:
      remainder = (total_shape % block_shape)[-1]
      n_cols_trim = total_shape[1] - remainder
    else:
      n_cols_trim = total_shape[1]

    n_blocks = int(n_cols_trim / block_ncols)
    for i in range(n_blocks):
      out_shape_tups.append( (i*block_ncols, ((i+1)*block_ncols)-1) )

    if remainder > 0:
      out_shape_tups.append( (total_shape[-1]-remainder, total_shape[-1]-1) )

    return out_shape_tups
