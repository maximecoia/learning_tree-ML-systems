"""Corpus preparation for L1: from a raw source to three frozen splits.

    python3 prepare.py            fetch the source if missing, then prepare

The corpus is Jules Verne, Vingt mille lieues sous les mers, Project
Gutenberg eBook #5097, in French. The raw file is not in this repository: the
script fetches it from SOURCE['url'] into source/, and refuses it unless its
SHA-256 is the one pinned below, so a third party rebuilds the same bytes.

It reads the source declared in SOURCE below, and writes into OUT:

    train.txt  dev.txt  test.txt   the three splits, UTF-8
    vocab.json                     the frozen vocabulary, one symbol per id
    manifest.json                  everything a third party needs to check
                                   that they rebuilt the same thing

THE PIPELINE, in the order the L1 course imposes, and why this order

    1  decode        bytes -> text, one declared encoding, strict
    2  clean         written transformations only, each one counted
    3  scrub         e-mail addresses and phone numbers out
    4  deduplicate   one copy of each long paragraph, BEFORE the split
    5  split         contiguous 90 / 5 / 5, cut between paragraphs
    6  freeze        the vocabulary, and an exact round trip on each split
    7  measure       the three numbers to know before training
    8  prove         SHA-256 of the source, of every output, of this script

    Decoding comes first because the same paragraph in two encodings has two
    hashes and escapes deduplication. Deduplication comes before the split
    because a duplicate straddling the cut is exactly the leak to avoid: the
    model recites on test what it read in train, and the test loss looks
    better than the model is.

WHAT MAKES IT REPLAYABLE

    The script, not the output, is the proof: a file says what was obtained,
    only a program says how. Every transformation lives in the code below,
    none by hand, and the manifest records the source hash, so a third party
    who fetches the same source and runs this file gets the same bytes. Run it
    twice: the manifest's output hashes do not move.

SWITCHING TO YOUR CORPUS

    Edit SOURCE, and nothing else. The script refuses to run while the
    licence field is empty: publishing the repo redistributes the corpus, so
    the licence is checked before, not after.

Written against Python 3.12. The preparation itself needs no torch; only
load(), which hands the splits to gpt.py, imports it.
"""

# --- the libraries ----------------------------------------------------------
# Standard library only. The preparation must run on any machine a third
# party has, before they install anything.
import hashlib      # SHA-256: the fingerprint of a file, or of a paragraph
import json         # manifest.json and vocab.json, readable by anyone
import math         # math.log for ln(V) and for the bigram loss
import os           # paths and folders
import platform     # the Python version, written into the manifest
import random       # shuffles DOCUMENTS only, and only with the seed below
import re           # the patterns of the cleaning and scrubbing steps
import sys          # sys.exit with a message when a check refuses
import unicodedata  # NFC normalization, and the category of each character

# --- the source: the only block to edit for your corpus ---------------------
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = HERE

SOURCE = {
    # A short name: it names the output folder.
    'name': 'verne',
    # A .txt file for one continuous text, or a folder of .txt files, one
    # document each. The split is not the same in the two cases, see split().
    'path': os.path.join(ROOT, 'source', 'pg5097.txt'),
    'url': 'https://www.gutenberg.org/cache/epub/5097/pg5097.txt',
    'author': 'Jules Verne (1828-1905); Project Gutenberg eBook #5097, '
              'credits Norm Wolcott, updated 2022-06-07',
    # Required. The script stops while this is empty.
    'licence': 'public domain: Verne died in 1905, and Project Gutenberg marks '
               'the eBook public domain in the USA. The Gutenberg header and '
               'licence are removed by strip_gutenberg below, so the published '
               'splits carry no Project Gutenberg trademark',
    'acquired': '2026-10-01',
    # The encoding the source is declared in. Decoding is strict: one invalid
    # byte stops the script instead of turning into a silent '?'.
    'encoding': 'utf-8',
    # The fingerprint of the raw bytes. Empty on the first run: the script
    # prints it, you paste it here, and from then on a different file under
    # the same path is refused.
    'sha256': '53507b025cd3580f4fbfa546baabb36f25adfb48b581c5b5016d91ad69d36c68',
}

