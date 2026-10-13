"""Memory cost of the key-value cache."""


def _positif(valeur):
    """Check that a value is a strictly positive integer."""
    if not isinstance(valeur, int):
        raise ValueError("valeur non entière")
    if valeur <= 0:
        raise ValueError("valeur non positive")
    return valeur


def _valider_config(config):
    """Check that a model configuration is complete and consistent.

    Return the config unchanged when it is valid, raise ValueError otherwise.
    """
    for cle in ("couches", "tetes", "tetes_kv", "dim_tete", "octets_par_nombre"):
        if cle not in config:
            raise ValueError("configuration incomplète : " + cle)
        _positif(config[cle])
    if config["tetes"] % config["tetes_kv"] != 0:
        raise ValueError("tetes n'est pas un multiple de tetes_kv")
    return config


def facteur_gqa(config):
    """Number of attention heads served by one key-value pair."""
    _valider_config(config)
    return config["tetes"] // config["tetes_kv"]


def octets_par_jeton(config):
    """Cost of one context token for one sequence.

    Formula: 2 × couches × tetes_kv × dim_tete × octets_par_nombre.
    The 2 counts the keys plus the values.
    """
    _valider_config(config)
    return (
        2
        * config["couches"]
        * config["tetes_kv"]
        * config["dim_tete"]
        * config["octets_par_nombre"]
    )


def octets_du_cache(config, contexte, lots=1):
    """Total cost of the cache for `lots` sequences of `contexte` tokens.

    `contexte` may be 0 (empty cache), but not negative.
    `lots` must be a positive integer (at least 1).
    """
    _valider_config(config)
    if not isinstance(contexte, int) or contexte < 0:
        raise ValueError("contexte négatif ou non entier")
    _positif(lots)
    return lots * contexte * octets_par_jeton(config)


def octets_des_poids(parametres, octets_par_nombre):
    """Model weights in bytes: parameters × bytes per number."""
    _positif(parametres)
    _positif(octets_par_nombre)
    return parametres * octets_par_nombre


def memoire_libre(memoire_totale, octets_poids, reserve=0):
    """Memory left for the cache after the weights and the reserve.

    A negative remainder is not a zero capacity: it is a refusal.
    """
    _positif(memoire_totale)
    _positif(octets_poids)
    if not isinstance(reserve, int) or reserve < 0:
        raise ValueError("réserve négative ou non entière")
    libre = memoire_totale - octets_poids - reserve
    if libre < 0:
        raise ValueError("les poids dépassent la carte")
    return libre


def jetons_tenables(config, libre):
    """Total number of context tokens the free memory holds.

    Integer division, rounded down.
    """
    _valider_config(config)
    if not isinstance(libre, int) or libre < 0:
        raise ValueError("mémoire libre négative ou non entière")
    return libre // octets_par_jeton(config)


def sequences_tenables(config, libre, contexte):
    """Number of sequences of `contexte` tokens served together.

    `contexte` must be strictly positive: a sequence of zero tokens makes
    no sense, and the division would be impossible.
    """
    _valider_config(config)
    if not isinstance(libre, int) or libre < 0:
        raise ValueError("mémoire libre négative ou non entière")
    _positif(contexte)
    return jetons_tenables(config, libre) // contexte