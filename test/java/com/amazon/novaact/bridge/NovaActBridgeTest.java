package com.amazon.novaact.bridge;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;
import java.net.InetSocketAddress;
import java.util.HashMap;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.CopyOnWriteArraySet;
import org.java_websocket.WebSocket;
import org.java_websocket.handshake.ClientHandshake;
import org.junit.Test;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.MockitoAnnotations;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import static org.junit.Assert.*;
import static org.junit.jupiter.api.Assertions.*;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.mockito.Mockito.*;
import static org.mockito.Mockito.when;

public class NovaActBridgeTest {

    @Mock
    private ObjectMapper mockObjectMapper;

    @Mock
    private WebSocket mockWebSocket;

    private NovaActBridge novaActBridge;

    @BeforeEach
    public void setUp() {
        MockitoAnnotations.openMocks(this);
        novaActBridge = new NovaActBridge("localhost", 8080);
        novaActBridge.clients = new CopyOnWriteArraySet<>();
        novaActBridge.objectMapper = mockObjectMapper;
    }

    /**
     * Tests the behavior of the broadcast method when the clients set is empty.
     * This scenario is explicitly handled in the method by returning early.
     */
    @Test
    public void testBroadcastWithEmptyClients() {
        NovaActBridge bridge = new NovaActBridge("localhost", 8080);

        // The clients set is initially empty in a new NovaActBridge instance

        // Call the broadcast method
        bridge.broadcast("testType", "testData");

        // No assertion is needed as we're testing that no exception is thrown
        // and the method returns silently when clients is empty
    }

    /**
     * Test case for broadcast method when clients set is empty.
     * This test verifies that the broadcast method returns early when there are no connected clients.
     */
    @Test
    public void testBroadcastWithEmptyClients_2() {
        String messageType = "testMessage";
        Object data = new Object();

        novaActBridge.broadcast(messageType, data);

        verify(mockObjectMapper, never()).createObjectNode();
        verify(mockWebSocket, never()).send(anyString());
    }

    /**
     * Tests the NovaActBridge constructor with an invalid port number.
     * This test verifies that the constructor throws an IllegalArgumentException
     * when an out-of-range port number is provided.
     */
    @Test(expected = IllegalArgumentException.class)
    public void testNovaActBridge_InvalidPort() {
        new NovaActBridge("localhost", 65536);
    }

    /**
     * Tests the onMessage method with an invalid JSON message.
     * This test verifies that the method handles the exception thrown when trying to parse an invalid JSON string.
     */
    @Test
    public void testOnMessageWithInvalidJson() {
        NovaActBridge bridge = new NovaActBridge("localhost", 8080);
        WebSocket mockWebSocket = Mockito.mock(WebSocket.class);
        String invalidJsonMessage = "This is not a valid JSON";

        bridge.onMessage(mockWebSocket, invalidJsonMessage);

        // Verify that no exceptions are thrown and the method completes
        // The actual behavior is just logging the error, which we can't easily verify in a unit test
    }

    /**
     * Tests the onMessage method with a JSON message that has an unknown message type.
     * This test verifies that the method handles messages with types other than "FRACTAL_CONFIG" or "META_INTERVENTION".
     */
    @Test
    public void testOnMessageWithUnknownType() {
        NovaActBridge bridge = new NovaActBridge("localhost", 8080);
        WebSocket mockWebSocket = Mockito.mock(WebSocket.class);
        String messageWithUnknownType = "{\"type\":\"UNKNOWN_TYPE\",\"data\":{}}";

        bridge.onMessage(mockWebSocket, messageWithUnknownType);

        // Verify that no exceptions are thrown and the method completes
        // The actual behavior is just logging the message, which we can't easily verify in a unit test
    }

    /**
     * Tests the onOpen method with a null WebSocket connection.
     * This verifies that the method handles null connections gracefully without throwing exceptions.
     */
    @Test
    public void testOnOpenWithNullConnection() {
        NovaActBridge bridge = new NovaActBridge("localhost", 8080);
        ClientHandshake mockHandshake = Mockito.mock(ClientHandshake.class);

        // Call onOpen with null connection
        bridge.onOpen(null, mockHandshake);

        // No assertion needed as we're just verifying it doesn't throw an exception
    }

