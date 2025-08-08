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
    distribution = {}

    # If the page has no links then assume it can go to all pages with equal probability
    if not corpus[page]:
        additional = (1 - damping_factor) / len(corpus)
        damping = damping_factor / len(corpus)
        for entry in corpus:
            distribution[entry] = distribution.get(entry, 0) + additional + damping
    else:
        # Get the random jump and the damping.
        additional = (1 - damping_factor) / len(corpus)
        damping = damping_factor / len(corpus[page])
        # Add the random jump to each page in case they are not linked
        for entry in corpus:
            distribution[entry] = additional
        # For each link in the chosen page add the damping
        for link in corpus[page]:
            distribution[link] += damping
    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    rank = {}

    # Get all the pages and initialize
    pages = []
    for entry in corpus:
        rank[entry] = 0
        pages.append(entry)

    # Choose initial page randomly and count it. Use it on the first sample
    page = random.choice(pages)
    rank[page] += 1
    sample = transition_model(corpus, page, damping_factor)
    # Loop for the samples
    for i in range(n-1):
        # Get the weights based on the sample
        weights = [sample[page] for page in pages]
        # Most probable page
        page = random.choices(pages, weights)[0]
        rank[page] += 1
        # Grab the page with the most probability
        sample = transition_model(corpus, page, damping_factor)

    # Get the distribution according to the sample size
    for page in rank:
        rank[page] /= n
    return rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    rank = {}

    # Get all the pages and initialize
    pages = []
    n = len(corpus)
    for entry in corpus:
        # Initialize as 1 / n
        rank[entry] = 1 / n
        pages.append(entry)

    # Iterate while the conversion is > 0.001
    while True:
        # Make a copy of old values
        prev_rank = rank.copy()
        # For each entry apply the formula
        for entry in rank:
            sumValues = 0
            for page in corpus:
                # If page has 0 links they divide by equally
                if not corpus[page]:
                    sumValues += rank[page] / n
                # If it has links
                elif entry in corpus[page]:
                    # Update sum with the division of the current page rank and the number of links it has
                    sumValues += rank[page] / len(corpus[page])
            # Apply the formula
            rank[entry] = ((1 - damping_factor) / n) + (damping_factor * sumValues)

        # Check if the convergence is met. If so stop iterating
        differences = [abs(prev_rank[page] - rank[page]) for page in rank]
        if max(differences) < 0.001:
            break

    return rank


if __name__ == "__main__":
    main()
