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

void test_new_note_number_up(void)
{
    TEST_ASSERT_EQUAL(newNoteNumberUp(1), 2);
    TEST_ASSERT_EQUAL(newNoteNumberUp(TOTAL_NUMBER_OF_NOTES - 1), 0);
}

void test_new_note_number_down(void)
{
    TEST_ASSERT_EQUAL(newNoteNumberDown(2), 1);
    TEST_ASSERT_EQUAL(newNoteNumberDown(0), TOTAL_NUMBER_OF_NOTES - 1);
}

int main()
{

    UNITY_BEGIN();
    RUN_TEST(test_new_note_number_up);
    RUN_TEST(test_new_note_number_down);
    UNITY_END();

    return 0;
}