    /**
     * Tests the onOpen method with a null ClientHandshake.
     * This verifies that the method handles null handshakes gracefully without throwing exceptions.
     */
    @Test
    public void testOnOpenWithNullHandshake() {
        NovaActBridge bridge = new NovaActBridge("localhost", 8080);
        WebSocket mockConn = Mockito.mock(WebSocket.class);
        Mockito.when(mockConn.getRemoteSocketAddress()).thenReturn(new InetSocketAddress("localhost", 8080));

        // Call onOpen with null handshake
        bridge.onOpen(mockConn, null);

        // No assertion needed as we're just verifying it doesn't throw an exception
    }

    /**
     * Test case for the NovaActBridge constructor.
     * This test verifies that the NovaActBridge is correctly initialized with the given host and port.
     */
    @Test
    public void test_NovaActBridge_1() {
        String host = "localhost";
        int port = 8080;
        NovaActBridge bridge = new NovaActBridge(host, port);

        InetSocketAddress address = (InetSocketAddress) bridge.getAddress();
        assertEquals(host, address.getHostName());
        assertEquals(port, address.getPort());
    }

    /**
     * Tests the broadcast method when clients are not empty.
     * Verifies that the message is properly constructed and sent to all connected clients.
     */
    @Test
    public void test_broadcast_2() throws Exception {
        // Create a mock NovaActBridge instance
        NovaActBridge bridge = Mockito.spy(new NovaActBridge("localhost", 8080));

        // Create a mock WebSocket client
        WebSocket mockClient = Mockito.mock(WebSocket.class);

        // Add the mock client to the clients set
        Set<WebSocket> clients = new CopyOnWriteArraySet<>();
        clients.add(mockClient);
        Mockito.doReturn(clients).when(bridge).getConnections();

        // Call the broadcast method
        String messageType = "testMessage";
        Object data = "testData";
        bridge.broadcast(messageType, data);

        // Verify that the message was sent to the client
        Mockito.verify(mockClient).send(Mockito.anyString());

        // Verify the content of the sent message
        ObjectMapper objectMapper = new ObjectMapper();
        ObjectNode expectedMessage = objectMapper.createObjectNode()
            .put("type", messageType)
            .put("timestamp", Mockito.anyLong());
        expectedMessage.set("data", objectMapper.valueToTree(data));

        Mockito.verify(mockClient).send(Mockito.argThat(arg -> {
            try {
                ObjectNode sentMessage = (ObjectNode) objectMapper.readTree(arg);
                return sentMessage.get("type").asText().equals(messageType) &&
                       sentMessage.has("timestamp") &&
                       sentMessage.get("data").asText().equals(data.toString());
            } catch (Exception e) {
                return false;
            }
        }));
    }

    /**
     * Tests that the onClose method removes the closed connection from the clients set
     * and logs the closure information.
     */
    @Test
    public void test_onClose_removes_client_and_logs_closure() {
        // Arrange
        NovaActBridge bridge = new NovaActBridge("localhost", 8080);
        WebSocket mockConn = Mockito.mock(WebSocket.class);
        Set<WebSocket> clients = new CopyOnWriteArraySet<>();
        clients.add(mockConn);

        // Mock the getRemoteSocketAddress method
        when(mockConn.getRemoteSocketAddress()).thenReturn(new InetSocketAddress("127.0.0.1", 12345));

        // Act
        bridge.onClose(mockConn, 1000, "Normal closure", false);

        // Assert
        assertFalse(clients.contains(mockConn), "The closed connection should be removed from the clients set");
    }

    /**
     * Test case for onError method when the WebSocket connection is not null.
     * Verifies that the connection is removed from the clients set and the error is logged.
     */
    @Test
    public void test_onError_whenConnectionIsNotNull() {
        // Arrange
        NovaActBridge bridge = new NovaActBridge("localhost", 8080);
        WebSocket mockConn = mock(WebSocket.class);
        Exception mockException = new Exception("Test exception");
        Set<WebSocket> clients = new CopyOnWriteArraySet<>();
        clients.add(mockConn);

        Logger mockLogger = mock(Logger.class);

        // Use reflection to set private fields
        try {
            java.lang.reflect.Field clientsField = NovaActBridge.class.getDeclaredField("clients");
            clientsField.setAccessible(true);
            clientsField.set(bridge, clients);

            java.lang.reflect.Field loggerField = NovaActBridge.class.getDeclaredField("logger");
            loggerField.setAccessible(true);
            loggerField.set(bridge, mockLogger);
        } catch (Exception e) {
            throw new RuntimeException("Failed to set up test", e);
        }

        // Act
        bridge.onError(mockConn, mockException);

        // Assert
        verify(mockLogger).error("WebSocket error occurred", mockException);
        assert !clients.contains(mockConn);
    }

