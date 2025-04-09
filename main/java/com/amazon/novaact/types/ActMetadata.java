package com.amazon.novaact.types;

import java.time.Instant;

/**
 * Metadata for an act() operation.
 */
public class ActMetadata {
    private final String sessionId;
    private final String actId;
    private final int numStepsExecuted;
    private final Instant startTime;
    private final Instant endTime;
    private final String prompt;

    public ActMetadata(String sessionId, String actId, int numStepsExecuted,
                      Instant startTime, Instant endTime, String prompt) {
        this.sessionId = sessionId;
        this.actId = actId;
        this.numStepsExecuted = numStepsExecuted;
        this.startTime = startTime;
        this.endTime = endTime;
        this.prompt = prompt;
    }

    @Override
    public String toString() {
        return String.format("ActMetadata(sessionId=%s, actId=%s, numSteps=%d, start=%s, end=%s, prompt='%s')",
                sessionId, actId, numStepsExecuted, startTime, endTime, prompt);
    }

    public String getSessionId() {
        return sessionId;
    }

    public String getActId() {
        return actId;
    }

    public int getNumStepsExecuted() {
        return numStepsExecuted;
    }

    public Instant getStartTime() {
        return startTime;
    }

    public Instant getEndTime() {
        return endTime;
    }

    public String getPrompt() {
        return prompt;
    }

    public static class Builder {
        private String sessionId;
        private String actId;
        private int numStepsExecuted;
        private Instant startTime;
        private Instant endTime;
        private String prompt;

        public Builder sessionId(String sessionId) {
            this.sessionId = sessionId;
            return this;
        }

        public Builder actId(String actId) {
            this.actId = actId;
            return this;
        }

        public Builder numStepsExecuted(int numStepsExecuted) {
            this.numStepsExecuted = numStepsExecuted;
            return this;
        }

        public Builder startTime(Instant startTime) {
            this.startTime = startTime;
            return this;
        }

        public Builder endTime(Instant endTime) {
            this.endTime = endTime;
            return this;
        }

        public Builder prompt(String prompt) {
            this.prompt = prompt;
            return this;
        }

        public ActMetadata build() {
            return new ActMetadata(sessionId, actId, numStepsExecuted,
                                 startTime, endTime, prompt);
        }
    }
}