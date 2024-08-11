from typing import List


def parallel(resistors: List[float]) -> float:
    rsum = sum(
        1 / resistor for resistor in resistors if resistor is not None and resistor > 0
    )
    return 1 / (rsum) if rsum > 0 else 0


def divider(rcommon: float, resistors: List[float]) -> float:
    return rcommon / (rcommon + parallel(resistors))


def out_voltage(vcc: float, rcommon: float, resistors: List[float]) -> float:
    return vcc * divider(rcommon=rcommon, resistors=resistors)


if __name__ == "__main__":
    vcc = 32768
    resistors = [1000, 1500, 2200]
    print("---")
    for combination in [
        [0, 0, 0],
        [0, 0, 1],
        [0, 1, 0],
        [0, 1, 1],
        [1, 0, 0],
        [1, 0, 1],
        [1, 1, 0],
        [1, 1, 1],
    ]:
        rescomb = [res * cmb for res, cmb in zip(resistors, combination)]
        print(rescomb, out_voltage(vcc=vcc, rcommon=1000, resistors=rescomb))

    print("---")

    resistors = [1000, 2200]

    for combination in [
        [0, 0],
        [0, 1],
        [1, 0],
        [1, 1],
    ]:
        rescomb = [res * cmb for res, cmb in zip(resistors, combination)]
        print(rescomb, out_voltage(vcc=vcc, rcommon=1000, resistors=rescomb))
