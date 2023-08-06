from collections import defaultdict
from functools import partial
from string import Template

from scopus import AuthorSearch, ScopusSearch
from scopus.exception import Scopus400Error, ScopusQueryError, Scopus500Error

from sosia.processing import get_authors
from sosia.utils import print_progress, run


def query(q_type, q, refresh=False, first_try=True):
    """Wrapper function to perform a particular search query

    Parameters
    ----------
    q_type : str
        Determines the query search that will be used.  Allowed values:
        "author", "docs".

    q : str
        The query string.

    refresh : bool (optional, default=False)
        Whether to refresh cached files if they exist, or not.

    first_try: bool (optional, default=True)
        A flag parameter to indicate whether the function has been called
        for the first time.  If False, KeyErrors will result in abortion.

    Returns
    -------
    res : list of namedtuples
        Documents represented by namedtuples as returned from scopus.

    Raises
    ------
    ValueError:
        If q_type is none of the allowed values.
    """
    try:
        if q_type == "author":
            res = AuthorSearch(q, refresh=refresh).authors or []
        elif q_type == "docs":
            res = ScopusSearch(q, refresh=refresh).results or []
            if not valid_results(res):
                res = query("docs", q, True, False)
        return res
    except (KeyError, UnicodeDecodeError, TypeError):
        if first_try:
            return query(q_type, q, True, False)
        else:
            return []


def query_journal(source_id, years, refresh):
    """Get authors by year for a particular source.

    Parameters
    ----------
    source_id : str or int
        The Scopus ID of the source.

    years : container of int or container of str
        The relevant pulication years to search for.

    refresh : bool (optional)
        Whether to refresh cached files if they exist, or not.

    Returns
    -------
    d : dict
        Dictionary keyed by year listing all authors who published in
        that year.
    """
    try:  # Try complete publication list first
        q = 'SOURCE-ID({})'.format(source_id)
        res = query("docs", q, refresh=refresh)
    except (ScopusQueryError, Scopus500Error):  # Fall back to year-wise queries
        res = []
        for year in years:
            q = Template('SOURCE-ID({}) AND PUBYEAR IS $fill'.format(source_id))
            ext, _ = stacked_query([year], [], q, "", partial(query, "docs"),
                                   refresh=refresh)
            if not valid_results(ext):  # Reload queries with missing years
                ext, _ = stacked_query([year], [], q, "", partial(query, "docs"),
                                       refresh=True)
            res.extend(ext)
    # Sort authors by year
    d = defaultdict(list)
    for pub in res:
        try:
            year = pub.coverDate[:4]
        except TypeError:  # missing year
            continue
        d[year].extend(get_authors([pub]))  # Populate dict
    return d


def stacked_query(group, res, query, joiner, func, refresh, i=0, total=None):
    """Auxiliary function to recursively perform queries until they work.

    Parameters
    ----------
    group : list of str
        Scopus IDs (of authors or sources) for which the stacked query should
        be conducted.

    res : list
        (Initially empty )Container to which the query results will be
        appended.

    query : Template()
        A string template with one paramter named `fill` which will be used
        as search query.

    joiner : str
        On wich the group elements should be joined to fill the query.

    func : function object
        The function to be used (ScopusSearch, AuthorSearch).  Should be
        provided with partial and additional parameters.

    refresh : bool
        Whether the cached files should be refreshed or not.

    i : int (optional, default=0)
        A count variable to be used for printing the progress bar.

    total : int (optional, default=None)
        The total number of elements in the group.  If provided, a progress
        bar will be printed.

    Returns
    -------
    res : list
        A list of namedtuples representing publications.

    i : int
        A running variable to indicate the progress.

    Notes
    -----
    Results of each successful query are appended to ´res´.
    """
    group = [str(g) for g in group]  # make robust to passing int
    q = query.substitute(fill=joiner.join(group))
    try:
        res.extend(run(func, q, refresh))
        if total:  # Equivalent of verbose
            i += len(group)
            print_progress(i, total)
    except (Scopus400Error, Scopus500Error, ScopusQueryError):
        if len(group) > 1:
            mid = len(group) // 2
            params = {"group": group[:mid], "res": res, "query": query, "i": i,
                      "joiner": joiner, "func": func, "total": total,
                      "refresh": refresh}
            res, i = stacked_query(**params)
            params.update({"group": group[mid:], "i": i})
            res, i = stacked_query(**params)
        elif "AND EID(" not in q:  # skip if already passed inside here
            groupeids = ["*" + str(n) for n in range(0, 10)]
            q = Template(q + " AND EID($fill)")
            mid = len(groupeids) // 2  # split here to avoid redundant query
            params = {"group": groupeids[:mid], "res": res, "query": q, "i": i,
                      "joiner": " OR ", "func": func, "total": None,
                      "refresh": refresh}
            res, i = stacked_query(**params)
            params.update({"group": groupeids[mid:], "i": i})
            res, i = stacked_query(**params)
        else:
            return None, i
    return res, i


def valid_results(res):
    """Verify that each element ScopusSearch in `res` contains year info."""
    try:
        _ = [p for p in res if p.subtype == "ar" and int(p.coverDate[:4])]
        return True
    except:
        return False
