import { defineRailway, github, preserve, project, service, volume } from "railway/iac";

export default defineRailway(() => {
  const foodData = volume("food-data", {
    alerts: { usage: { "100": {}, "80": {}, "95": {} } },
    allowOnlineResize: true,
    region: "us-east4-eqdc4a",
    sizeMB: 500,
  });

  const pantryManager = service("pantry-manager", {
    source: github("awbjcj/pantry-manager", { branch: "master", checkSuites: false }),
    build: { buildEnvironment: "V3", builder: "DOCKERFILE", dockerfilePath: "Dockerfile" },
    start: "uv run --no-sync python bin/run.py",
    healthcheck: "/healthz",
    healthcheckTimeout: 120,
    replicas: { "us-east4-eqdc4a": 1 },
    deploy: { restartPolicyType: "ON_FAILURE", restartPolicyMaxRetries: 5 },
    networking: { privateNetworkEndpoint: "food-manager" },
    volumeMounts: { "/data": foodData },
    // Values remain in Railway; only their names are managed here.
    env: {
      ALLOWED_TELEGRAM_USER_ID: preserve(),
      ANTHROPIC_API_KEY: preserve(),
      ANTHROPIC_BASE_URL: preserve(),
      ANTHROPIC_MODEL: preserve(),
      ANTHROPIC_SEARCH_MODEL: preserve(),
      ANTHROPIC_TEXT_MODEL: preserve(),
      BILLING_ENABLED: preserve(),
      DEEPSEEK_API_KEY: preserve(),
      DEEPSEEK_MODEL: preserve(),
      ENV: preserve(),
      GEMINI_API_KEY: preserve(),
      GEMINI_MODEL: preserve(),
      GEMINI_TEXT_MODEL: preserve(),
      HOSTED_FEATURES_ENABLED: preserve(),
      LLM_PROVIDER: preserve(),
      OPENAI_API_KEY: preserve(),
      OPENAI_BASE_URL: preserve(),
      OPENAI_MODEL: preserve(),
      OPENAI_TEXT_MODEL: preserve(),
      OPEN_REGISTRATION: preserve(),
      OPERATOR_BOT_TOKEN: preserve(),
      OPERATOR_TELEGRAM_IDS: preserve(),
      SPOONACULAR_API_KEY: preserve(),
      SUB2API_ANTHROPIC_TOKEN: preserve(),
      SUB2API_BASE_URL: preserve(),
      SUB2API_OPENAI_TOKEN: preserve(),
      TELEGRAM_BOT_TOKEN: preserve(),
      WEB_APP_URL: preserve(),
    },
  });

  return project("pantry-manager", {
    variables: { managed: true },
    resources: [pantryManager, foodData],
  });
});
