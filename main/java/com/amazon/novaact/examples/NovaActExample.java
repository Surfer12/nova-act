package com.amazon.novaact.examples;

import com.amazon.novaact.NovaAct;
import com.amazon.novaact.types.ActResult;

import java.util.concurrent.CompletableFuture;

/**
 * Example usage of the NovaAct Java SDK.
 */
public class NovaActExample {
    public static void main(String[] args) {
        // Get API key from environment variable
        String apiKey = System.getenv("NOVA_ACT_API_KEY");
        if (apiKey == null) {
            System.err.println("Please set NOVA_ACT_API_KEY environment variable");
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
                System.out.println("Search completed: " + result.getResult());
            }).join();

            // Example: Select first result
            CompletableFuture<ActResult> selectResult = novaAct.act("select the first result");
            selectResult.thenAccept(result -> {
                System.out.println("Selection completed: " + result.getResult());
            }).join();

            // Example: Add to cart
            CompletableFuture<ActResult> cartResult = novaAct.act(
                "scroll down or up until you see 'add to cart' and then click 'add to cart'");
            cartResult.thenAccept(result -> {
                System.out.println("Added to cart: " + result.getResult());
            }).join();

            // NovaAct will be automatically closed due to try-with-resources
        } catch (Exception e) {
            System.err.println("Error running NovaAct example: " + e.getMessage());
            e.printStackTrace();
        }
    }

    /**
     * Example of using NovaAct in interactive mode.
     */
    public static void interactiveExample() {
        String apiKey = System.getenv("NOVA_ACT_API_KEY");
        if (apiKey == null) {
            System.err.println("Please set NOVA_ACT_API_KEY environment variable");
            return;
        }

        NovaAct novaAct = null;
        try {
            novaAct = new NovaAct.Builder()
                .startingPage("https://www.amazon.com")
                .novaActApiKey(apiKey)
                .headless(false)
                .build();

            novaAct.start();

            // Example of interactive use
            System.out.println("NovaAct started. Enter commands (empty line to exit):");
            
            var scanner = new java.util.Scanner(System.in);
            String line;
            while ((line = scanner.nextLine()) != null && !line.trim().isEmpty()) {
                try {
                    CompletableFuture<ActResult> result = novaAct.act(line);
                    result.thenAccept(r -> {
                        System.out.println("Result: " + r.getResult());
                    }).join();
                } catch (Exception e) {
                    System.err.println("Error executing command: " + e.getMessage());
                }
            }
        } catch (Exception e) {
            System.err.println("Error in interactive mode: " + e.getMessage());
            e.printStackTrace();
        } finally {
            if (novaAct != null) {
                novaAct.close();
            }
        }
    }
}