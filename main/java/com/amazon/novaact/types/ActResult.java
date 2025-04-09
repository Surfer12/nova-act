package com.amazon.novaact.types;

import com.fasterxml.jackson.databind.JsonNode;
import java.util.Optional;

/**
 * Result of an act() operation.
 */
public class ActResult {
    private final String response;
    private final JsonNode parsedResponse;
    private final boolean validJson;
    private final boolean matchesSchema;
    private final ActMetadata metadata;
    private final boolean success;
    private final String result;
    private final String processingLevel;
    private final int iterationCount;

    public ActResult(String response, JsonNode parsedResponse, boolean validJson, 
                    boolean matchesSchema, ActMetadata metadata, boolean success,
                    String result, String processingLevel, int iterationCount) {
        this.response = response;
        this.parsedResponse = parsedResponse;
        this.validJson = validJson;
        this.matchesSchema = matchesSchema;
        this.metadata = metadata;
        this.success = success;
        this.result = result;
        this.processingLevel = processingLevel;
        this.iterationCount = iterationCount;
    }

    public String getResponse() {
        return response;
    }

    public Optional<JsonNode> getParsedResponse() {
        return Optional.ofNullable(parsedResponse);
    }

    public boolean isValidJson() {
        return validJson;
    }

    public boolean matchesSchema() {
        return matchesSchema;
    }

    public ActMetadata getMetadata() {
        return metadata;
    }

    public boolean isSuccess() {
        return success;
    }

    public String getResult() {
        return result;
    }

    public String getProcessingLevel() {
        return processingLevel;
    }

    public int getIterationCount() {
        return iterationCount;
    }

    public static class Builder {
        private String response;
        private JsonNode parsedResponse;
        private boolean validJson;
        private boolean matchesSchema;
        private ActMetadata metadata;
        private boolean success;
        private String result;
        private String processingLevel = "mesoLevel";
        private int iterationCount = 1;

        public Builder response(String response) {
            this.response = response;
            return this;
        }

        public Builder parsedResponse(JsonNode parsedResponse) {
            this.parsedResponse = parsedResponse;
            return this;
        }

        public Builder validJson(boolean validJson) {
            this.validJson = validJson;
            return this;
        }

        public Builder matchesSchema(boolean matchesSchema) {
            this.matchesSchema = matchesSchema;
            return this;
        }

        public Builder metadata(ActMetadata metadata) {
            this.metadata = metadata;
            return this;
        }

        public Builder success(boolean success) {
            this.success = success;
            return this;
        }

        public Builder result(String result) {
            this.result = result;
            return this;
        }

        public Builder processingLevel(String processingLevel) {
            this.processingLevel = processingLevel;
            return this;
        }

        public Builder iterationCount(int iterationCount) {
            this.iterationCount = iterationCount;
            return this;
        }

        public ActResult build() {
            return new ActResult(response, parsedResponse, validJson, matchesSchema,
                               metadata, success, result, processingLevel, iterationCount);
        }
    }
}