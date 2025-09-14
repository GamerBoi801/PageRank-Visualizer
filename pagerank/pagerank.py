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

    #checking if the dir exists or not
    if not os.path.exists(directory):
        raise FileNotFoundError(f"Directory '{directory}' does not exist.")
    
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
    linked to by `page`.
    
      With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    new_list = dict()
    
    links = corpus[page]
    prob = dict()
    N = len(corpus)


    #checking to see if it has no links
    if len(links) <= 0:
        for p in corpus:
            prob[p] = 1 / N
    
    #now for pages more than 1
    else:
        #check if the current page ahs any outgoing links  
        L = len(links)
        for page in corpus:
            if page in links:
                prob[page] = damping_factor * (1/L) + (1-damping_factor) * (1/N)
            else:
                prob[page] = (1 - damping_factor) * (1/N)
    
    return prob
    


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # pagerank(page) = no. of times page visited / n

    
    #first sample is randomly chosen
    first_random_choice = random.choice(list(corpus.keys()))
    current_page = first_random_choice
    
    pages_visited = {page: 0 for page in corpus}
    pages_visited[current_page] += 1

    # n is the no. of steps in surfing simulation
    for i in range(1, n):
        probabilities = transition_model(corpus, current_page, damping_factor)
        names = probabilities.keys()
        probs = probabilities.values()

        next_page = random.choices(list(names), weights=list(probs), k=1)[0]
        pages_visited[next_page] += 1

        current_page = next_page

    
    #convert counts to probabilities
    for page in pages_visited:
        pages_visited[page] /= n

    return pages_visited




def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    old_pagerank = dict()

    #total no. of pages in corpus
    N = len(corpus)
    domain_names = corpus.keys()

    #first assign 1/N to every domain_name PageRank value
    for name in corpus:
        old_pagerank[name] = 1 / N

    #base case: when diff in PageRank values > 0.001

    while True:
        new_pagerank = dict()

        for page in corpus:
            temp = 0.0

            for possible_page in corpus:

                #find linked pages to that page
                links = corpus[possible_page]

                #if there r no linking page, we treat is as linking to all pages in to the corpus including itself
                if len(links) <= 0:
                    temp += float(old_pagerank[possible_page]) / N
                elif page in links:
                    #if there is linking pages, then
                    temp += float(old_pagerank[possible_page]) / len(links)


            new_pagerank[page] = (1 - damping_factor) / N + damping_factor * temp
        
        max_diff = max(abs(new_pagerank[p] - old_pagerank [p]) for p in corpus)

        if max_diff < 0.001:
            break

        old_pagerank = new_pagerank.copy()


    total = sum(new_pagerank.values())
    for page in new_pagerank:
        new_pagerank[page] /= total

    return new_pagerank

if __name__ == "__main__":
    main()
