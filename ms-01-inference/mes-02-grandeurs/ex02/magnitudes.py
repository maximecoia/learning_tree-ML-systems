"""magnitudes.py: orders of magnitude of modern systems.

Two reference tables (latencies, bandwidths) and six small functions
for back-of-the-envelope reasoning before writing any code.
"""

# Latencies in nanoseconds (ns), fastest to slowest
LATENCY_NS = {
    "l1": 1,                  # L1 cache: ~1 ns
    "l2": 4,                  # L2 cache: ~4 ns
    "l3": 20,                 # L3 cache: ~20 ns
    "ram": 100,               # main memory: ~100 ns
    "ssd": 50_000,            # NVMe SSD: ~50 µs
    "disk": 5_000_000,        # hard disk: ~5 ms
    "datacenter": 500_000,    # round trip within a datacenter: ~0.5 ms
    "continent": 150_000_000, # intercontinental round trip: ~150 ms
}

# Bandwidths in bytes per second
BANDWIDTH = {
    "ram":    100_000_000_000,    # server RAM: ~100 GB/s
    "hbm":    2_000_000_000_000,  # HBM (GPU memory): ~2 TB/s
    "pcie":   32_000_000_000,     # PCIe Gen4 x16: ~32 GB/s
    "net10g": 1_250_000_000,      # 10 Gbit/s network = 1.25 GB/s
}


def transfer_time(nbytes, bytes_per_s):
    """Time (s) to move nbytes bytes at bytes_per_s (B/s)."""
    if nbytes < 0 or bytes_per_s < 0:
        raise ValueError("negative value")
    if bytes_per_s == 0:
        raise ValueError("zero bandwidth")
    return nbytes / bytes_per_s


def link_bytes_per_s(bits_per_s):
    """Bandwidth in bytes/s of a link advertised in bits/s."""
    if bits_per_s < 0:
        raise ValueError("negative value")
    return bits_per_s / 8


def model_bytes(params, bits):
    """Size in bytes of params parameters, each stored on bits bits."""
    if params < 0 or bits < 0:
        raise ValueError("negative value")
    if bits == 0:
        raise ValueError("zero precision")
    return params * bits / 8


def light_round_trip(km):
    """Time (s) for light to cover km of fibre and back, at 200 000 km/s."""
    if km < 0:
        raise ValueError("negative value")
    return 2 * km / 200_000


def cycles(seconds, ghz=3.0):
    """Number of cycles a core at ghz gigahertz runs in seconds seconds."""
    if seconds < 0 or ghz < 0:
        raise ValueError("negative value")
    return seconds * ghz * 1e9


def launch_share(work_s, launch_s):
    """Share of the total time spent launching (rather than working)."""
    if work_s < 0 or launch_s < 0:
        raise ValueError("negative value")
    if work_s + launch_s == 0:
        raise ValueError("zero total duration")
    return launch_s / (work_s + launch_s)