OUT = os.path.join(HERE, 'data', SOURCE['name'])

# --- the decisions, each one written once -----------------------------------
SPLIT = (0.90, 0.05, 0.05)   # train, dev, test, in characters
SEED = 1337                  # used only to shuffle documents; a single
                             # continuous text is split without any draw
MIN_DEDUP_CHARS = 64         # paragraphs shorter than this are not deduplicated,
                             # see deduplicate() for the measurement behind it
MIN_CORPUS_CHARS = 100_000   # below this the script refuses: a toy GPT has more
                             # parameters than the corpus has positions to predict
                             # and recites before it learns
WARN_CORPUS_CHARS = 300_000  # below this it warns: a few hundred thousand
                             # characters is the reasonable floor
EMAIL = re.compile(r'[\w.+-]+@[\w-]+(?:\.[\w-]+)+')
# 9 to 15 digits, with optional single spaces, dots or dashes between them,
# and an optional leading +. Nine digits minimum keeps years and short
# numbers out. It will also catch a long serial number: every match is
# counted and the first ones are printed, so a human checks the catch.
PHONE = re.compile(r'(?<![\w+])\+?\d(?:[ .-]?\d){8,14}(?!\w)')
EMAIL_TOKEN = '<email>'
PHONE_TOKEN = '<phone>'


def sha256_bytes(data):
    """The hex SHA-256 of some bytes: 64 characters that change entirely
    when a single byte of the input changes."""
    return hashlib.sha256(data).hexdigest()


def sha256_file(path):
    with open(path, 'rb') as f:
        return sha256_bytes(f.read())


def refuse(message):
    """Stop with a sentence rather than a traceback: a refusal is a decision
    of the pipeline, not a bug."""
    sys.exit('REFUSED  ' + message)


# --- 1. decode ------------------------------------------------------------
def read_source(path, encoding):
    """(documents, raw_sha256, raw_bytes). One document for a file, one per
    .txt file for a folder, in sorted name order so the order never depends
    on the file system."""
    if os.path.isdir(path):
        names = sorted(n for n in os.listdir(path) if n.endswith('.txt'))
        paths = [os.path.join(path, n) for n in names]
    elif os.path.isfile(path):
        paths = [path]
    else:
        refuse('source not found: %s. Fetch it from %s' % (path, SOURCE['url']))
    raws = [open(p, 'rb').read() for p in paths]
    # For a folder, the fingerprint covers the names and the bytes, so a
    # renamed or reordered document changes it.
    h = hashlib.sha256()
    for p, raw in zip(paths, raws):
        h.update(os.path.basename(p).encode('utf-8') + b'\0' + raw + b'\0')
    digest = h.hexdigest() if len(paths) > 1 else sha256_bytes(raws[0])
    documents = []
    for p, raw in zip(paths, raws):
        try:
            # errors='strict' is the default, written out because it is the
            # decision: a byte the encoding cannot read is an error, never
            # a replacement character that would enter the vocabulary.
            documents.append(raw.decode(encoding, errors='strict'))
        except UnicodeDecodeError as e:
            refuse('%s is not valid %s at byte %d. Declare the right encoding '
                   'in SOURCE' % (p, encoding, e.start))
    return documents, digest, sum(len(r) for r in raws)


# --- 2. clean -------------------------------------------------------------
# Each step is a function text -> text, and clean() counts what each one
# changed. A transformation that is not written here does not happen, and
# one that happens is in the manifest with its count.
def normalize_newlines(text):
    # Windows writes \r\n and old Macs \r. Left alone, '\r' becomes a
    # symbol of the vocabulary that carries no meaning.
    return text.replace('\r\n', '\n').replace('\r', '\n')