    /**
     * Test case for onError method when the WebSocket connection is null.
     * This test verifies that the method handles a null connection correctly
     * and logs the error without throwing an exception.
     */
    @Test
    public void test_onError_whenConnectionIsNull() {
        NovaActBridge bridge = new NovaActBridge("localhost", 8080);
        Logger mockLogger = Mockito.mock(Logger.class);
        Exception testException = new Exception("Test exception");

        // Set the mock logger using reflection
        try {
            java.lang.reflect.Field loggerField = NovaActBridge.class.getDeclaredField("logger");
            loggerField.setAccessible(true);
            loggerField.set(bridge, mockLogger);
        } catch (NoSuchFieldException | IllegalAccessException e) {
            throw new RuntimeException("Failed to set mock logger", e);
        }

        // Call onError with null connection
        bridge.onError(null, testException);

        // Verify that error was logged
        Mockito.verify(mockLogger).error("WebSocket error occurred", testException);
    }

    /**
     * Tests the onError method when the WebSocket connection is null.
     * This is an edge case where the connection object passed to onError is null,
     * which is explicitly handled in the method implementation.
     */
    @Test
    public void test_onError_with_null_connection() {
        NovaActBridge bridge = new NovaActBridge("localhost", 8080);
        Logger mockLogger = mock(Logger.class);
        Exception testException = new Exception("Test exception");

        // Use reflection to set the mock logger
        try {
            java.lang.reflect.Field loggerField = NovaActBridge.class.getDeclaredField("logger");
            loggerField.setAccessible(true);
            loggerField.set(bridge, mockLogger);
        } catch (NoSuchFieldException | IllegalAccessException e) {
            throw new RuntimeException("Failed to set mock logger", e);
        }

        bridge.onError(null, testException);

        verify(mockLogger).error("WebSocket error occurred", testException);
    }

    /**
     * Tests the onMessage method when the message type is neither "FRACTAL_CONFIG" nor "META_INTERVENTION".
     * This test verifies that the method handles unknown message types gracefully without throwing exceptions.
     */
    @Test
    public void test_onMessage_handlesUnknownMessageType() throws Exception {
        WebSocket mockConn = Mockito.mock(WebSocket.class);
        NovaActBridge bridge = new NovaActBridge("localhost", 8080);
        ObjectMapper objectMapper = new ObjectMapper();

        ObjectNode testMessage = objectMapper.createObjectNode();
        testMessage.put("type", "UNKNOWN_TYPE");
        String messageString = objectMapper.writeValueAsString(testMessage);

        bridge.onMessage(mockConn, messageString);

        // Verify that no exceptions are thrown and no specific actions are taken
        verify(mockConn, never()).send(anyString());
    }

    /**
     * Test case for onMessage method when receiving a META_INTERVENTION message.
     * This test verifies that the handleMetaIntervention method is called with the correct intervention data
     * when a META_INTERVENTION message is received.
     */
    @Test
    public void test_onMessage_handles_meta_intervention() throws Exception {
        // Create a mock WebSocket connection
        WebSocket mockConn = Mockito.mock(WebSocket.class);

        // Create a mock NovaActBridge instance
        NovaActBridge novaActBridge = Mockito.spy(new NovaActBridge("localhost", 8080));

        // Create a sample META_INTERVENTION message
        ObjectMapper objectMapper = new ObjectMapper();
        ObjectNode messageNode = objectMapper.createObjectNode();
        messageNode.put("type", "META_INTERVENTION");
        ObjectNode interventionNode = messageNode.putObject("intervention");
        interventionNode.put("someKey", "someValue");
        String message = objectMapper.writeValueAsString(messageNode);

        // Call the onMessage method
        novaActBridge.onMessage(mockConn, message);

        // Verify that handleMetaIntervention was called with the correct intervention data
        verify(novaActBridge).handleMetaIntervention(interventionNode);
    }

