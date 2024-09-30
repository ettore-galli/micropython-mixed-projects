from math import sin

from ghost_detector.ghost_detector_logic import GhostDetector


def normalize(values: list[float], top: int) -> list[int]:
    bottom = min(*values)
    peaks = max(*values) - min(*values)
    return [int((point - bottom) * top / peaks) for point in values]


def plot(values: list[float]) -> None:
    for point in normalize(values, 64):
        print(("-" * (point - 1) if point > 1 else "") + "*")  # noqa: T201


def test_dft() -> None:
    domain = range(32)
    samples = [
        (
            sin(3 * 6.28 * index / len(domain))
            + sin(3 * 6.28 * 2 * index / len(domain))
            + sin(3 * 6.28 * 3 * index / len(domain))
        )
        for index in domain
    ]

    dft = GhostDetector.perform_r_dft(samples)

    assert len(dft) == len(domain)

    assert dft == [
        0.04107717738326346,
        0.041069782325346256,
        0.04104747844926989,
        0.041009903442527154,
        0.04095643214248368,
        0.04088614228788678,
        0.04079776160146007,
        0.040689590199818375,
        0.04055938882751079,
        0.04040421790439347,
        0.04022020334111717,
        0.04000218967330871,
        0.039743213726489625,
        0.03943368128446656,
        0.03906003015414369,
        0.03860245747810537,
        0.03803083064630794,
        0.037296782448012517,
        0.03631693283224749,
        0.03493246763291567,
        0.03279230194698517,
        0.028902417872246445,
        0.018587222921155215,
        1.1182506119731752,
        0.05058613666714167,
        0.031097056937930117,
        1.108344397146092,
        0.059696012914351414,
        0.040414698220946864,
        1.0977896801344926,
        0.07336218139706689,
        0.06365331203558382,
    ]
