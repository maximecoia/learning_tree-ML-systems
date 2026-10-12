<!-- Généré par carte_phases.py. Ne pas éditer à la main. -->

# Phase 4 — The school's AI projects, entering vLLM

`ms-03-contribution` · weeks 21–34 · 12 sub-modules, 0 written · 0 exercises

**What it buys.** milestone 6, starvation measured in Codexion under FIFO and EDF, and a first pull request in the vLLM organisation or in llm-d

**How it ends.** Not on a feeling, on one binary test: *Codexion publishes each coder's waiting times under FIFO and under EDF, and starvation reads in the numbers. L3 is open, or its postponement is written in the journal with the condition that triggered it.*

Descriptions below translate the curriculum's own `competence` field, one sentence per sub-module. Each translation is stored with a fingerprint of the French it was made from, so a source that changes stops this page from being rebuilt rather than outrunning it. Rows are in the order the work goes, read from the curriculum's `apres` and `fil` fields; work done alongside the sequence comes last.

| Sub-module | Layer | What it covers | Where the work is |
|---|---|---|---|
| `t42-05-callmemaybe` | imposed | Make Qwen3-0.6B choose a function and its arguments through constrained decoding on its logits, with valid JSON on every output, and measure what each token costs | 42 subject, not published |
| `t42-06-rag-machine` | imposed | Pass `RAG against the machine` within the scope of its subject, and keep its index of the vLLM repository as a map of the code for the contribution | 42 subject, not published |
| `t42-07-codexion` | imposed | Pass `codexion` with its FIFO and EDF schedulers, and show by measurement, with each coder's waiting times published, that starvation is ruled out under EDF | 42 subject, not published |
| `inf-08-speculatif` | added | Predict the speedup of speculative decoding from the acceptance rate and the draft length, prove it lossless against the target model, and say from what concurrency it stops paying | planned, not written yet |
| `inf-09-pagedattention` | added | Explain the paging of the KV cache as PagedAttention defines it, and say block by block which waste it removes | planned, not written yet |
| `inf-10-fragmentation` | added | Put a percentage on the memory lost to fragmentation when the KV cache is not paged, over a trace of requests whose lengths vary | planned, not written yet |
| `inf-11-compiler-vllm` | added | Build vLLM from source and run its test suite, until you know which change forces which rebuild | planned, not written yet |
| `inf-12-chemin-requete` | added | Trace a request through vLLM, from the API entry point to the token returned, naming the components it crosses and what each one decides | planned, not written yet |
| `inf-13-reproduire-bug` | added | Reproduce an open bug of the repository from its report, and cut the reproduction down to the smallest case that still triggers it | planned, not written yet |
| `inf-14-premiere-pr` | added | Open a first pull request on vLLM and carry its review through to a merge, or to a refusal whose reason you understand | planned, not written yet |
| `inf-15-choisir-issue` | added | Pick an issue whose stake is the scheduler or the cache rather than the kernel, and justify that choice by the gain expected and by what is within reach | planned, not written yet |
| `l3-01-contribution` | proof | Open a pull request in an upstream inference engine, engage its review, and publish the measured gain it brings | planned, not written yet |

## Reading

What each sub-module points at, straight from the curriculum. Links only: why a given one is there is written in French, next to the curriculum itself, and translating it would put the same sentence in two places waiting to disagree. A sub-module absent from this table has nothing declared yet, and a resource that lives in a repository you cannot open is left out rather than linked to a 404.

