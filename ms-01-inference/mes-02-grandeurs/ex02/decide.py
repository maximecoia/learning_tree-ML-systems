"""decide.py: which regime, which ceiling, which gain.

Reuses counts.py (compute_floor) and magnitudes.py (transfer_time):
the time a thing takes = quantity / rate, whether the quantity is
operations or bytes.
"""

from counts import compute_floor
from magnitudes import transfer_time


def regime(flops, nbytes, flops_per_s, bytes_per_s, launch_s=0.0):
    """What limits the computation: 'overhead', 'memory' or 'compute'."""
    if flops < 0 or nbytes < 0:
        raise ValueError("negative count")
    if flops_per_s <= 0 or bytes_per_s <= 0:
        raise ValueError("zero or negative rate")
    if launch_s < 0:
        raise ValueError("negative launch time")
    t_compute = compute_floor(flops, flops_per_s)
    t_bytes = transfer_time(nbytes, bytes_per_s)
    if launch_s >= max(t_compute, t_bytes):
        return "overhead"
    if t_bytes > t_compute:
        return "memory"
    return "compute"


def decode_ceiling(model_nbytes, bytes_per_s):
    """Max tokens/s when decoding: every token rereads all the weights."""
    if model_nbytes <= 0:
        raise ValueError("a model that weighs nothing")
    if bytes_per_s <= 0:
        raise ValueError("zero or negative rate")
    return bytes_per_s / model_nbytes


def batch_throughput(model_nbytes, bytes_per_s, batch):
    """Same ceiling when one read of the weights serves batch requests."""
    if batch <= 0:
        raise ValueError("empty batch")
    return batch * decode_ceiling(model_nbytes, bytes_per_s)


def amdahl(p, k):
    """Overall speedup: 1 / ((1 - p) + p/k); k may be infinite.

    No special case is needed for an infinite k: in floating point,
    p / inf is 0.0, and the formula then reduces to 1 / (1 - p).
    """
    if p < 0 or p > 1:
        raise ValueError("fraction outside 0 to 1")
    if k <= 0:
        raise ValueError("zero or negative speedup factor")
    return 1 / ((1 - p) + p / k)


def time_saved(share, saving):
    """Share of the total time removed: share × saving (fractions in 0 to 1)."""
    if not (0 <= share <= 1) or not (0 <= saving <= 1):
        raise ValueError("fraction outside 0 to 1")
    return share * saving


def in_flight(rate_per_s, latency_s):
    """Requests in flight, by Little's law: N = throughput × latency."""
    if rate_per_s < 0 or latency_s < 0:
        raise ValueError("negative value")
    return rate_per_s * latency_s


def saturates(arrival_per_s, service_per_s):
    """True when arrivals strictly exceed service."""
    if arrival_per_s < 0 or service_per_s < 0:
        raise ValueError("negative value")
    return arrival_per_s > service_per_s


def cost_per_request(price_per_hour, requests_per_hour):
    """Price of one request: hourly price divided by requests per hour."""
    if price_per_hour < 0:
        raise ValueError("negative price")
    if requests_per_hour <= 0:
        raise ValueError("a machine that serves no request")
    return price_per_hour / requests_per_hour
