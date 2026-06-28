CLOCK = 150_000_000
MAXDIV = 65536
MAXFRACT = 256


def calc_freq_table():

    for clkdiv in range(1, MAXDIV):
        for fract in range(MAXFRACT):
            freq = int(CLOCK / (clkdiv + fract / MAXFRACT))
            yield (CLOCK, clkdiv, fract, freq)


if __name__ == "__main__":
    # for row in calc_freq_table():
    #     print(row)
    for i in range(13):
        print(440*2**(i/12))