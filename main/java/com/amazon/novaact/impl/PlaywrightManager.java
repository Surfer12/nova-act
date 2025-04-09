package com.amazon.novaact.impl;

import com.microsoft.playwright.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.nio.file.Path;
import java.util.List;
import java.util.concurrent.atomic.AtomicBoolean;

/**
 * Manages Playwright browser instances and provides browser automation capabilities.
 */
public class PlaywrightManager implements AutoCloseable {
    private static final Logger logger = LoggerFactory.getLogger(PlaywrightManager.class);

    private final String startingPage;
    private final Path userDataDir;
    private final Path extensionPath;
    private final int screenWidth;
    private final int screenHeight;
    private final boolean headless;
    private final String chromeChannel;
    private final String userAgent;
    private final Path logsDirectory;
    private final boolean recordVideo;

    private Playwright playwright;
    private Browser browser;
    private BrowserContext context;
    private final AtomicBoolean started = new AtomicBoolean(false);
    private String sessionId;

    private PlaywrightManager(Builder builder) {
        this.startingPage = builder.startingPage;
        this.userDataDir = builder.userDataDir;
        this.extensionPath = builder.extensionPath;
        this.screenWidth = builder.screenWidth;
        this.screenHeight = builder.screenHeight;
        this.headless = builder.headless;
        this.chromeChannel = builder.chromeChannel;
        this.userAgent = builder.userAgent;
        this.logsDirectory = builder.logsDirectory;
        this.recordVideo = builder.recordVideo;
    }

    public void start() {
        if (started.get()) {
            logger.warn("Playwright is already started");
            return;
        }

        try {
            playwright = Playwright.create();
            
            BrowserType browserType = switch (chromeChannel.toLowerCase()) {
                case "chrome" -> playwright.chromium();
                case "firefox" -> playwright.firefox();
                case "webkit" -> playwright.webkit();
                default -> throw new IllegalArgumentException("Unsupported browser type: " + chromeChannel);
            };

            var launchOptions = new BrowserType.LaunchOptions()
                .setHeadless(headless)
                .setArgs(List.of(
                    "--disable-extensions-except=" + extensionPath,
                    "--load-extension=" + extensionPath
                ));

            if (userDataDir != null) {
                launchOptions.setUserDataDir(userDataDir);
            }

            browser = browserType.launch(launchOptions);

            var contextOptions = new Browser.NewContextOptions()
                .setViewportSize(screenWidth, screenHeight);

            if (userAgent != null) {
                contextOptions.setUserAgent(userAgent);
            }

            if (recordVideo) {
                contextOptions.setRecordVideoDir(logsDirectory);
            }

            context = browser.newContext(contextOptions);
            var page = context.newPage();
            page.navigate(startingPage);

            started.set(true);
            logger.info("Started Playwright with {} on {}", chromeChannel, startingPage);
        } catch (Exception e) {
            close();
            throw new RuntimeException("Failed to start Playwright", e);
        }
    }

    @Override
    public void close() {
        try {
            if (context != null) {
                context.close();
                context = null;
            }
            if (browser != null) {
                browser.close();
                browser = null;
            }
            if (playwright != null) {
                playwright.close();
                playwright = null;
            }
            started.set(false);
            sessionId = null;
        } catch (Exception e) {
            logger.error("Error closing Playwright resources", e);
            throw new RuntimeException("Failed to close Playwright", e);
        }
    }

    public boolean isStarted() {
        return started.get();
    }

    public Page getPage(int index) {
        if (!isStarted()) {
            throw new IllegalStateException("Playwright must be started before accessing pages");
        }

        var pages = context.pages();
        if (pages.isEmpty()) {
            throw new IllegalStateException("No pages available");
        }

        if (index < 0) {
            return pages.get(pages.size() - 1);
        }
        
        if (index >= pages.size()) {
            throw new IndexOutOfBoundsException("Page index out of bounds: " + index);
        }

        return pages.get(index);
    }

    public List<Page> getPages() {
        if (!isStarted()) {
            throw new IllegalStateException("Playwright must be started before accessing pages");
        }
        return context.pages();
    }

    public void setSessionId(String sessionId) {
        this.sessionId = sessionId;
    }

    public String getSessionId() {
        return sessionId;
    }

    public static class Builder {
        private String startingPage;
        private Path userDataDir;
        private Path extensionPath;
        private int screenWidth;
        private int screenHeight;
        private boolean headless;
        private String chromeChannel = "chrome";
        private String userAgent;
        private Path logsDirectory;
        private boolean recordVideo;

        public Builder startingPage(String startingPage) {
            this.startingPage = startingPage;
            return this;
        }

        public Builder userDataDir(Path userDataDir) {
            this.userDataDir = userDataDir;
            return this;
        }

        public Builder extensionPath(Path extensionPath) {
            this.extensionPath = extensionPath;
            return this;
        }

        public Builder screenWidth(int screenWidth) {
            this.screenWidth = screenWidth;
            return this;
        }

        public Builder screenHeight(int screenHeight) {
            this.screenHeight = screenHeight;
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

        public PlaywrightManager build() {
            return new PlaywrightManager(this);
        }
    }
}