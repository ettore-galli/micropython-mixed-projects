#include <unity.h>
#include <notes.h>

void setUp(void)
{
    // set stuff up here
}

void tearDown(void)
{
    // clean stuff up here
}

void test_nextSynthNoteStatus(void)
{
    int STEPS = 10;

    SynthNote synthNote = {0, {0, 1}, {false, false}, 0, 0, false, 0};

    unsigned int status_history[10];
    unsigned int expected_status_history[10] = {0, 1, 2, 1, 0, 1, 2, 1, 0, 1};

    for (int c = 0; c < STEPS; c++)
    {
        nextSynthNoteStatus(&synthNote, 2);
        TEST_ASSERT_EQUAL_UINT(expected_status_history[c], synthNote.status);
    }
}

void test_setSynthNotePinStatus(void)
{
    int STEPS = 10;

    SynthNote synthNote = {0, {0, 1}, {false, false}, 0, 0, false, 0};

    unsigned int status_history[10];
    unsigned int expected_pin_status_history[10][2] = {
        {0, 0},
        {1, 0},
        {1, 1},
        {1, 0},
        {0, 0},
        {1, 0},
        {1, 1},
        {1, 0},
        {0, 0},
        {1, 0},
    };

    for (int c = 0; c < STEPS; c++)
    {
        nextSynthNoteStatus(&synthNote, 2);
        setSynthNotePinStatus(&synthNote);
        TEST_ASSERT_EQUAL_UINT_ARRAY(expected_pin_status_history[c], &synthNote.pin_status, 2);
    }
}

int main()
{

    UNITY_BEGIN();
    RUN_TEST(test_nextSynthNoteStatus);
    RUN_TEST(test_setSynthNotePinStatus);
    UNITY_END();

    return 0;
}
