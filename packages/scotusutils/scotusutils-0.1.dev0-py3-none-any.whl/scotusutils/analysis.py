from scotusutils import dbtools


class SCOTUSCorpus(object):

    def populate(self, opinions = None, transcripts = None):
        """Initial population of corpus with data dump"""
        pass


def get_term_data(term):
    corpus = SCOTUSCorpus()
    opinions = dbtools.get_opinions(term = term)
    transcripts = dbtools.get_transcripts(term = term)
    corpus.populate(opinions = opinions, transcripts = transcripts)
    return corpus


def analyze_term_data(term, data):
    pass


def analyze(term):
    """Placeholder func for main analysis of term"""
    term_data = get_term_data(term = term)
    term_analysis = analyze_term_data(term = term, data = term_data)
    return {"Term" : term,
            "Data" : term_data,
            "Analysis" : term_analysis,
            }