| Sub-module | Points at |
|---|---|
| `inf-08-speculatif` | [Stanford CS336, lecture 10, Inference](https://cs336.stanford.edu/lectures/?trace=lecture_10) · course<br>[Sharon Zhou, Transformers in Practice](https://www.deeplearning.ai/courses/transformers-in-practice) · course<br>[Hugging Face, Assisted Generation](https://huggingface.co/blog/assisted-generation) · article<br>[Harvard CS249r, Machine Learning Systems at Scale, the Inference at Scale chapter](https://mlsysbook.ai/vol2/inference/inference.html) · book<br>[GPU MODE, lecture 22, Hacker's Guide to Speculative Decoding in vLLM, Cade Daniel](https://www.youtube.com/watch?v=9wNAgpX6z_4) · video<br>[Maarten Grootendorst, A Visual Guide to Gemma 4](https://newsletter.maartengrootendorst.com/p/a-visual-guide-to-gemma-4) · article<br>[Stanford CME295, lecture 3 on video, Fall 2025, Transformers & Large Language Models](https://www.youtube.com/watch?v=Q5baLehv5So) · video |
| `inf-09-pagedattention` | [UC Berkeley, vLLM: Easy, Fast, and Cheap LLM Serving with PagedAttention](https://blog.vllm.ai/blog/2023-06-20-vllm) · article<br>[Stanford CS336, lecture 10, Inference](https://cs336.stanford.edu/lectures/?trace=lecture_10) · course<br>[Harvard CS249r, Machine Learning Systems at Scale, the Inference at Scale chapter](https://mlsysbook.ai/vol2/inference/inference.html) · book<br>[JINO-ROHIT/nano-paged-attention](https://github.com/JINO-ROHIT/nano-paged-attention) · repo<br>[JINO-ROHIT/ORCA](https://github.com/JINO-ROHIT/ORCA) · repo<br>[vLLM, Automatic Prefix Caching](https://docs.vllm.ai/en/latest/design/prefix_caching/) · docs<br>[Stanford CME295, lecture 3 on video, Fall 2025, Transformers & Large Language Models](https://www.youtube.com/watch?v=Q5baLehv5So) · video |
| `inf-10-fragmentation` | [JINO-ROHIT/nano-paged-attention](https://github.com/JINO-ROHIT/nano-paged-attention) · repo<br>[CMU 15-213, Dynamic Memory Allocation: Basic](https://www.cs.cmu.edu/~213/lectures/13-malloc-basic.pdf) · course<br>[CMU 11-868, Woosuk Kwon, Efficient LLM Inference with Paged Attention and vLLM](https://llmsystem.github.io/llmsystem2026spring/assets/files/llmsys-24-vLLM_woosuk_kwon-b6a0750bb310949461ba5a635a1126eb.pdf) · course<br>[Zachary DeVito, A guide to PyTorch's CUDA Caching Allocator](https://zdevito.github.io/2022/08/04/cuda-caching-allocator.html) · article |
| `inf-11-compiler-vllm` | [vLLM, Contributing to vLLM, Developing](https://docs.vllm.ai/en/latest/contributing/#developing) · docs<br>[vLLM, GPU Installation, Python-only build](https://docs.vllm.ai/en/latest/getting_started/installation/gpu/#python-only-build) · docs<br>[vLLM, Incremental Compilation Workflow](https://docs.vllm.ai/en/latest/contributing/incremental_build/) · docs<br>[vLLM, CPU Installation, Apple silicon](https://docs.vllm.ai/en/latest/getting_started/installation/cpu/#apple-silicon) · docs<br>[vLLM, torch.compile integration](https://docs.vllm.ai/en/latest/design/torch_compile/#compilation-cache) · docs |
| `inf-12-chemin-requete` | [CMU 11-868, Woosuk Kwon, Efficient LLM Inference with Paged Attention and vLLM](https://llmsystem.github.io/llmsystem2026spring/assets/files/llmsys-24-vLLM_woosuk_kwon-b6a0750bb310949461ba5a635a1126eb.pdf) · course<br>[AI Engineer World's Fair 2026, Charles Frye, What Is an Inference Engine, Anyway?](https://www.youtube.com/watch?v=woIYJYd_etI) · video<br>[Aleksa Gordić, Inside vLLM: Anatomy of a High-Throughput LLM Inference System](https://www.aleksagordic.com/blog/vllm) · article<br>[GeeeekExplorer/nano-vllm](https://github.com/GeeeekExplorer/nano-vllm) · repo<br>[vLLM, Architecture Overview](https://docs.vllm.ai/en/latest/design/arch_overview/) · docs |
| `inf-13-reproduire-bug` | [vllm-project/vllm/.github/ISSUE_TEMPLATE/400-bug-report.yml](https://github.com/vllm-project/vllm/blob/main/.github/ISSUE_TEMPLATE/400-bug-report.yml) · docs<br>[vLLM, CI Failures](https://docs.vllm.ai/en/latest/contributing/ci/failures/) · docs<br>[vLLM, How to debug the vLLM-torch.compile integration](https://docs.vllm.ai/en/latest/design/debug_vllm_compile/) · docs<br>[vLLM, Python Multiprocessing](https://docs.vllm.ai/en/latest/design/multiprocessing/) · docs<br>[stas00/ml-engineering/debug/pytorch.md#reducing-the-number-of-layers-for-large-models](https://github.com/stas00/ml-engineering/blob/master/debug/pytorch.md#reducing-the-number-of-layers-for-large-models) · book |
| `inf-14-premiere-pr` | [vLLM, Contributing to vLLM, Pull Requests & Code Reviews](https://docs.vllm.ai/en/latest/contributing/#pull-requests-code-reviews) · docs |
| `inf-15-choisir-issue` | [vLLM, Labels](https://docs.vllm.ai/en/latest/contributing/labels/) · docs<br>[vLLM, Contributing to vLLM, Job Board](https://docs.vllm.ai/en/latest/contributing/#job-board) · docs |
| `l3-01-contribution` | [vllm-project/vllm/.github/PULL_REQUEST_TEMPLATE.md](https://github.com/vllm-project/vllm/blob/main/.github/PULL_REQUEST_TEMPLATE.md) · docs |

---

← [ms-02-infrastructure](../ms-02-infrastructure) · [the roadmap](../README.md) · [ms-04-agents-reseau](../ms-04-agents-reseau) →
