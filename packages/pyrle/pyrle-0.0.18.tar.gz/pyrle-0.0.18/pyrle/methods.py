import pandas as pd
import numpy as np

from pyrle import Rle
from pyrle.rledict import PyRles
from pyrle.src.coverage import _coverage

from natsort import natsorted

from sys import stderr

from collections import defaultdict



try:
    # ray.init(logging_level=logging.CRITICAL) # logging_level=logging.CRITICAL # local_mode=True
    import ray
    import logging
    if not ray.is_initialized():
        ray.init(local_mode=True, logging_level=logging.CRITICAL, ignore_reinit_error=True) # logging_level=logging.CRITICAL # local_mode=True
except:
    import pyrle.raymock as ray


try:
    dummy = profile
except:
    profile = lambda x: x


def _merge_rles(rle):

    new_dict = {}
    dd = defaultdict(list)
    for chromosome, strand in rle.rles.keys():
        dd[chromosome].append(strand)

    for c, s in dd.items():
        if len(s) == 1:
            new_dict[c] = rle.rles[c, s[0]]
        else:
            new_dict[c] = rle.rles[c, "+"] + rle.rles[c, "-"]

    return new_dict


def ensure_both_or_none_stranded(self, other):

    # means other not stranded
    if self.stranded:
        self.rles = _merge_rles(self)
    else:
        other.rles = _merge_rles(other)

    return self, other


def chromosomes_in_both_self_other(self, other):

    chromosomes_in_both = natsorted(set(self.rles.keys()).intersection(other.rles.keys()))
    chromosomes_in_self_not_other = natsorted(set(self.rles.keys()) - set(other.rles.keys()))
    chromosomes_in_other_not_self = natsorted(set(other.rles.keys()) - set(self.rles.keys()))

    return chromosomes_in_both, chromosomes_in_self_not_other, chromosomes_in_other_not_self


def binary_operation(operation, self, other):

    func = {"div": __div, "mul": __mul, "add": __add, "sub": __sub}[operation]

    if self.stranded != other.stranded:
        self, other = ensure_both_or_none_stranded(self, other)

    chromosomes_in_both, chromosomes_in_self_not_other, chromosomes_in_other_not_self = chromosomes_in_both_self_other(self, other)

    both_results = []
    for c in chromosomes_in_both:
        both_results.append(func.remote(self.rles[c], other.rles[c]))

    # rles = {c: r for c, r in zip(cs, _rles)}

    self_results = []
    for c in chromosomes_in_self_not_other:
        _other = Rle([np.sum(self.rles[c].runs)], [0])
        self_results.append(func.remote(self.rles[c], _other))

    other_results = []
    for c in chromosomes_in_other_not_self:
        _self = Rle([np.sum(other.rles[c].runs)], [0])
        other_results.append(func.remote(_self, other.rles[c]))


    rles = {k: v for k, v in zip(chromosomes_in_both + chromosomes_in_self_not_other + chromosomes_in_other_not_self,
                                 ray.get(both_results + self_results + other_results))}
    return PyRles(rles)


@ray.remote
def __add(self, other):

    return self + other

@ray.remote
def __sub(self, other):

    return self - other

@ray.remote
def __div(self, other):

    return self / other

@ray.remote
def __mul(self, other):

    return self * other



@ray.remote
def coverage(df, kwargs):

    value_col = kwargs.get("value_col", None)

    if value_col:
        values = df[value_col].astype(np.float64).values
    else:
        values = np.ones(len(df))

    starts_df = pd.DataFrame({"Position": df.Start, "Value": values})["Position Value".split()]
    ends_df = pd.DataFrame({"Position": df.End, "Value": -1 * values})["Position Value".split()]
    _df = pd.concat([starts_df, ends_df], ignore_index=True)
    _df = _df.sort_values("Position", kind="mergesort")

    if _df.Position.dtype.name == "int32":
        _df.Position = _df.Position.astype(np.int64)

    runs, values = _coverage(_df.Position.values, _df.Value.values)

    return Rle(runs, values)




def to_ranges(grles):

    from pyranges import PyRanges

    dfs = []
    if grles.stranded:

        for (chromosome, strand), rle in grles.items():
            starts, ends, values = _to_ranges(rle)
            df = pd.concat([pd.Series(r) for r in [starts, ends, values]], axis=1)
            df.columns = "Start End Score".split()
            df.insert(0, "Chromosome", chromosome)
            df.insert(df.shape[1], "Strand", strand)
            df = df[df.Score != 0]
            dfs.append(df)
    else:

        for chromosome, rle in grles.items():
            starts, ends, values = _to_ranges(rle)
            df = pd.concat([pd.Series(r) for r in [starts, ends, values]], axis=1)
            df.columns = "Start End Score".split()
            df.insert(0, "Chromosome", chromosome)
            df = df[df.Score != 0]
            dfs.append(df)

    return PyRanges(pd.concat(dfs))


def _to_ranges(rle):

    runs = pd.Series(rle.runs)
    starts = pd.Series([0] + list(runs)).cumsum()

    ends = starts + runs

    values = pd.Series(rle.values)

    start_idx = values[values.shift(-1) != values].index
    end_idx = values[values.shift(1) != values].index

    starts = starts.loc[start_idx]
    ends = ends.loc[end_idx]
    values = values[start_idx].reset_index(drop=True)

    return starts.astype(int).reset_index(drop=True), ends.astype(int).reset_index(drop=True), values
