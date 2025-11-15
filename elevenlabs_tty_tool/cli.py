"""CLI entry point for elevenlabs-tty-tool.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import click

from elevenlabs_tty_tool.commands import (
    info,
    list_models,
    list_voices,
    pricing,
    synthesize,
    update_voices,
)


@click.group()
@click.version_option(version="0.2.0")
def main() -> None:
    """
    ElevenLabs TTS CLI - Professional text-to-speech synthesis.

    Convert text to natural-sounding speech using ElevenLabs' advanced AI voices.
    """
    pass


# Register commands
main.add_command(synthesize)
main.add_command(list_voices)
main.add_command(list_models)
main.add_command(pricing)
main.add_command(info)
main.add_command(update_voices)


if __name__ == "__main__":
    main()
