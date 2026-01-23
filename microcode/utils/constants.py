import os


# Modaic
MODAIC_REPO_PATH = "farouk1/nanocode"


# Display
DEFAULT_HISTORY_LIMIT = 5
BANNER_ART = """
                      ▓██████▓                                          
                    ░██████████░                                        
            ▒█▒     ████████████                                        
             ▓▓    ▓████████████▓                                       
            ▓█▒    ▓█████████████      ░▓▓▓▒                            
           ▒██     ▓████████████▒     ██▓░ ░▓▓░                         
           ▒██▓     ▓███████████     ██▓                                
            ▓███▓    ▓█████████    ▒███▓  ▒██░                          
       ▓███▒  ██████▒▒████████▓▒██████▓  ▓█▓ ▒▓                         
     ▒█████████▒▓███████████████████▒   ▓█▓                             
     ▓▓     ▒█████████████████████▓   ▒███▒                             
     ▓▒        ░▓████████████████████████▒                              
              ██████▓▓██████████▒  ░░░░                                  
             ▓██▒   ░███▓ ███▒▓██▓                                      
             ▓██   ▓██▓    ▓██░▒█████████▓   * powered by modaic *                           
       ▒▒   ▓██▒  ███       ░██▓  ░▒▒░  ░█▒                             
         ▓████▒   ██▒        ███                                        
                  ▒███▒    ▓██▓                                         
""".strip("\n")

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
BLUE = "\033[34m"
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
MAGENTA = "\033[35m"


# Cache
CACHE_DIR = os.path.join(
    os.getenv("XDG_CACHE_HOME", os.path.expanduser("~/.cache")),
    "microcode",
)
OPENROUTER_KEY_PATH = os.path.join(CACHE_DIR, "openrouter_key.json")
MODEL_CONFIG_PATH = os.path.join(CACHE_DIR, "model_config.json")
SETTINGS_CONFIG_PATH = os.path.join(CACHE_DIR, "settings_config.json")

# Models
AVAILABLE_MODELS = {
    "1": ("GPT-5.2 Codex", "openai/gpt-5.2-codex"),
    "2": ("GPT-5.2", "openai/gpt-5.2"),
    "3": ("Claude Opus 4.5", "anthropic/claude-opus-4.5"),
    "4": ("Claude Opus 4", "anthropic/claude-opus-4"),
    "5": ("Qwen 3 Coder", "qwen/qwen3-coder"),
    "6": ("Gemini 3 Flash Preview", "google/gemini-3-flash-preview"),
    "7": ("Kimi K2 0905", "moonshotai/kimi-k2-0905"),
    "8": ("Minimax M2.1", "minimax/minimax-m2.1"),
}
