"""
4D-ARE Experiment Configuration

API credentials are read from environment variables (or a `.env` file):
    OPENAI_COMPATIBLE_API_KEY   (required)
    OPENAI_COMPATIBLE_BASE_URL  (optional, defaults to the OpenAI API)
"""

import os

from dotenv import load_dotenv

load_dotenv()

# API Configuration
OPENAI_COMPATIBLE_BASE_URL = os.environ.get(
    "OPENAI_COMPATIBLE_BASE_URL", "https://api.openai.com/v1"
)
OPENAI_COMPATIBLE_API_KEY = os.environ.get("OPENAI_COMPATIBLE_API_KEY")

if not OPENAI_COMPATIBLE_API_KEY:
    raise RuntimeError(
        "OPENAI_COMPATIBLE_API_KEY is not set. Export it in your shell or add it "
        "to a .env file (see .env.example) before running the experiment."
    )

# Experiment Parameters
NUM_SCENARIOS = 150          # 目标样本量
BATCH_SIZE = 10              # 每批生成的场景数（避免 API 过载）

# Model Selection
MODEL_GENERATOR = "gpt-4-turbo"   # 场景生成器
MODEL_AGENT = "gpt-4o"            # Agent 执行
MODEL_JUDGE = "gpt-4o"            # 评估裁判

# Output Paths
SCENARIOS_PATH = "data/scenarios.json"
RESULTS_PATH = "data/results.csv"
DETAILED_RESULTS_PATH = "data/detailed_results.json"
HUMAN_CALIBRATION_PATH = "human_calibration.csv"

# Retry Configuration
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds
