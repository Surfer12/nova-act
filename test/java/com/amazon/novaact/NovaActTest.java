package com.amazon.novaact;

import com.amazon.novaact.types.ActResult;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.condition.EnabledIfEnvironmentVariable;

import java.util.concurrent.CompletableFuture;
import java.util.concurrent.TimeUnit;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Tests for NovaAct Java SDK.
 */
@EnabledIfEnvironmentVariable(named = "NOVA_ACT_API_KEY", matches = ".+")
class NovaActTest {
    private NovaAct novaAct;
    private static final String TEST_PAGE = "https://www.amazon.com";
    private static final int TIMEOUT_SECONDS = 30;

    @BeforeEach
    void setUp() {
        String apiKey = System.getenv("NOVA_ACT_API_KEY");
        assertNotNull(apiKey, "NOVA_ACT_API_KEY environment variable must be set");

        novaAct = new NovaAct.Builder()
            .startingPage(TEST_PAGE)
            .novaActApiKey(apiKey)
            .headless(true)  // Run headless in tests
            .build();
    }

    @AfterEach
    void tearDown() {
        if (novaAct != null) {
            novaAct.close();
        }
    }

    @Test
    void testStartAndStop() {
        assertFalse(novaAct.isStarted());
        novaAct.start();
        assertTrue(novaAct.isStarted());
        novaAct.close();
        assertFalse(novaAct.isStarted());
    }

    @Test
    void testBasicSearch() throws Exception {
        novaAct.start();
        assertTrue(novaAct.isStarted());

        CompletableFuture<ActResult> future = novaAct.act("search for java programming books");
        ActResult result = future.get(TIMEOUT_SECONDS, TimeUnit.SECONDS);

        assertNotNull(result);
        assertTrue(result.isSuccess());
        assertNotNull(result.getResult());
    }

    @Test
    void testMultipleActions() throws Exception {
        novaAct.start();
        assertTrue(novaAct.isStarted());

        // First action: search
        CompletableFuture<ActResult> searchFuture = novaAct.act("search for coffee maker");
        ActResult searchResult = searchFuture.get(TIMEOUT_SECONDS, TimeUnit.SECONDS);
        assertTrue(searchResult.isSuccess());

        // Second action: select result
        CompletableFuture<ActResult> selectFuture = novaAct.act("select the first result");
        ActResult selectResult = selectFuture.get(TIMEOUT_SECONDS, TimeUnit.SECONDS);
        assertTrue(selectResult.isSuccess());
    }

    @Test
    void testInvalidPrompt() {
        novaAct.start();
        assertTrue(novaAct.isStarted());

        assertThrows(IllegalArgumentException.class, () -> {
            novaAct.act("");  // Empty prompt should throw exception
        });

        assertThrows(IllegalArgumentException.class, () -> {
            novaAct.act(null);  // Null prompt should throw exception
        });
    }

    @Test
    void testPageAccess() {
        novaAct.start();
        assertTrue(novaAct.isStarted());

        assertNotNull(novaAct.getPage());
        assertNotNull(novaAct.getPages());
        assertFalse(novaAct.getPages().isEmpty());
    }

    @Test
    void testClientNotStarted() {
        // Don't start the client
        assertThrows(IllegalStateException.class, () -> {
            novaAct.act("this should fail");
        });

        assertThrows(IllegalStateException.class, () -> {
            novaAct.getPage();
        });
    }
}