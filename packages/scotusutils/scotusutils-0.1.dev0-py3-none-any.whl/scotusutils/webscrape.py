
def scrape_term_opinions(term):
    pass


def store_term_opinions(opinions):
    pass


def collect_term_opinions(term):
    """Scrape & Store SCOTUS opinions for given term"""
    opinions = scrape_term_opinions(term = term)
    status = store_term_opinions(opinions = opinions)
    return status
