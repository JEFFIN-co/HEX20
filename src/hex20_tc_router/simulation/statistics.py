"""HEX20 M10 validation statistics and report helpers."""
from __future__ import annotations
from collections import Counter
from dataclasses import asdict, dataclass
from statistics import mean, median


@dataclass
class ValidationStats:
    total: int
    accepted: int
    rejected: int
    acceptance_rate_pct: float
    rejection_rate_pct: float
    latency_mean_ms: float
    latency_median_ms: float
    latency_p95_ms: float
    latency_p99_ms: float
    latency_max_ms: float
    latency_min_ms: float
    throughput_cmd_s: float

    def to_dict(self):
        return asdict(self)


def percentile(values: list[float], p: float) -> float:
    if not values:
        return 0.0
    values = sorted(values)
    rank = (len(values) - 1) * p
    low = int(rank)
    high = min(low + 1, len(values) - 1)
    frac = rank - low
    return values[low] + (values[high] - values[low]) * frac


def summarize(results, elapsed_s: float) -> ValidationStats:
    total = len(results)
    accepted = sum(1 for r in results if r.accepted)
    rejected = total - accepted
    latencies = [r.latency_ms for r in results]
    return ValidationStats(
        total=total,
        accepted=accepted,
        rejected=rejected,
        acceptance_rate_pct=(accepted / total * 100) if total else 0.0,
        rejection_rate_pct=(rejected / total * 100) if total else 0.0,
        latency_mean_ms=mean(latencies) if latencies else 0.0,
        latency_median_ms=median(latencies) if latencies else 0.0,
        latency_p95_ms=percentile(latencies, .95),
        latency_p99_ms=percentile(latencies, .99),
        latency_max_ms=max(latencies) if latencies else 0.0,
        latency_min_ms=min(latencies) if latencies else 0.0,
        throughput_cmd_s=(total / elapsed_s) if elapsed_s > 0 else 0.0,
    )


def count_field(results, field: str):
    return dict(Counter(getattr(r, field) for r in results))
