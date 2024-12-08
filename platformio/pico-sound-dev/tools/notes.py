C = 523.2511306011972

names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"] * 3

for note in [
    f"{{0, {n}, {C*2**(n/12)}, 0, false}}, // {name} "
    for n, name in zip(range(36), names)
]:
    print(note)
