package Tests;


import org.junit.jupiter.api.*;
import sample.API_operations;

import java.io.IOException;

import static org.junit.jupiter.api.Assertions.assertThrows;


class API_operationsTest {
    private API_operations tester = new API_operations();

    @BeforeAll
    public static void start() {
        System.out.println("Starting tests");
    }

    @Test
    // Parameter test
    public void new_transaction_parameterTest() {
        // Check for null parameter
        System.out.println("null, 1");
        assertThrows(ExceptionInInitializerError.class, () -> tester.new_transaction(null, 1));
        // Check for empty parameter
        System.out.println("\"\", 1");
        assertThrows(NoClassDefFoundError.class, () -> tester.new_transaction("", 1));
        // Check for negative parameter
        System.out.println("\"String\", -1");
        assertThrows(NoClassDefFoundError.class, () -> tester.new_transaction("String", -1));
        // Check for infinity
        System.out.println("\"String\", Infinity");
        assertThrows(NoClassDefFoundError.class, () -> tester.new_transaction("String", Float.POSITIVE_INFINITY));
        // Check for negative infinity
        System.out.println("\"String\", -Infinity");
        assertThrows(NoClassDefFoundError.class, () -> tester.new_transaction("String", Float.NEGATIVE_INFINITY));
    }

    @RepeatedTest(1000)
    // Performance test
    public void register_user_performanceTest() {
        tester.register_user();
    }

    @RepeatedTest(1000)
    // Performance test
    public void get_balance_performanceTest() throws IOException {
        tester.get_balance();
    }

    @RepeatedTest(1000)
    // Performance test
    public void set_masternode_performanceTest() {
        tester.set_masternode();
    }

    @RepeatedTest(1000)
    // Performance test
    public void new_transaction_performanceTest() {
        tester.new_transaction("", 0);
    }

    @RepeatedTest(1000)
    // Performance test
    public void mining_performanceTest() {
        tester.mining();
    }




    @AfterAll
    public static void end() {
        System.out.println("All tests finished");
    }

}