def normalize_unicode(text):
    # 'é' can be one code point, U+00E9, or two, 'e' followed by the
    # combining accent U+0301. They print the same and are two different
    # symbols to the model. NFC composes them into one, always the same.
    return unicodedata.normalize('NFC', text)


def drop_invisible(text):
    # Unicode categories Cc (control) and Cf (format): the byte order mark
    # U+FEFF, zero-width spaces, stray control bytes. Invisible in an
    # editor, real symbols for the model. Newline and tab are kept.
    return ''.join(c for c in text
                   if c in '\n\t' or unicodedata.category(c) not in ('Cc', 'Cf'))


GUTENBERG_START = re.compile(r'^\*\*\* START OF THE PROJECT GUTENBERG EBOOK .*\*\*\*$', re.M)
GUTENBERG_END = re.compile(r'^\*\*\* END OF THE PROJECT GUTENBERG EBOOK .*\*\*\*$', re.M)


def strip_gutenberg(text):
    # Keep only what lies between the START and END lines of Project
    # Gutenberg. Above them: the eBook's metadata and conditions of use;
    # below them: the full Project Gutenberg licence, about 19 000
    # characters of English legal text that is not Verne and that every
    # Gutenberg file repeats. Refuses rather than guesses when a marker is
    # missing, since a silent pass-through would publish the licence.
    start, end = GUTENBERG_START.search(text), GUTENBERG_END.search(text)
    if not start or not end or end.start() < start.end():
        refuse('the Project Gutenberg START and END lines were not found in order')
    return text[start.end():end.start()]


def strip_trailing_spaces(text):
    # Spaces at the end of a line are invisible and inconsistent. Removing
    # them also turns a line of spaces into an empty line, which is what
    # makes the paragraph cut below reliable.
    return '\n'.join(line.rstrip(' \t') for line in text.split('\n'))


def collapse_blank_lines(text):
    # Three newlines or more become two: one blank line, and only one,
    # separates two paragraphs. The paragraph is the unit of the
    # deduplication and of the split, so its boundary has one spelling.
    return re.sub(r'\n{3,}', '\n\n', text)


def unwrap_paragraphs(text):
    # The eBook breaks its lines at about 72 columns and centres its titles
    # with leading spaces. Those breaks belong to the 2004 typesetting, not
    # to Verne: left in, the model spends capacity learning where a line of
    # that edition ended. Inside a paragraph every line is stripped and the
    # lines are joined with one space, and runs of spaces collapse to one,
    # which also flattens the column alignment of the table of contents.
    # Paragraph boundaries, one blank line, are untouched.
    out = []
    for p in text.split('\n\n'):
        line = ' '.join(l.strip() for l in p.split('\n') if l.strip())
        out.append(re.sub(r' {2,}', ' ', line))
    return '\n\n'.join(p for p in out if p).strip('\n')


CLEANING = [normalize_newlines, strip_gutenberg, normalize_unicode, drop_invisible,
            strip_trailing_spaces, collapse_blank_lines, unwrap_paragraphs]


def clean(documents):
    """Apply every step to every document. Returns (documents, counts), with
    the number of characters each step removed or rewrote."""
    counts = {}
    for step in CLEANING:
        before = sum(len(d) for d in documents)
        changed = 0
        out = []
        for d in documents:
            new = step(d)
            # A step can rewrite without changing the length, NFC for
            # instance on some scripts: count differing positions too.
            changed += (abs(len(d) - len(new)) if len(d) != len(new)
                        else sum(1 for a, b in zip(d, new) if a != b))
            out.append(new)
        documents = out
        counts[step.__name__] = {'chars_changed': changed,
                                 'chars_after': sum(len(d) for d in documents),
                                 'chars_before': before}
    return documents, counts


