<!-- Généré par carte_phases.py. Ne pas éditer à la main. -->

# Phase 6: Agents, network, the service

`ms-06-service` · school milestones 7 and 8 · 5 sub-modules, 0 written · 0 exercises

The school's milestones 7 and 8, which close the common core. The agents and transcendence become service exercises there: cost per million tokens, latency per request, monitoring. It is an operator's view of a model, the one who pays the bill and carries the pager.

**Skills this phase builds**

- Cost per million tokens compared across models and providers
- A Kubernetes controller written in Go
- A model served and monitored, metrics in Prometheus

**Done when.** Agent Smith's report gives, per model and per provider, the cost per million tokens and the latency per request, with the source and date of each price. `transcendance` is validated, its part serves a model whose metrics land in Prometheus, and its real hours stayed under one hundred and twenty.

| Sub-module | Layer | What it covers | Where the work is |
|---|---|---|---|
| `t42-08-flyin` | imposed | Validate `fly-in` at the perimeter of its subject, the toll's mark being the only objective | 42 subject, not published |
| `t42-09-agent-smith` | imposed | Pass `agent smith` within the scope of its subject, and make its report carry the cost per million tokens of each model compared | 42 subject, not published |
| `t42-10-answer-protocol` | imposed | Pass `answer protocol` as a group, in Go if the group agrees, a TCP server faithful to the protocol and two clients | 42 subject, not published |
| `go-02-controller` | added | Write a controller with controller-runtime like AIBrix's: a custom resource the API server validates, an owned Deployment reconciled without needless writes, a status, conditions and a finalizer, a pure scaling rule tested by table, then the loop closed on pod metrics, all graded by envtest under go test -race, without Docker | planned, not written yet |
| `t42-11-transcendence` | imposed | Cross `transcendance` fast and cleanly, taking the serving and monitoring part, under a ceiling of 120 hours | 42 subject, not published |

Rows follow the order of the work; work done alongside the sequence comes last. Every English sentence on this page is translated from the curriculum's French and stored with a fingerprint of its source, so a changed source stops the page from being rebuilt.

## Reading

What each sub-module points at, straight from the curriculum. Links only: why a given one is there is written in French, next to the curriculum itself, and translating it would put the same sentence in two places waiting to disagree. A sub-module absent from this table has nothing declared yet, and a resource that lives in a repository you cannot open is left out rather than linked to a 404.

| Sub-module | Points at |
|---|---|
| `go-02-controller` | [The Kubebuilder Book](https://book.kubebuilder.io/) · book<br>[Kubebuilder, Configuring EnvTest](https://book.kubebuilder.io/reference/envtest.html) · docs<br>[kubernetes-sigs/controller-runtime](https://github.com/kubernetes-sigs/controller-runtime) · repo<br>[Kubernetes, the Horizontal Pod Autoscaler](https://kubernetes.io/docs/concepts/workloads/autoscaling/horizontal-pod-autoscale/) · docs<br>[vllm-project/aibrix/pkg/controller/kvcache/kvcache_controller.go](https://github.com/vllm-project/aibrix/blob/main/pkg/controller/kvcache/kvcache_controller.go) · repo<br>[vllm-project/aibrix/pkg/controller/podautoscaler/algorithm](https://github.com/vllm-project/aibrix/tree/main/pkg/controller/podautoscaler/algorithm) · repo<br>[vllm-project/aibrix/docs/source/designs/aibrix-autoscaler.rst](https://github.com/vllm-project/aibrix/blob/main/docs/source/designs/aibrix-autoscaler.rst) · docs<br>[llm-d/llm-d-router/blob/v1.0.0/pkg/epp/controller/pod_reconciler.go](https://github.com/llm-d/llm-d-router/blob/v1.0.0/pkg/epp/controller/pod_reconciler.go) · repo |
| `t42-11-transcendence` | [OpenTelemetry, Python, Getting Started](https://opentelemetry.io/docs/languages/python/getting-started/) · docs |

---

← [ms-05-contribution](../ms-05-contribution) · [the roadmap](../README.md) · [ms-07-cpu](../ms-07-cpu) →
