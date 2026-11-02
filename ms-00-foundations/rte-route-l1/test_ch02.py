"""Run chapter 2's graders against my `ch02.py` instead of the book's package.

    python3 -m pytest test_ch02.py -q      # beside ch02.py, one level inside the book

Two graders here, and they are not worth the same.

`pkg/llms_from_scratch/tests/test_ch02.py` is upstream's, reused as is. It
proves one thing: the dataloader runs end to end. Its last line reads
`input_embeddings.shape == torch.Size([8, 4, 256])` -- an expression, not an
assertion -- so it cannot fail on a wrong shape, a wrong stride or a target
that is not shifted. It is kept for the one thing it does cover, and it is not
presented as more than that.

The four tests below are mine, not the book's. They assert what chapter 2
states in prose and upstream forgot to check: the target is the input shifted
by one, one window opens per start position, windows are spaced by `stride`,
and the position table broadcasts across the batch.

The book's package is not installed, so `llms_from_scratch.ch02` is a free
name. It is registered here, pointing at my file, which is what turns
upstream's `from llms_from_scratch.ch02 import create_dataloader_v1` into an
import of my answer.
"""
import importlib.util
import sys
import types
from pathlib import Path

import pytest
import tiktoken
import torch

HERE = Path(__file__).resolve().parent
UPSTREAM_TEST = Path("pkg") / "llms_from_scratch" / "tests" / "test_ch02.py"


def _book_root():
    """The clone of rasbt/LLMs-from-scratch around this directory.

    This binder reuses upstream's test and the chapter's corpus, and both belong
    to the book. So the directory holding `ch02.py` and this file must sit one
    level inside a clone of the book, as `mes-reponses/` does. A missing book is
    an error and never a skip: a skipped grader reads as nothing wrong.
    """
    if (HERE.parent / UPSTREAM_TEST).is_file():
        return HERE.parent
    raise FileNotFoundError(
        f"rasbt/LLMs-from-scratch is not around this directory: {HERE.parent / UPSTREAM_TEST} "
        "is missing. Copy this directory into a clone of the book and run again.")


UPSTREAM_ROOT = _book_root()
UPSTREAM_TESTS = UPSTREAM_ROOT / UPSTREAM_TEST
CORPUS_DIR = UPSTREAM_ROOT / "ch02" / "01_main-chapter-code"

BATCH_SIZE = 8
MAX_LENGTH = 4
STRIDE = 4
VOCAB_SIZE = 50257
OUTPUT_DIM = 256
CONTEXT_LENGTH = 1024


def _register(answer):
    """Publish `answer` under the name upstream imports."""
    package = sys.modules.get("llms_from_scratch")
    if package is None:
        package = types.ModuleType("llms_from_scratch")
        package.__path__ = []                   # a package, so the submodule resolves
        sys.modules["llms_from_scratch"] = package
    spec = importlib.util.spec_from_file_location("llms_from_scratch.ch02", answer)
    module = importlib.util.module_from_spec(spec)
    sys.modules["llms_from_scratch.ch02"] = module
    spec.loader.exec_module(module)
    package.ch02 = module
    return module


def _answer_under_test():
    """This directory's `ch02.py`, unless a runner registered another one.

    `blanc/verifier_ch02.py` registers the blank file before loading this binder.
    Honouring what is already in `sys.modules` is what lets the blank-file
    test measure the blank file instead of quietly importing the answer.
    """
    already = sys.modules.get("llms_from_scratch.ch02")
    if already is not None:
        return already
    answer = HERE / "ch02.py"
    if not answer.is_file():
        raise FileNotFoundError(f"the answer is missing: {answer}")
    return _register(answer)


def _load_upstream_tests():
    """Import upstream's test_ch02.py under a name of its own.

    It is one `test_ch02.py` among several in this book; importing it as
    `test_ch02` would make which one wins depend on sys.path order.
    """
    if not UPSTREAM_TESTS.is_file():
        raise FileNotFoundError(f"upstream's test is missing: {UPSTREAM_TESTS}")
    spec = importlib.util.spec_from_file_location("amont_ch02_tests", UPSTREAM_TESTS)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MINE = _answer_under_test()
UPSTREAM = _load_upstream_tests()

# Upstream's own test, re-exported so pytest collects it here.
test_dataloader = UPSTREAM.test_dataloader


@pytest.fixture(autouse=True)
def _in_corpus_dir(monkeypatch):
    """Upstream's test opens `the-verdict.txt` from the working directory and
    downloads it when it is missing. Running from where the book keeps the file
    means the suite never reaches the network."""
    monkeypatch.chdir(CORPUS_DIR)


@pytest.fixture(scope="module")
def raw_text():
    with open(CORPUS_DIR / "the-verdict.txt", "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture(scope="module")
def token_ids(raw_text):
    tokenizer = tiktoken.get_encoding("gpt2")
    return tokenizer.encode(raw_text, allowed_special={"<|endoftext|>"})


@pytest.fixture
def dataset(raw_text):
    tokenizer = tiktoken.get_encoding("gpt2")
    return MINE.GPTDatasetV1(raw_text, tokenizer, MAX_LENGTH, STRIDE)


def test_targets_are_the_inputs_shifted_by_one(dataset):
    """The whole point of the window: predicting the next token."""
    for index in (0, 1, len(dataset) // 2, len(dataset) - 1):
        inputs, targets = dataset[index]
        assert inputs.shape == torch.Size([MAX_LENGTH])
        assert targets.shape == torch.Size([MAX_LENGTH])
        assert torch.equal(inputs[1:], targets[:-1])


def test_one_window_per_start_position(dataset, token_ids):
    """The tail shorter than a window is dropped, and nothing else is."""
    expected = len(range(0, len(token_ids) - MAX_LENGTH, STRIDE))
    assert len(dataset) == expected


def test_windows_are_spaced_by_the_stride(dataset, token_ids):
    """`stride` is what decides whether two windows overlap."""
    assert dataset[0][0].tolist() == token_ids[:MAX_LENGTH]
    assert dataset[1][0].tolist() == token_ids[STRIDE:STRIDE + MAX_LENGTH]
    assert dataset[2][0].tolist() == token_ids[2 * STRIDE:2 * STRIDE + MAX_LENGTH]


def test_position_embeddings_broadcast_across_the_batch(raw_text):
    """The assertion upstream's last line is missing.

    [8, 4] token ids plus a [4, 256] position table gives [8, 4, 256], and the
    same position vector lands on every sequence of the batch.
    """
    token_embedding_layer = torch.nn.Embedding(VOCAB_SIZE, OUTPUT_DIM)
    pos_embedding_layer = torch.nn.Embedding(CONTEXT_LENGTH, OUTPUT_DIM)

    dataloader = MINE.create_dataloader_v1(
        raw_text,
        batch_size=BATCH_SIZE,
        max_length=MAX_LENGTH,
        stride=STRIDE,
        shuffle=False,
    )
    x, y = next(iter(dataloader))
    assert x.shape == torch.Size([BATCH_SIZE, MAX_LENGTH])
    assert y.shape == torch.Size([BATCH_SIZE, MAX_LENGTH])

    token_embeddings = token_embedding_layer(x)
    pos_embeddings = pos_embedding_layer(torch.arange(MAX_LENGTH))
    input_embeddings = token_embeddings + pos_embeddings

    assert input_embeddings.shape == torch.Size([BATCH_SIZE, MAX_LENGTH, OUTPUT_DIM])
    for sequence in range(BATCH_SIZE):
        added = input_embeddings[sequence] - token_embeddings[sequence]
        assert torch.allclose(added, pos_embeddings, atol=1e-6)