# --- 3. scrub personal data -----------------------------------------------
def scrub(documents):
    """Replace e-mail addresses and phone numbers by a fixed token.

    A model restitutes what it saw, and a rare but exact number is precisely
    what it can recite. Keeping the corpus private does not help once the
    weights are public. Returns (documents, report), the report holding the
    counts and the first matches, for a human to check the catch.
    """
    report = {}
    for label, pattern, token in (('email', EMAIL, EMAIL_TOKEN),
                                  ('phone', PHONE, PHONE_TOKEN)):
        found = [m for d in documents for m in pattern.findall(d)]
        documents = [pattern.sub(token, d) for d in documents]
        report[label] = {'replaced': len(found), 'first': found[:5]}
    return documents, report


# --- 4. deduplicate -------------------------------------------------------
def paragraphs(text):
    # After collapse_blank_lines, exactly one blank line separates two
    # paragraphs, so split and join are exact inverses of each other.
    return text.split('\n\n')


def deduplicate(documents):
    """Keep the first copy of every paragraph of at least MIN_DEDUP_CHARS.

    One pass, one dictionary of hashes: the first time a paragraph is seen
    its hash goes in, every later copy is dropped, whatever document it is
    in. A repetition threshold ("drop what appears 3 times or more") would
    let through the single duplicate, the one that leaks between train and
    test.

    Why a length floor, measured on Tiny Shakespeare on 2026-09-28: its 74
    exact duplicate paragraphs are all speaker names alone on their line,
    'GLOUCESTER:' 18 times, 'LUCIO:' 10 times, none longer than 43
    characters. Dropping them deletes the labels of the dialogue and removes
    no passage the model could recite. A paragraph shorter than 64
    characters, two contexts of 32, is kept; the manifest still counts it.
    """
    seen = set()
    kept_documents = []
    dropped, dropped_chars, short_repeats = 0, 0, 0
    for d in documents:
        kept = []
        for p in paragraphs(d):
            key = hashlib.sha256(p.encode('utf-8')).digest()
            if key in seen:
                if len(p) >= MIN_DEDUP_CHARS:
                    dropped += 1
                    dropped_chars += len(p)
                    continue
                short_repeats += 1
            seen.add(key)
            kept.append(p)
        kept_documents.append('\n\n'.join(kept))
    return kept_documents, {'dropped_paragraphs': dropped,
                            'dropped_chars': dropped_chars,
                            'short_repeats_kept': short_repeats,
                            'min_chars': MIN_DEDUP_CHARS}


# --- 5. split -------------------------------------------------------------
def cut_points(sizes, fractions):
    """Indexes where the cumulative size first reaches each fraction."""
    total = sum(sizes)
    cuts, acc = [], 0
    goals = [total * sum(fractions[:k + 1]) for k in range(len(fractions) - 1)]
    for i, s in enumerate(sizes):
        acc += s
        while goals and acc >= goals[0]:
            cuts.append(i + 1)
            goals.pop(0)
    return cuts


def split(documents):
    """(train, dev, test) as three strings.

    One continuous text: contiguous slices, cut between two paragraphs, never
    inside one. A draw character by character would put the two halves of a
    sentence on both sides, and the validation would measure nothing: every
    test character would have its neighbours in train. No draw, so no seed.

    Several documents: the document is the unit of independence. They are
    shuffled with SEED, then cut at document boundaries, so no document is
    ever split. Without the written seed two runs would have two different
    test sets, and their losses would no longer compare.
    """
    if len(documents) == 1:
        units = paragraphs(documents[0])
    else:
        units = list(documents)
        random.Random(SEED).shuffle(units)   # a private generator, seeded
    joiner = '\n\n'                         # one blank line between units
    sizes = [len(u) + len(joiner) for u in units]
    a, b = cut_points(sizes, SPLIT)
    parts = (units[:a], units[a:b], units[b:])
    if not all(parts):
        refuse('a split is empty: the corpus has too few units to cut 90/5/5')
    return tuple(joiner.join(p) for p in parts)


