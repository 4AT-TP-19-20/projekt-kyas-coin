package Tests;

import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import sample.API_operations;

import static org.junit.jupiter.api.Assertions.*;

class API_operationsTest {

    @BeforeAll
    private static void start() {
        System.out.println("Starting tests");
    }

    @Test
    private void test_new_transaction() {
        API_operations o = new API_operations();
        assertThrows(NullPointerException.class, () -> o.new_transaction(null, 0));
        assertThrows(NullPointerException.class, () -> o.new_transaction(null, 1));
        assertThrows(NullPointerException.class, () -> o.new_transaction("", 1));
        assertThrows(NullPointerException.class, () -> o.new_transaction("Test", 1));
        assertThrows(NullPointerException.class, () -> o.new_transaction("Test", -1));
        assertThrows(NullPointerException.class, () -> o.new_transaction("Test", Float.POSITIVE_INFINITY));
        assertThrows(NullPointerException.class, () -> o.new_transaction("Test", Float.NEGATIVE_INFINITY));
    }

    @AfterEach
    private void afterEach() {
        System.out.println("New Test:");
    }

    @AfterAll
    private static void end() {
        System.out.println("All tests finished");
    }

}