from .tones import Tone


class Chord:
    def __init__(self, *, tones):
        self.tones = tones

    def __repr__(self):
        l = tuple([tone.full_name for tone in self.tones])
        return f"<Chord tones={l!r}>"

    # @property
    # def harmony(self):
    #     pass


class NamedChord:
    def __init__(self, *, name, system):
        self.name
        self.system


class Fretboard:
    def __init__(self, *, tones):
        self.tones = tones

    def __repr__(self):
        l = tuple([tone.full_name for tone in self.tones])
        return f"<Fretboard tones={l!r}>"

    def fingering(self, *positions):
        if not len(positions) == len(self.tones):
            raise ValueError(
                "The number of positions must match the number of tones (strings)."
            )

        tones = []
        for (i, tone) in enumerate(self.tones):
            tones.append(tone.add(positions[i]))

        return Chord(tones=tones)


def fretboard_from_joni(annotation, default_octave=2):
    """Converts Joni notation into a Fredboard object.

    e.g. 'E 55545'
    """
    split_annotation = annotation.split()

    if not len(split_annotation) == 2:
        raise ValueError("Must be in 'E 55545' format.")

    base_tone = split_annotation[0]
    intervals = split_annotation[1]
    base_octave = default_octave

    base_tone = Tone.from_string(f"{base_tone}{base_octave}")

    strings = [base_tone]
    last_tone = base_tone

    for interval in intervals:
        interval = int(interval)
        next_tone = last_tone.add(interval)
        strings.append(next_tone)
        last_tone = next_tone

    return Fretboard(tones=strings)


fretboards = {"guitar": fretboard_from_joni("E 55545", default_octave=2)}
