import json
from typing import Dict
from dataclasses import dataclass


@dataclass
class FormConfig:
    """Form filling configuration."""
    enabled: bool = True
    fill_delay: int = 100
    defaults: Dict[str, str] = None  # selector -> value mapping
    
    def __post_init__(self):
        if self.defaults is None:
            self.defaults = {}


@dataclass
class Config:
    """Main configuration class."""
    start_url: str
    max_depth: int
    max_clicks_per_page: int
    wait_timeout: int = 30000
    network_idle_timeout: int = 2000
    http_credentials: Dict[str, str] = None
    form_filling: FormConfig = None
    exclude_patterns: list = None
    output_file: str = "mappings_output.json"

    def __post_init__(self):
        if self.exclude_patterns is None:
            self.exclude_patterns = ["logout", "delete", "remove"]


def load_config(config_path: str) -> Config:
    """Load configuration from JSON file."""
    with open(config_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    http_credentials = None
    if 'http_credentials' in data:
        http_credentials = data['http_credentials']

    # Parse form config
    form_config = None
    if 'form_filling' in data:
        form_data = data['form_filling']
        form_config = FormConfig(
            enabled=form_data.get('enabled', True),
            fill_delay=form_data.get('fill_delay', 100),
            defaults=form_data.get('defaults', {})
        )
    else:
        # Default enabled with no specific defaults
        form_config = FormConfig()

    return Config(
        start_url=data['start_url'],
        max_depth=data.get('max_depth', 3),
        max_clicks_per_page=data.get('max_clicks_per_page', 20),
        wait_timeout=data.get('wait_timeout', 30000),
        network_idle_timeout=data.get('network_idle_timeout', 2000),
        http_credentials=http_credentials,
        form_filling=form_config,
        exclude_patterns=data.get('exclude_patterns', []),
        output_file=data.get('output_file', 'mappings_output.json')
    )

