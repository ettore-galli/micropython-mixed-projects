#include <unity.h>

void setUp(void)
{
    // set stuff up here
}

void tearDown(void)
{
    // clean stuff up here
}

void simple_test(void)
{
    TEST_ASSERT_EQUAL(33, 33);
    TEST_ASSERT_EQUAL(1, 1);
}

int main()
{

    UNITY_BEGIN();
    RUN_TEST(simple_test);
    UNITY_END();

    return 0;
}
