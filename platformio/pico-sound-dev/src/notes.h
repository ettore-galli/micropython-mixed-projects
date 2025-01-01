
/**
 * tools/notes.py
 */

typedef unsigned int (*NoteNumberChangeFunction)(const unsigned int note_number);

const unsigned int TOTAL_NUMBER_OF_NOTES = 25;
const unsigned int ACTUAL_NUMBER_OF_NOTES = 8;

const float C = 523.2511306011972;

struct note_reference
{
    unsigned int id;
    float freq;
};

note_reference notes_reference[TOTAL_NUMBER_OF_NOTES] = {
    {0, 523.2511306011972},   // C
    {1, 554.3652619537442},   // C#
    {2, 587.3295358348151},   // D
    {3, 622.2539674441617},   // D#
    {4, 659.2551138257398},   // E
    {5, 698.4564628660078},   // F
    {6, 739.9888454232688},   // F#
    {7, 783.9908719634985},   // G
    {8, 830.6093951598901},   // G#
    {9, 879.9999999999999},   // A
    {10, 932.3275230361797},  // A#
    {11, 987.7666025122481},  // B
    {12, 1046.5022612023945}, // C
    {13, 1108.7305239074883}, // C#
    {14, 1174.6590716696303}, // D
    {15, 1244.5079348883235}, // D#
    {16, 1318.5102276514797}, // E
    {17, 1396.9129257320155}, // F
    {18, 1479.9776908465376}, // F#
    {19, 1567.981743926997},  // G
    {20, 1661.2187903197805}, // G#
    {21, 1759.9999999999998}, // A
    {22, 1864.6550460723595}, // A#
    {23, 1975.5332050244965}, // B
    {24, 2093.004522404789},  // C
};

struct note
{
    unsigned long lastTick;
    unsigned int pin;
    unsigned int note_number;
    unsigned int delayTimeus;
    bool status;
};

note notes[ACTUAL_NUMBER_OF_NOTES] = {
    {0, 0, 7, 0, false},
    {0, 1, 9, 0, false},
    {0, 2, 12, 0, false},
    {0, 3, 14, 0, false},
    {0, 4, 17, 0, false},
    {0, 5, 19, 0, false},
    {0, 6, 21, 0, false},
    {0, 7, 24, 0, false},
};

struct control_pin
{
    unsigned int note_pin;
    unsigned int control_pin;
};

control_pin control_pins[ACTUAL_NUMBER_OF_NOTES] = {
    {0, 8},
    {1, 9},
    {2, 10},
    {3, 11},
    {4, 12},
    {5, 13},
    {6, 14},
    {7, 15},
};

unsigned int newNoteNumberUp(const unsigned int note_number)
{
    return (note_number + 1) % TOTAL_NUMBER_OF_NOTES;
}

unsigned int newNoteNumberDown(const unsigned int note_number)
{
    return note_number > 0 ? note_number - 1 : TOTAL_NUMBER_OF_NOTES - 1;
}