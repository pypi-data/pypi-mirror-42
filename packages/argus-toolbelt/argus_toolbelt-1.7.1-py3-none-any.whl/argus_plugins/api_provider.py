from api_generator import load
from argus_cli import register_provider
from argus_cli.settings import settings


@register_provider()
def argus_api(apikey: str = None) -> None:
    """Argus CLI provider"""
    if apikey:
        settings["api"]["api_key"] = apikey

    load(settings["api"]["api_url"], settings["api"]["definitions"])