# --- 6. freeze the vocabulary ---------------------------------------------
def build_vocab(*texts):
    """Every distinct character of the whole corpus, sorted.

    Built on the three splits together: the vocabulary depends on the
    corpus, not on the cut, and a symbol seen only in test must still have
    an id. Sorting makes the ids independent of the reading order.
    """
    return sorted(set(''.join(texts)))


def codecs(vocab):
    """(encode, decode): characters to ids and back, through the table."""
    to_id = {c: i for i, c in enumerate(vocab)}
    return (lambda s: [to_id[c] for c in s],
            lambda ids: ''.join(vocab[i] for i in ids))


# --- 7. the three numbers to know before training -------------------------
def bigram_loss(train_ids, dev_ids, V):
    """Dev cross-entropy of a counted bigram, add-one smoothed.

    The cheapest measure of how hard a corpus is, and the level the GPT has
    to beat: it sees only what one character says about the next. Same
    formula as gpt.bigram_dev_loss, in plain Python so the preparation needs
    no torch. The +1 keeps a pair never seen in train from probability zero.
    """
    counts = [[1] * V for _ in range(V)]
    for a, b in zip(train_ids, train_ids[1:]):
        counts[a][b] += 1
    totals = [sum(row) for row in counts]
    pairs = list(zip(dev_ids, dev_ids[1:]))
    return -sum(math.log(counts[a][b] / totals[a]) for a, b in pairs) / len(pairs)


# --- 8. write and prove ---------------------------------------------------
def write_text(path, text):
    # newline='' writes '\n' as '\n' on every system: without it, Windows
    # would write '\r\n' and the output hashes would differ by machine.
    with open(path, 'w', encoding='utf-8', newline='') as f:
        f.write(text)


def fetch(path, url):
    """Download the source once, when it is missing. Nothing is trusted from
    the download itself: main() compares its SHA-256 with the pinned one, so
    a changed file on the server is refused, not silently used."""
    import urllib.request
    os.makedirs(os.path.dirname(path), exist_ok=True)
    print('fetch    %s' % url)
    with urllib.request.urlopen(url, timeout=60) as response:
        data = response.read()
    with open(path, 'wb') as f:
        f.write(data)


