"""Checks this repository using nothing but this repository.

    python3 tools/check.py            the three checks CI runs
    python3 tools/check.py --links    also ask every external link, slowly

Exit 0 when everything holds, 1 when something does not, 2 when a check could
not be carried out. The third code matters more than it looks: each check walks
a list, and a list that comes back empty would otherwise read as a clean run.

Why this file is here. Everything that validates this showcase lives in the
private corpus that produces it, because it needs the curriculum to compare
against. Three questions do not: whether the published Python parses, whether
the links between these pages resolve, and whether `.gitignore` and git agree.
A reader can run those, and so can CI, which is the point of a repository whose
own README says a check is only worth something if it can fail.

**External links are not in the CI set, on purpose.** There are 393 of them and
a third of the hosts answer 403 to anything without a browser. A red mark on a
public page because ACM dislikes scripts today teaches nobody anything, and a
check people learn to ignore is worse than no check. `--links` asks them when
someone wants to know.
"""

import ast
import pathlib
import re
import subprocess
import sys
import unicodedata

RACINE = pathlib.Path(__file__).resolve().parent.parent


def suivis(motif="*"):
    """What git tracks, which is exactly what a visitor gets.

    Asking git, rather than walking the directory, is what makes "published"
    mean published: an ignored file on someone's disk is not in the answer.
    The cost is that this needs a checkout. GitHub also hands this repository
    out as a zip, where there is no git at all, and a traceback is a poor way
    to say so.
    """
    try:
        sortie = subprocess.run(
            ["git", "-C", str(RACINE), "ls-files", motif],
            capture_output=True, text=True, check=True,
        ).stdout.split("\n")
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Code 2, not 1: nothing was found wrong, the question could not be put.
        print("This check asks git what is published, so it needs a clone rather")
        print("than a downloaded archive:")
        print("    git clone https://github.com/maximecoia/learning_tree-ML-systems")
        raise SystemExit(2) from None
    return [p for p in sortie if p]


def python_parse():
    """Every published .py file is syntactically valid Python."""
    casses = []
    for f in suivis("*.py"):
        try:
            ast.parse((RACINE / f).read_text(encoding="utf-8"))
        except SyntaxError as e:
            casses.append(f"{f}:{e.lineno}: {e.msg}")
    return len(suivis("*.py")), casses


def ancres(texte):
    """The anchors GitHub derives from a page's headings."""
    out = set()
    for _, titre in re.findall(r"^(#{1,6})\s+(.+?)\s*$", texte, re.M):
        t = re.sub(r"`|\*|\[|\]|\(.*?\)", "", titre)
        t = unicodedata.normalize("NFKD", t)
        s = "".join(c for c in t.lower() if c.isalnum() or c in " -_")
        out.add(s.strip().replace(" ", "-"))
    return out | set(re.findall(r'<a[^>]+(?:name|id)="([^"]+)"', texte))


def liens_de(texte):
    """Every markdown destination, counting nested parentheses.

    `…/Starvation_(computer_science)` is a live page whose destination holds a
    balanced pair. A pattern that stops at the first `)` cuts the URL in half
    and then reports the half it made up as broken.
    """
    for m in re.finditer(r"\]\(", texte):
        i, profondeur = m.end(), 1
        while i < len(texte) and profondeur:
            if texte[i] == "(":
                profondeur += 1
            elif texte[i] == ")":
                profondeur -= 1
            i += 1
        if profondeur == 0:
            yield texte[m.end():i - 1].strip()


def renvois_internes():
    """Every link between these pages resolves, file and anchor alike."""
    pages = {f: (RACINE / f).read_text(encoding="utf-8", errors="replace")
             for f in suivis("*.md")}
    index = {f: ancres(t) for f, t in pages.items()}
    casses, comptes = [], 0
    for f, texte in pages.items():
        for cible in liens_de(texte):
            if cible.startswith(("http://", "https://", "mailto:")):
                continue
            fichier, _, frag = cible.partition("#")
            if fichier:
                vise = (RACINE / f).parent / fichier
                try:
                    cle = str(vise.resolve().relative_to(RACINE))
                except ValueError:
                    continue
            else:
                cle = f
            comptes += 1
            if not (RACINE / cle).exists():
                casses.append(f"{f} -> {cible} (no such file)")
            elif frag and cle in index and frag not in index[cle]:
                casses.append(f"{f} -> {cible} (no such heading)")
    return comptes, casses


def regles_qui_mentent():
    """.gitignore names a file git tracks anyway, and git says nothing."""
    return [p for p in subprocess.run(
        ["git", "-C", str(RACINE), "ls-files", "--ignored", "--exclude-standard", "-c"],
        capture_output=True, text=True, check=True,
    ).stdout.split("\n") if p]


def liens_externes():
    """Ask every external address. Slow, and never part of the CI verdict."""
    import concurrent.futures
    import urllib.error
    import urllib.request

    vivant = {401, 402, 403, 429}  # gated, not gone
    adresses = sorted({c for f in suivis("*.md")
                       for c in liens_de((RACINE / f).read_text(encoding="utf-8", errors="replace"))
                       if c.startswith(("http://", "https://"))})

    def demander(url):
        for methode in ("HEAD", "GET"):
            req = urllib.request.Request(url, method=methode,
                                         headers={"User-Agent": "learning-tree-check/1.0"})
            try:
                with urllib.request.urlopen(req, timeout=20) as r:
                    return r.status
            except urllib.error.HTTPError as e:
                if methode == "HEAD":
                    continue  # several hosts answer 404 to HEAD and 200 to GET
                return e.code
            except Exception:  # noqa: BLE001
                if methode == "GET":
                    return None
        return None

    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
        codes = dict(zip(adresses, pool.map(demander, adresses)))
    morts = [(u, c) for u, c in codes.items() if c in (404, 410)]
    muets = [u for u, c in codes.items() if c is None]
    gardes = [(u, c) for u, c in codes.items() if c in vivant]
    return len(adresses), morts, muets, gardes


def main():
    echecs, impossible = 0, False

    total, casses = python_parse()
    print(f"python   {total} published files parse" if not casses
          else f"python   {len(casses)} of {total} files do not parse")
    for c in casses:
        print(f"           {c}")
    echecs += bool(casses)
    impossible |= total == 0

    total, casses = renvois_internes()
    print(f"links    {total} internal links resolve" if not casses
          else f"links    {len(casses)} of {total} internal links are broken")
    for c in casses:
        print(f"           {c}")
    echecs += bool(casses)
    impossible |= total == 0

    menteuses = regles_qui_mentent()
    print("ignore   .gitignore and git agree" if not menteuses
          else f"ignore   {len(menteuses)} tracked files that .gitignore refuses")
    for m in menteuses:
        print(f"           {m}   (git rm --cached '{m}')")
    echecs += bool(menteuses)

    if "--links" in sys.argv:
        total, morts, muets, gardes = liens_externes()
        if len(muets) > max(3, total // 10):
            print(f"external {len(muets)} of {total} addresses never answered: this is "
                  f"the network, not a verdict")
            raise SystemExit(2)
        print(f"external {total} addresses asked, {len(gardes)} gated, {len(muets)} silent")
        for u, c in sorted(morts):
            print(f"           {c}  {u}")
        echecs += bool(morts)

    if impossible:
        print("\nA check found nothing to check. That is not a pass.")
        raise SystemExit(2)
    if echecs:
        raise SystemExit(1)
    print("\nall clear")


if __name__ == "__main__":
    main()
