package com.amazon.novaact.impl;

import com.amazon.novaact.types.ActMetadata;
import com.amazon.novaact.types.ActResult;
import com.amazon.novaact.types.BackendInfo;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.microsoft.playwright.Page;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.nio.file.Path;
import java.time.Instant;
import java.util.Map;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicBoolean;

/**
 * Handles communication with the Chrome extension for browser actuation.
 */
public class ExtensionDispatcher {
    private static final Logger logger = LoggerFactory.getLogger(ExtensionDispatcher.class);
    private static final ObjectMapper objectMapper = new ObjectMapper();

    private final BackendInfo backendInfo;
    private final String novaActApiKey;
    private final boolean tty;
    private final String sessionId;
    private final PlaywrightManager playwrightManager;
    private final Path logsDirectory;

    private final Map<String, CompletableFuture<ActResult>> pendingPrompts = new ConcurrentHashMap<>();
    private final AtomicBoolean promptCancelled = new AtomicBoolean(false);

    private ExtensionDispatcher(Builder builder) {
        this.backendInfo = builder.backendInfo;
        this.novaActApiKey = builder.novaActApiKey;
        this.tty = builder.tty;
        this.sessionId = builder.sessionId;
        this.playwrightManager = builder.playwrightManager;
        this.logsDirectory = builder.logsDirectory;

        setupMessageHandlers();
    }

    private void setupMessageHandlers() {
        Page page = playwrightManager.getPage();
        
        // Listen for extension messages
        page.onWebSocket(webSocket -> {
            webSocket.onFrameReceived(frame -> {
                try {
                    JsonNode message = objectMapper.readTree(frame.text());
                    handleExtensionMessage(message);
                } catch (Exception e) {
                    logger.error("Error processing extension message", e);
                }
            });
        });
    }

    private void handleExtensionMessage(JsonNode message) {
        String type = message.path("type").asText();
        String promptId = message.path("promptId").asText();
        
        CompletableFuture<ActResult> future = pendingPrompts.get(promptId);
        if (future == null) {
            logger.warn("No pending prompt found for ID: {}", promptId);
            return;
        }

        switch (type) {
            case "PROMPT_COMPLETE" -> {
                ActResult result = parseActResult(message);
                future.complete(result);
                pendingPrompts.remove(promptId);
            }
            case "PROMPT_ERROR" -> {
                String error = message.path("error").asText();
                future.completeExceptionally(new RuntimeException(error));
                pendingPrompts.remove(promptId);
            }
            case "PROMPT_PROGRESS" -> {
                // Handle progress updates if needed
                logger.debug("Progress update for prompt {}: {}", promptId, message);
            }
            default -> logger.warn("Unknown message type: {}", type);
        }
    }

    public CompletableFuture<ActResult> dispatchPrompt(String prompt, int maxSteps, ActMetadata metadata) {
        if (promptCancelled.get()) {
            return CompletableFuture.failedFuture(
                new IllegalStateException("Cannot dispatch new prompt while previous is being cancelled"));
        }

        CompletableFuture<ActResult> future = new CompletableFuture<>();
        pendingPrompts.put(metadata.getActId(), future);

        try {
            Page page = playwrightManager.getPage();
            
            Map<String, Object> message = Map.of(
                "type", "EXECUTE_PROMPT",
                "promptId", metadata.getActId(),
                "prompt", prompt,
                "maxSteps", maxSteps,
                "metadata", Map.of(
                    "sessionId", sessionId,
                    "actId", metadata.getActId(),
                    "startTime", Instant.now().toEpochMilli()
                ),
                "apiKey", novaActApiKey,
                "endpoint", backendInfo.apiUri()
            );

            page.evaluate("window.postMessage(" + objectMapper.writeValueAsString(message) + ", '*')");
            
            // Set up timeout if needed
            // future.orTimeout(timeout, TimeUnit.MILLISECONDS);
            
            return future;
        } catch (Exception e) {
            pendingPrompts.remove(metadata.getActId());
            return CompletableFuture.failedFuture(e);
        }
    }

    public void cancelPrompt() {
        if (promptCancelled.compareAndSet(false, true)) {
            try {
                Page page = playwrightManager.getPage();
                page.evaluate("window.postMessage({type: 'CANCEL_PROMPT'}, '*')");
                
                // Complete all pending prompts with cancellation
                pendingPrompts.forEach((id, future) -> 
                    future.completeExceptionally(new RuntimeException("Prompt cancelled")));
                pendingPrompts.clear();
            } catch (Exception e) {
                logger.error("Error cancelling prompt", e);
            } finally {
                promptCancelled.set(false);
            }
        }
    }

    private ActResult parseActResult(JsonNode message) {
        try {
            JsonNode data = message.path("data");
            return new ActResult.Builder()
                .response(data.path("response").asText())
                .parsedResponse(data.path("parsedResponse"))
                .validJson(data.path("validJson").asBoolean())
                .matchesSchema(data.path("matchesSchema").asBoolean())
                .metadata(objectMapper.treeToValue(data.path("metadata"), ActMetadata.class))
                .success(data.path("success").asBoolean())
                .result(data.path("result").asText())
                .processingLevel(data.path("processingLevel").asText())
                .iterationCount(data.path("iterationCount").asInt())
                .build();
        } catch (Exception e) {
            logger.error("Error parsing act result", e);
            throw new RuntimeException("Failed to parse act result", e);
        }
    }

    public static class Builder {
        private BackendInfo backendInfo;
        private String novaActApiKey;
        private boolean tty;
        private String sessionId;
        private PlaywrightManager playwrightManager;
        private Path logsDirectory;

        public Builder backendInfo(BackendInfo backendInfo) {
            this.backendInfo = backendInfo;
            return this;
        }

        public Builder novaActApiKey(String novaActApiKey) {
            this.novaActApiKey = novaActApiKey;
            return this;
        }

        public Builder tty(boolean tty) {
            this.tty = tty;
            return this;
        }

        public Builder sessionId(String sessionId) {
            this.sessionId = sessionId;
            return this;
        }

        public Builder playwrightManager(PlaywrightManager playwrightManager) {
            this.playwrightManager = playwrightManager;
            return this;
        }

        public Builder logsDirectory(Path logsDirectory) {
            this.logsDirectory = logsDirectory;
            return this;
        }

        public ExtensionDispatcher build() {
            return new ExtensionDispatcher(this);
        }
    }
}