package com.amazon.novaact.types;

/**
 * Metadata for an act() operation.
 */
public class ActMetadata {
    private final String sessionId;
    private final String actId;
    private final int numStepsExecuted;
    private final double startTime;
    private final double endTime;
    private final String prompt;

    public ActMetadata(String sessionId, String actId, int numStepsExecuted,
                      double startTime, double endTime, String prompt) {
        this.sessionId = sessionId;
        this.actId = actId;
        this.numStepsExecuted = numStepsExecuted;
        this.startTime = startTime;
        this.endTime = endTime;
        this.prompt = prompt;
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

    public double getStartTime() {
        return startTime;
    }

    public double getEndTime() {
        return endTime;
    }

    public String getPrompt() {
        return prompt;
    }

    public static class Builder {
        private String sessionId;
        private String actId;
        private int numStepsExecuted;
        private double startTime;
        private double endTime;
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

        public Builder startTime(double startTime) {
            this.startTime = startTime;
            return this;
        }

        public Builder endTime(double endTime) {
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