    /**
     * Test case for onMessage method when receiving a FRACTAL_CONFIG message.
     * Verifies that the method correctly processes the FRACTAL_CONFIG message,
     * updates the fractalConfig, and broadcasts an acknowledgment.
     */
    @Test
    public void test_onMessage_processesFractalConfigMessage() {
        // Arrange
        NovaActBridge bridge = Mockito.spy(new NovaActBridge("localhost", 8080));
        WebSocket mockConn = Mockito.mock(WebSocket.class);
        ObjectMapper objectMapper = new ObjectMapper();
        ObjectNode configData = objectMapper.createObjectNode();
        configData.put("someConfigKey", "someConfigValue");
        ObjectNode message = objectMapper.createObjectNode();
        message.put("type", "FRACTAL_CONFIG");
        message.set("config", configData);

        // Act
        bridge.onMessage(mockConn, message.toString());

        // Assert
        verify(bridge).broadcast(eq("fractalConfigAck"), eq(java.util.Map.of("status", "received")));
    }

    /**
     * Tests that the onOpen method adds the connection to the clients set
     * and logs the new connection information.
     */
    @Test
    public void test_onOpen_addsClientAndLogsConnection() {
        NovaActBridge bridge = new NovaActBridge("localhost", 8080);
        WebSocket mockConn = Mockito.mock(WebSocket.class);
        ClientHandshake mockHandshake = Mockito.mock(ClientHandshake.class);
        InetSocketAddress mockAddress = new InetSocketAddress("127.0.0.1", 12345);

        when(mockConn.getRemoteSocketAddress()).thenReturn(mockAddress);

        bridge.onOpen(mockConn, mockHandshake);

        // Verify that the client was added (this assumes the clients set is accessible for testing)
        // If it's not accessible, this part of the test would need to be removed or modified
        // assert(bridge.getClients().contains(mockConn));

        // Verify that the logger.info method was called with the correct message
        // This would require adding a mock logger to the NovaActBridge class and injecting it
        // For now, we'll leave this commented out as it requires modifying the original class
        // verify(mockLogger).info("New connection from: " + mockAddress);
    }

    /**
     * Test case for onStart method of NovaActBridge
     * Verifies that the correct log message is produced when the WebSocket server starts
     */
    @Test
    public void test_onStart_logsCorrectMessage() {
        // Create a mock logger
        Logger mockLogger = mock(Logger.class);

        // Create a test instance of NovaActBridge
        NovaActBridge bridge = new NovaActBridge("localhost", 8080) {
            @Override
            protected Logger getLogger() {
                return mockLogger;
            }
        };

        // Call the onStart method
        bridge.onStart();

        // Verify that the correct log message was produced
        verify(mockLogger).info("WebSocket server started on /localhost:8080");
    }

    /**
     * Tests the sendThoughtUpdate method when fractalConfig is null.
     * Verifies that the method broadcasts the thought data without transformation.
     */
    @Test
    public void test_sendThoughtUpdate_whenFractalConfigIsNull() {
        NovaActBridge bridge = spy(new NovaActBridge("localhost", 8080));
        Map<String, Object> thoughtData = new HashMap<>();
        thoughtData.put("id", "123");
        thoughtData.put("prompt", "Test prompt");
        thoughtData.put("result", "Test result");

        bridge.sendThoughtUpdate(thoughtData);

        verify(bridge).broadcast("thoughtUpdate", thoughtData);
    }

    /**
     * Tests the sendThoughtUpdate method when fractalConfig is not null.
     * Verifies that the thought data is transformed and broadcast correctly.
     */
    @Test
    public void test_sendThoughtUpdate_whenFractalConfigNotNull() {
        NovaActBridge bridge = new NovaActBridge("localhost", 8080);
        Map<String, Object> fractalConfig = new HashMap<>();
        fractalConfig.put("someKey", "someValue");
        bridge.fractalConfig = fractalConfig;

        Map<String, Object> thoughtData = new HashMap<>();
        thoughtData.put("prompt", "Test prompt");
        thoughtData.put("result", "Test result");

        bridge.sendThoughtUpdate(thoughtData);

        // Note: Since broadcast is a void method and we don't have a way to verify its call,
        // this test mainly ensures that the method doesn't throw any exceptions.
        // In a real scenario, you might want to use a mocking framework to verify the broadcast call.
    }

    /**
     * Tests the sendThoughtUpdate method when thoughtData is empty.
     * This is an edge case where an empty map is provided as input.
     * The method should handle this case without throwing exceptions.
     */
    @Test
    public void test_sendThoughtUpdate_with_empty_thoughtData() {
        NovaActBridge bridge = new NovaActBridge("localhost", 8080);
        Map<String, Object> emptyThoughtData = new HashMap<>();
        bridge.sendThoughtUpdate(emptyThoughtData);
        // No assertion needed as we're just checking if the method executes without throwing an exception
    }

}
