package com.amazon.novaact.bridge;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;
import org.java_websocket.WebSocket;
import org.java_websocket.handshake.ClientHandshake;
import org.java_websocket.server.WebSocketServer;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.net.InetSocketAddress;
import java.util.Map;
import java.util.Set;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CopyOnWriteArraySet;

/**
 * WebSocket bridge for Nova Act to communicate with frontend.
 */
public class NovaActBridge extends WebSocketServer {
    private static final Logger logger = LoggerFactory.getLogger(NovaActBridge.class);
    private static final ObjectMapper objectMapper = new ObjectMapper();

    private final Set<WebSocket> clients = new CopyOnWriteArraySet<>();
    private final Map<String, Object> fractalConfig = new ConcurrentHashMap<>();

    public NovaActBridge(String host, int port) {
        super(new InetSocketAddress(host, port));
    }

    @Override
    public void onOpen(WebSocket conn, ClientHandshake handshake) {
        if (conn == null) {
            logger.error("Received null connection in onOpen");
            return;
        }
        clients.add(conn);
        logger.info("New connection from: {}", conn.getRemoteSocketAddress());
    }

    @Override
    public void onClose(WebSocket conn, int code, String reason, boolean remote) {
        if (conn == null) {
            logger.error("Received null connection in onClose");
            return;
        }
        clients.remove(conn);
        logger.info("Closed connection to: {}", conn.getRemoteSocketAddress());
    }

    @Override
    public void onMessage(WebSocket conn, String message) {
        if (conn == null || message == null) {
            logger.error("Received null connection or message in onMessage");
            return;
        }

        try {
            ObjectNode data = (ObjectNode) objectMapper.readTree(message);
            logger.debug("Received message: {}", data);

            String type = data.path("type").asText();
            switch (type) {
                case "FRACTAL_CONFIG":
                    fractalConfig.putAll(objectMapper.convertValue(data.path("config"), Map.class));
                    broadcast("fractalConfigAck", Map.of("status", "received"));
                    break;
                case "META_INTERVENTION":
                    handleMetaIntervention(data.path("intervention"));
                    break;
                default:
                    logger.warn("Unknown message type: {}", type);
                    break;
            }
        } catch (Exception e) {
            logger.error("Error processing message: {}", message, e);
        }
    }

    @Override
    public void onError(WebSocket conn, Exception ex) {
        if (conn != null) {
            clients.remove(conn);
            logger.error("WebSocket error for connection {}: {}", conn.getRemoteSocketAddress(), ex.getMessage(), ex);
        } else {
            logger.error("WebSocket error: {}", ex.getMessage(), ex);
        }
    }

    @Override
    public void onStart() {
        logger.info("WebSocket server started on {}", getAddress());
    }

    public void broadcast(String messageType, Object data) {
        if (clients.isEmpty()) {
            return;
        }

        try {
            ObjectNode message = objectMapper.createObjectNode()
                .put("type", messageType)
                .put("timestamp", System.currentTimeMillis());
            message.set("data", objectMapper.valueToTree(data));

            String messageJson = objectMapper.writeValueAsString(message);
            broadcast(messageJson);
            logger.debug("Broadcast message: {}", message);
        } catch (Exception e) {
            logger.error("Error broadcasting message: {}", e.getMessage(), e);
        }
    }

    public void sendThoughtUpdate(Map<String, Object> thoughtData) {
        if (fractalConfig.size() > 0) {
            thoughtData = transformThoughtForFractal(thoughtData);
        }
        broadcast("thoughtUpdate", thoughtData);
    }

    private Map<String, Object> transformThoughtForFractal(Map<String, Object> thoughtData) {
        return Map.of(
            "id", thoughtData.getOrDefault("id", UUID.randomUUID().toString()),
            "prompt", thoughtData.get("prompt"),
            "result", thoughtData.get("result"),
            "metadata", thoughtData.getOrDefault("metadata", Map.of()),
            "fractalData", Map.of(
                "level", thoughtData.getOrDefault("processingLevel", "mesoLevel"),
                "iteration", thoughtData.getOrDefault("iterationCount", 1),
                "timestamp", thoughtData.get("timestamp"),
                "transformations", applyFractalTransformations(thoughtData)
            )
        );
    }

    private void handleMetaIntervention(JsonNode intervention) {
        try {
            broadcast("metaIntervention", intervention);
        } catch (Exception e) {
            logger.error("Error handling meta intervention: {}", e.getMessage(), e);
        }
    }

    private List<Map<String, Object>> applyFractalTransformations(Map<String, Object> thoughtData) {
        List<Map<String, Object>> transformations = new ArrayList<>();
        if (fractalConfig.size() > 0 && fractalConfig.containsKey("transformations")) {
            // Apply transformations based on fractal config
            // This is a simplified version - actual implementation would depend on transformation rules
        }
        return transformations;
    }
}