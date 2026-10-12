<!-- Généré par carte_phases.py. Ne pas éditer à la main. -->

# Phase 3 — Python, administration, the way in

`ms-02-infrastructure` · weeks 9–20 · 7 sub-modules, 3 written · 20 exercises

**What it buys.** milestones 4 and 5, then the Inception stack ported to Kubernetes, serving the L2 server with its metrics in Prometheus

**How it ends.** Not on a feeling, on one binary test: *Your inference server runs on a local Kubernetes, its metrics land in Prometheus, and a load test replays L2's curve, explaining the gap with the native measurement.*

Descriptions below translate the curriculum's own `competence` field, one sentence per sub-module. Each translation is stored with a fingerprint of the French it was made from, so a source that changes stops this page from being rebuilt rather than outrunning it. Rows are in the order the work goes, read from the curriculum's `apres` and `fil` fields; work done alongside the sequence comes last.

| Sub-module | Layer | What it covers | Where the work is |
|---|---|---|---|
| `t42-01-piscine-python` | imposed | Pass the eleven modules of the 2026 Python piscine, from functions to validated models, within each subject's scope: the exact names, the authorized functions, flake8, type hints checked by mypy, and the behaviour each requirement describes | 42 subject, not published · 11 exercises |
| `sh-01-b2br` | imposed | Administer a hardened machine, from encrypted partitioning to password policy, and be able to defend every choice: the subject's configuration files handed in and read, and the monitoring script run against command doubles | 42 subject, not published · 5 exercises |
| `sh-02-netpractice` | imposed | Split a network into subnets that satisfy a subject's constraints, and diagnose a configuration that does not route by naming the cause | 42 subject, not published |
| `t42-02-amazeing` | imposed | Deliver A-Maze-ing within its subject's scope: a configuration read and its errors explained, a perfect maze or a playable board with coherent walls, the shortest path written, a seed that reproduces, and the generator shipped as a reusable package | 42 subject, not published · 4 exercises |
| `t42-03-pacman` | imposed | Validate `pacman` at the perimeter of its subject, adding nothing | 42 subject, not published |
| `t42-04-inception` | imposed | Validate `inception` at the perimeter of its subject, adding nothing | 42 subject, not published |
| `ops-01-exploitation` | added | Port the Inception stack to a local Kubernetes, serve L2's inference server on it with its metrics in Prometheus, and replay its curve under load | planned, not written yet |

## Reading

What each sub-module points at, straight from the curriculum. Links only: why a given one is there is written in French, next to the curriculum itself, and translating it would put the same sentence in two places waiting to disagree. A sub-module absent from this table has nothing declared yet, and a resource that lives in a repository you cannot open is left out rather than linked to a 404.

| Sub-module | Points at |
|---|---|
| `t42-01-piscine-python` | [PEP 8, the style guide](https://peps.python.org/pep-0008/) · docs<br>[flake8, the documentation](https://flake8.pycqa.org/en/latest/) · docs<br>[mypy, the documentation](https://mypy.readthedocs.io/en/stable/) · docs<br>[Python, errors and exceptions](https://docs.python.org/3/tutorial/errors.html) · docs<br>[Python, abc, abstract base classes](https://docs.python.org/3/library/abc.html) · docs<br>[Python, typing](https://docs.python.org/3/library/typing.html) · docs<br>[Python, modules and packages](https://docs.python.org/3/tutorial/modules.html) · docs<br>[Python, venv](https://docs.python.org/3/library/venv.html) · docs<br>[Python Packaging, writing pyproject.toml](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/) · docs<br>[python-dotenv](https://pypi.org/project/python-dotenv/) · docs<br>[Pydantic, the documentation](https://docs.pydantic.dev/latest/) · docs<br>[Python, functools](https://docs.python.org/3/library/functools.html) · docs |
| `sh-01-b2br` | [42 subject, Born2beroot](https://projects.intra.42.fr/projects/born2beroot) · assignment<br>[Debian, The Debian Administrator's Handbook](https://debian-handbook.info/browse/stable/) · book<br>[sudoers, manual](https://www.sudo.ws/docs/man/sudoers.man/) · docs<br>[sshd_config, manual](https://man.openbsd.org/sshd_config) · docs<br>[pam_pwquality, manual](https://manpages.debian.org/bookworm/libpam-pwquality/pam_pwquality.8.en.html) · docs<br>[UFW, the Ubuntu documentation](https://help.ubuntu.com/community/UFW) · docs<br>[cron, the crontab manual](https://man7.org/linux/man-pages/man5/crontab.5.html) · docs |
| `sh-02-netpractice` | [42 subject, NetPractice](https://projects.intra.42.fr/projects/netpractice) · assignment<br>[freeCodeCamp, Kshitij Sharma, Computer Networking Fundamentals Course](https://www.youtube.com/watch?v=fQbBPa0ADvs) · video<br>[Practical Networking, Subnetting Mastery](https://www.practicalnetworking.net/stand-alone/subnetting-mastery/) · course<br>[Practical Networking, Packet Traveling](https://www.practicalnetworking.net/series/packet-traveling/packet-traveling/) · course<br>[RFC 950, the Internet standard subnetting procedure](https://www.rfc-editor.org/rfc/rfc950) · docs<br>[RFC 4632, Classless Inter-Domain Routing, CIDR](https://www.rfc-editor.org/rfc/rfc4632) · docs<br>[RFC 1918, address allocation for private internets](https://www.rfc-editor.org/rfc/rfc1918) · docs<br>[Wikipedia, OSI model](https://en.wikipedia.org/wiki/OSI_model) · article |
| `t42-02-amazeing` | [42 subject, A-Maze-ing](https://projects.intra.42.fr/projects/a-maze-ing) · assignment<br>[Jamis Buck, Maze Generation: Recursive Backtracking](https://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking) · article<br>[Jamis Buck, Mazes for Programmers](https://pragprog.com/titles/jbmaze/mazes-for-programmers/) · book<br>[Wikipedia, Maze generation algorithm](https://en.wikipedia.org/wiki/Maze_generation_algorithm) · article<br>[Wikipedia, Breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search) · article<br>[Python, random.Random](https://docs.python.org/3/library/random.html#random.Random) · docs<br>[Python Packaging User Guide, Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/) · docs |
| `t42-04-inception` | [freeCodeCamp, KodeKloud, Docker Tutorial for Beginners](https://www.youtube.com/watch?v=fqMOX6JJhGo) · video |
| `ops-01-exploitation` | [JINO-ROHIT/advanced_ml/12-ml-systems](https://github.com/JINO-ROHIT/advanced_ml/tree/main/12-ml-systems) · repo<br>[JINO-ROHIT/fastapi_with_celery_redis](https://github.com/JINO-ROHIT/fastapi_with_celery_redis) · repo |

---

← [ms-01-inference](../ms-01-inference) · [the roadmap](../README.md) · [ms-03-contribution](../ms-03-contribution) →
