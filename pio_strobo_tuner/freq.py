CLOCK = 150_000_000
MAXDIV = 65536
MAXFRACT = 256

import math


def calc_freq_table():

    for clkdiv in range(1, MAXDIV):
        for fract in range(MAXFRACT):
            freq = int(CLOCK / (clkdiv + fract / MAXFRACT))
            yield (CLOCK, clkdiv, fract, freq)


F_SYS = 125_000_000  # Hz, clock di sistema (es. RP2040)
N_CICLI = 10  # cicli per periodo completo (5 blocchi da 1000)


def sm_freq_from_target(f_target):
    # 1) frequenza ideale del clock SM
    f_sm_des = f_target * N_CICLI

    # 2) valore da passare alla SM (deve essere intero)
    freq_param = round(f_sm_des)

    # 3) MicroPython calcolerà questo divisore:
    d = round(F_SYS / freq_param)

    # 4) frequenza reale della SM
    f_sm_real = F_SYS / d

    # 5) frequenza reale di uscita
    f_out_real = f_sm_real / N_CICLI

    # 6) errori
    err_hz = f_out_real - f_target
    err_cent = 1200 * math.log2(f_out_real / f_target)

    return {
        "f_target": f_target,
        "N_CICLI": N_CICLI,
        "freq_for_sm": freq_param,  # <-- questo è ciò che devi impostare nella SM
        "divider": d,
        "f_sm_real": f_sm_real,
        "f_out_real": f_out_real,
        "err_hz": err_hz,
        "err_cent": err_cent,
    }


def best_freqs():
    freqs = [
        440.0,
        466.1637615180899,
        493.8833012561241,
        523.2511306011972,
        554.3652619537442,
        587.3295358348151,
        622.2539674441618,
        659.2551138257398,
        698.4564628660078,
        739.9888454232688,
        783.9908719634985,
        830.6093951598903,
    ]

    for ftarget in freqs:
        info = sm_freq_from_target(ftarget)
        print(
            f"{info['f_target']:9.3f} Hz -> "
            f"freq_for_sm={info['freq_for_sm']:9.3f}, "
            f"cents={info['err_cent']:6.4f}"
        )


if __name__ == "__main__":
    # for row in calc_freq_table():
    #     print(row)
    best_freqs()
