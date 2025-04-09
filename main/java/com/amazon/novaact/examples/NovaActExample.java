package com.amazon.novaact.examples;

import com.amazon.novaact.NovaAct;
import com.amazon.novaact.types.ActResult;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Objects;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.TimeUnit;

/**
 * Example usage of the NovaAct Java SDK.
 */
public final class NovaActExample {
    private static final Logger logger = LoggerFactory.getLogger(NovaActExample.class);
    private static final int TIMEOUT_SECONDS = 30;

    private NovaActExample() {
        // Utility class should not be instantiated
        throw new UnsupportedOperationException("Utility class");
    }

    public static void main(String[] args) {
        // Get API key from environment variable
        final String apiKey = System.getenv("NOVA_ACT_API_KEY");
        if (apiKey == null) {
            logger.error("Please set NOVA_ACT_API_KEY environment variable");
            System.exit(1);
        }

        // Create NovaAct instance with builder pattern
        try (NovaAct novaAct = new NovaAct.Builder()
                .startingPage("https://www.amazon.com")
                .novaActApiKey(apiKey)
                .headless(false)  // Show browser window
                .build()) {

            // Start the client
            novaAct.start();

            // Example: Search for a coffee maker
            CompletableFuture<ActResult> searchResult = novaAct.act("search for a coffee maker");
            searchResult.thenAccept(result -> {
                logger.info("Search completed: {}", result.getResult());
            }).join();

            // Example: Select first result
            CompletableFuture<ActResult> selectResult = novaAct.act("select the first result");
            selectResult.thenAccept(result -> {
                logger.info("Selection completed: {}", result.getResult());
            }).join();

            // Example: Add to cart
            CompletableFuture<ActResult> cartResult = novaAct.act(
                "scroll down or up until you see 'add to cart' and then click 'add to cart'");
            cartResult.thenAccept(result -> {
                logger.info("Added to cart: {}", result.getResult());
            }).join();

            // NovaAct will be automatically closed due to try-with-resources
        } catch (Exception e) {
            logger.error("Error running NovaAct example: {}", e.getMessage(), e);
            System.exit(1);
        }
    }

    /**
     * Example of using NovaAct in interactive mode.
     */
    public static void interactiveExample() {
        final String apiKey = Objects.requireNonNull(System.getenv("NOVA_ACT_API_KEY"),
            "Please set NOVA_ACT_API_KEY environment variable");

        NovaAct novaAct = null;
        try {
            novaAct = new NovaAct.Builder()
                .startingPage("https://www.amazon.com")
                .novaActApiKey(apiKey)
                .headless(false)
                .build();

            novaAct.start();

            // Example of interactive use
            logger.info("NovaAct started. Enter commands (empty line to exit):");
            
            var scanner = new java.util.Scanner(System.in);
            String line;
            while ((line = scanner.nextLine()) != null && !line.trim().isEmpty()) {
                try {
                    CompletableFuture<ActResult> result = novaAct.act(line);
                    result.thenAccept(r -> {
                        logger.info("Result: {}", r.getResult());
                    }).get(TIMEOUT_SECONDS, TimeUnit.SECONDS);
                } catch (Exception e) {
                    logger.error("Error executing command: {}", e.getMessage(), e);
                }
            }
        } catch (Exception e) {
            logger.error("Error in interactive mode: {}", e.getMessage(), e);
        } finally {
            if (novaAct != null) {
                novaAct.close();
            }
        }
    }
}