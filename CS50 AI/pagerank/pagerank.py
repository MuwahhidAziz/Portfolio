import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    linked = ( corpus[page] or set(corpus.keys()) ) | {page}
    n = len(linked)
    transition = {}
    for p in linked:
        transition[p] = (1 - damping_factor) / n + (0 if p == page else (damping_factor/(n-1)) )
    alpha = 1 / sum(transition.values())
    return {key:transition[key]*alpha for key in transition}


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages  = list(corpus.keys())
    rank = {key:0 for key in pages}
    current = random.choice(pages)
    for _ in range(n):
        rank[current] += 1
        transition = transition_model(corpus, current, damping_factor)
        current = random.choices(list(transition.keys()), list(transition.values()))[0]
    alpha = 1 / sum(rank.values())
    return {key:val*alpha for key, val in rank.items()}

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages = list(corpus.keys())
    N = len(pages)
    cnst = (1 - damping_factor) / N
    default = 1 / N
    limit = 0.001
    rank = {page:default for page in pages}
    while True:
        differences = []
        for page in pages:

            current = rank[page]
            total = 0

            for p in pages:

                links = corpus[p]

                if not links:
                    links = pages

                n = len(links)

                if page in links:
                    total += rank[p] / n

            new = cnst + damping_factor*total
            differences.append(abs(new - current))
            rank[page] = new
        if max(differences) <= limit:
            return rank


if __name__ == "__main__":
    main()