def main():
    if not SOURCE['licence'].strip():
        refuse('SOURCE has no licence. Check it before anything else: '
               'publishing the repo redistributes the corpus')
    if not os.path.exists(SOURCE['path']):
        fetch(SOURCE['path'], SOURCE['url'])

    documents, raw_sha, raw_bytes = read_source(SOURCE['path'], SOURCE['encoding'])
    print('source   %s, %d bytes, %d document(s)' % (SOURCE['name'], raw_bytes, len(documents)))
    print('sha256   %s' % raw_sha)
    if SOURCE['sha256'] and SOURCE['sha256'] != raw_sha:
        refuse('the source is not the declared one. Expected %s' % SOURCE['sha256'])
    if not SOURCE['sha256']:
        print('         paste this hash into SOURCE["sha256"] to pin the source')

    documents, cleaning = clean(documents)
    documents, scrubbing = scrub(documents)
    documents, dedup = deduplicate(documents)
    train, dev, test = split(documents)

    corpus_chars = len(train) + len(dev) + len(test)
    if corpus_chars < MIN_CORPUS_CHARS:
        refuse('%d characters, under the floor of %d' % (corpus_chars, MIN_CORPUS_CHARS))

    vocab = build_vocab(train, dev, test)
    encode, decode = codecs(vocab)
    ids = {name: encode(text) for name, text in (('train', train), ('dev', dev), ('test', test))}
    for name, text in (('train', train), ('dev', dev), ('test', test)):
        # The exact round trip: decode(encode(x)) == x on every split, or
        # the model is trained on something else than the text published.
        if decode(ids[name]) != text:
            refuse('the round trip is broken on %s' % name)
    V = len(vocab)
    bigram = bigram_loss(ids['train'], ids['dev'], V)

    os.makedirs(OUT, exist_ok=True)
    outputs = {}
    for name, text in (('train', train), ('dev', dev), ('test', test)):
        path = os.path.join(OUT, name + '.txt')
        write_text(path, text)
        outputs[name + '.txt'] = {'chars': len(text), 'sha256': sha256_file(path)}
    vocab_path = os.path.join(OUT, 'vocab.json')
    write_text(vocab_path, json.dumps(vocab, ensure_ascii=False))
    outputs['vocab.json'] = {'symbols': V, 'sha256': sha256_file(vocab_path)}

    manifest = {
        'source': {**SOURCE, 'path': os.path.relpath(SOURCE['path'], ROOT),
                   'sha256': raw_sha, 'bytes': raw_bytes, 'documents': len(documents)},
        'decisions': {'split': SPLIT, 'seed': SEED, 'min_dedup_chars': MIN_DEDUP_CHARS,
                      'min_corpus_chars': MIN_CORPUS_CHARS,
                      'email_token': EMAIL_TOKEN, 'phone_token': PHONE_TOKEN},
        'cleaning': cleaning,
        'scrubbing': scrubbing,
        'deduplication': dedup,
        'numbers': {'vocab_size': V, 'ln_V': math.log(V),
                    'bigram_dev_loss': bigram, 'corpus_chars': corpus_chars},
        'outputs': outputs,
        'environment': {'python': platform.python_version(),
                        'unicode': unicodedata.unidata_version,
                        'script_sha256': sha256_file(os.path.abspath(__file__))},
    }
    manifest_path = os.path.join(OUT, 'manifest.json')
    write_text(manifest_path, json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')

    for step, c in cleaning.items():
        print('clean    %-22s %7d chars changed' % (step, c['chars_changed']))
    for label, r in scrubbing.items():
        print('scrub    %-22s %7d replaced   %s' % (label, r['replaced'], r['first']))
    print('dedup    %d paragraphs dropped, %d chars; %d short repeats kept'
          % (dedup['dropped_paragraphs'], dedup['dropped_chars'], dedup['short_repeats_kept']))
    for name in ('train', 'dev', 'test'):
        print('split    %-5s %9d chars  %5.2f %%' % (name, len(ids[name]), 100 * len(ids[name]) / corpus_chars))
    print('V        %d   ln(V) %.4f   bigram dev %.4f' % (V, math.log(V), bigram))
    if corpus_chars < WARN_CORPUS_CHARS:
        print('WARNING  %d characters: under the reasonable floor of %d' % (corpus_chars, WARN_CORPUS_CHARS))
    print('wrote    %s' % os.path.relpath(OUT, ROOT))


# --- the door gpt.py goes through -----------------------------------------
def load(out_dir):
    """(train, dev, test, vocab, encode, decode), the splits as torch tensors.

    Every output is checked against the manifest first: a split edited by
    hand after the preparation is refused, because it is no longer what the
    manifest, and so the report, says the model saw.
    The test split is returned but must be read once, at the very end:
    every look at it to choose a setting turns it, slowly and invisibly,
    into a second training set.
    """
    import torch
    with open(os.path.join(out_dir, 'manifest.json'), encoding='utf-8') as f:
        manifest = json.load(f)
    for name, info in manifest['outputs'].items():
        if sha256_file(os.path.join(out_dir, name)) != info['sha256']:
            refuse('%s differs from the manifest: rerun prepare.py' % name)
    with open(os.path.join(out_dir, 'vocab.json'), encoding='utf-8') as f:
        vocab = json.load(f)
    encode, decode = codecs(vocab)
    splits = []
    for name in ('train', 'dev', 'test'):
        with open(os.path.join(out_dir, name + '.txt'), encoding='utf-8', newline='') as f:
            # dtype long: embedding indices are integers.
            splits.append(torch.tensor(encode(f.read()), dtype=torch.long))
    return (*splits, vocab, encode, decode)


if __name__ == '__main__':
    main()
