package com.amazon.novaact.types;

/**
 * Information about the Nova Act backend service.
 */
public record BackendInfo(String apiUri, String keygenUri) {
    public static final BackendInfo PROD = new BackendInfo(
        "https://nova.amazon.com/agent",
        "https://nova.amazon.com/act"
    );
}