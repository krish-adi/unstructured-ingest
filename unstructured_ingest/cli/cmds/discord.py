import typing as t
from dataclasses import dataclass

import click

from unstructured_ingest.cli.base.src import BaseSrcCmd
from unstructured_ingest.cli.interfaces import (
    CliConfig,
    DelimitedString,
)
from unstructured_ingest.connector.discord import SimpleDiscordConfig


@dataclass
class DiscordCliConfig(SimpleDiscordConfig, CliConfig):
    @staticmethod
    def get_cli_options() -> t.List[click.Option]:
        options = [
            click.Option(
                ["--token"],
                required=True,
                help="Bot token used to access Discord API, must have "
                "READ_MESSAGE_HISTORY scope for the bot user",
            ),
            click.Option(
                ["--channels"],
                required=True,
                type=DelimitedString(),
                help="Comma-delimited list of discord channel ids to ingest from.",
            ),
            click.Option(
                ["--period"],
                default=None,
                type=click.IntRange(0),
                help="Number of days to go back in the history of "
                "discord channels, must be a number",
            ),
        ]
        return options


def get_base_src_cmd() -> BaseSrcCmd:
    cmd_cls = BaseSrcCmd(
        cmd_name="discord",
        cli_config=DiscordCliConfig,
    )
    return cmd_cls
