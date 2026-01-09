"""
4D-ARE Experiment Configuration
使用 Ilya 提供的 OpenAI compatible API
"""

# API Configuration
OPENAI_COMPATIBLE_BASE_URL = "https://xiaoai.plus/v1"
OPENAI_COMPATIBLE_API_KEY = "sk-YKdSSGVtZ6fuioo3tCa4lIR5WwdYCxzRjoPUJHnY9A2BaLSE"

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
