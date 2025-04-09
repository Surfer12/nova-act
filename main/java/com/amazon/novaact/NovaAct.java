package com.amazon.novaact;

import com.amazon.novaact.bridge.NovaActBridge;
import com.amazon.novaact.impl.ExtensionDispatcher;
import com.amazon.novaact.impl.PlaywrightManager;
import com.amazon.novaact.types.ActMetadata;
import com.amazon.novaact.types.ActResult;
import com.amazon.novaact.types.BackendInfo;
import com.fasterxml.jackson.databind.JsonNode;
import com.microsoft.playwright.Page;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.Closeable;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.Instant;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.CompletableFuture;

/**
 * Client for interacting with the Nova Act Agent.
 */
public class NovaAct implements Closeable {
    private static final Logger logger = LoggerFactory.getLogger(NovaAct.class);
    private static final int DEFAULT_ACT_MAX_STEPS = 30;
    private static final int DEFAULT_SCREEN_WIDTH = 1600;
    private static final int DEFAULT_SCREEN_HEIGHT = 900;

    private final String startingPage;
    private final Path userDataDir;
    private final boolean deleteUserDataDirOnClose;
    private final BackendInfo backendInfo;
    private final String novaActApiKey;
    private final String endpointName;
    private final boolean tty;
    private final Path logsDirectory;
    private final PlaywrightManager playwrightManager;
    private final NovaActBridge bridge;
    private ExtensionDispatcher dispatcher;
    private String sessionId;

    private NovaAct(Builder builder) {
        this.startingPage = builder.startingPage;
        this.userDataDir = setupUserDataDir(builder.userDataDir, builder.cloneUserDataDir);
        this.deleteUserDataDirOnClose = builder.userDataDir == null || builder.cloneUserDataDir;
        this.backendInfo = builder.backendInfo;
        this.novaActApiKey = getApiKey(builder.novaActApiKey);
        this.endpointName = builder.endpointName;
        this.tty = builder.tty;
        this.logsDirectory = setupLogsDirectory(builder.logsDirectory);
        
        this.playwrightManager = new PlaywrightManager.Builder()
            .startingPage(startingPage)
            .userDataDir(userDataDir)
            .extensionPath(builder.extensionPath)
            .screenWidth(builder.screenWidth)
            .screenHeight(builder.screenHeight)
            .headless(builder.headless)
            .chromeChannel(builder.chromeChannel)
            .userAgent(builder.userAgent)
            .logsDirectory(logsDirectory)
            .recordVideo(builder.recordVideo)
            .build();

        if (builder.enableBridge) {
            this.bridge = new NovaActBridge(builder.bridgeHost, builder.bridgePort);
        } else {
            this.bridge = null;
        }
    }

    public void start() {
        if (isStarted()) {
            logger.warn("Client is already started; to start over, call close() first.");
            return;
        }

        try {
            sessionId = UUID.randomUUID().toString();
            playwrightManager.start();
            
            if (dispatcher == null) {
                dispatcher = new ExtensionDispatcher.Builder()
                    .backendInfo(backendInfo)
                    .novaActApiKey(novaActApiKey)
                    .tty(tty)
                    .sessionId(sessionId)
                    .playwrightManager(playwrightManager)
                    .logsDirectory(logsDirectory)
                    .build();
            }

            if (bridge != null) {
                bridge.start();
            }

            logger.info("Started session {} on {}", sessionId, startingPage);
        } catch (Exception e) {
            close();
            throw new RuntimeException("Failed to start NovaAct client", e);
        }
    }

    @Override
    public void close() {
        try {
            if (dispatcher != null) {
                dispatcher.cancelPrompt();
            }
            
            if (playwrightManager != null) {
                playwrightManager.close();
            }

            if (bridge != null) {
                bridge.stop();
            }

            if (deleteUserDataDirOnClose && userDataDir != null) {
                Files.deleteIfExists(userDataDir);
            }

            dispatcher = null;
            sessionId = null;
            logger.info("Session ended");
        } catch (Exception e) {
            throw new RuntimeException("Failed to stop NovaAct client", e);
        }
    }

    public CompletableFuture<ActResult> act(String prompt) {
        return act(prompt, DEFAULT_ACT_MAX_STEPS, null);
    }

    public CompletableFuture<ActResult> act(String prompt, int maxSteps, JsonNode schema) {
        if (!isStarted()) {
            throw new IllegalStateException("Client must be started before calling act()");
        }

        validatePrompt(prompt);
        validateMaxSteps(maxSteps);
        if (schema != null) {
            validateSchema(schema);
            prompt = addSchemaToPrompt(prompt, schema);
        }

        ActMetadata metadata = new ActMetadata.Builder()
            .sessionId(sessionId)
            .actId(UUID.randomUUID().toString())
            .startTime(Instant.now().toEpochMilli())
            .prompt(prompt)
            .build();

        return dispatcher.dispatchPrompt(prompt, maxSteps, metadata)
            .thenApply(response -> {
                if (bridge != null && response.isSuccess()) {
                    bridge.sendThoughtUpdate(Map.of(
                        "prompt", prompt,
                        "result", response.getResult(),
                        "metadata", response.getMetadata(),
                        "processingLevel", response.getProcessingLevel(),
                        "iterationCount", response.getIterationCount(),
                        "timestamp", Instant.now().toEpochMilli()
                    ));
                }
                return response;
            });
    }

    public boolean isStarted() {
        return playwrightManager != null && playwrightManager.isStarted() && dispatcher != null;
    }

    public Page getPage() {
        return getPage(-1);
    }

    public Page getPage(int index) {
        if (!isStarted()) {
            throw new IllegalStateException("Client must be started before accessing pages");
        }
        return playwrightManager.getPage(index);
    }

    public List<Page> getPages() {
        if (!isStarted()) {
            throw new IllegalStateException("Client must be started before accessing pages");
        }
        return playwrightManager.getPages();
    }

    public static class Builder {
        private String startingPage;
        private Path userDataDir;
        private boolean cloneUserDataDir = true;
        private Path extensionPath;
        private int screenWidth = DEFAULT_SCREEN_WIDTH;
        private int screenHeight = DEFAULT_SCREEN_HEIGHT;
        private boolean headless = false;
        private String chromeChannel = "chrome";
        private String novaActApiKey;
        private String endpointName = "default";
        private boolean tty = true;
        private String userAgent;
        private Path logsDirectory;
        private boolean recordVideo = false;
        private boolean enableBridge = true;
        private String bridgeHost = "localhost";
        private int bridgePort = 8081;
        private BackendInfo backendInfo = BackendInfo.PROD;

        public Builder startingPage(String startingPage) {
            this.startingPage = startingPage;
            return this;
        }

        public Builder userDataDir(Path userDataDir) {
            this.userDataDir = userDataDir;
            return this;
        }

        public Builder cloneUserDataDir(boolean cloneUserDataDir) {
            this.cloneUserDataDir = cloneUserDataDir;
            return this;
        }

        public Builder extensionPath(Path extensionPath) {
            this.extensionPath = extensionPath;
            return this;
        }

        public Builder screenDimensions(int width, int height) {
            this.screenWidth = width;
            this.screenHeight = height;
            return this;
        }

        public Builder headless(boolean headless) {
            this.headless = headless;
            return this;
        }

        public Builder chromeChannel(String chromeChannel) {
            this.chromeChannel = chromeChannel;
            return this;
        }

        public Builder novaActApiKey(String apiKey) {
            this.novaActApiKey = apiKey;
            return this;
        }

        public Builder endpointName(String endpointName) {
            this.endpointName = endpointName;
            return this;
        }

        public Builder tty(boolean tty) {
            this.tty = tty;
            return this;
        }

        public Builder userAgent(String userAgent) {
            this.userAgent = userAgent;
            return this;
        }

        public Builder logsDirectory(Path logsDirectory) {
            this.logsDirectory = logsDirectory;
            return this;
        }

        public Builder recordVideo(boolean recordVideo) {
            this.recordVideo = recordVideo;
            return this;
        }

        public Builder bridge(boolean enable, String host, int port) {
            this.enableBridge = enable;
            this.bridgeHost = host;
            this.bridgePort = port;
            return this;
        }

        public Builder backendInfo(BackendInfo backendInfo) {
            this.backendInfo = backendInfo;
            return this;
        }

        public NovaAct build() {
            return new NovaAct(this);
        }
    }

    private static Path setupUserDataDir(Path userDataDir, boolean clone) {
        // Implementation for setting up user data directory
        return null; // TODO
    }

    private static Path setupLogsDirectory(Path logsDirectory) {
        // Implementation for setting up logs directory
        return null; // TODO
    }

    private static String getApiKey(String apiKey) {
        // Implementation for getting API key from parameter or environment
        return null; // TODO
    }

    private static void validatePrompt(String prompt) {
        // Implementation for validating prompt
    }

    private static void validateMaxSteps(int maxSteps) {
        // Implementation for validating max steps
    }

    private static void validateSchema(JsonNode schema) {
        // Implementation for validating JSON schema
    }

    private static String addSchemaToPrompt(String prompt, JsonNode schema) {
        // Implementation for adding schema to prompt
        return null; // TODO
    }
}