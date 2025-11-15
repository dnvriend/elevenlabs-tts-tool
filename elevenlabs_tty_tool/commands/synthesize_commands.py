"""
Synthesize command implementation.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import sys
from pathlib import Path

import click

from elevenlabs_tty_tool.core.client import get_client
from elevenlabs_tty_tool.core.synthesize import play_speech, read_from_stdin, save_speech
from elevenlabs_tty_tool.models import DEFAULT_MODEL, get_deprecation_warning, validate_model
from elevenlabs_tty_tool.voices import VoiceManager


@click.command()
@click.argument("text", required=False)
@click.option(
    "--stdin",
    "-s",
    is_flag=True,
    help="Read text from stdin instead of argument",
)
@click.option(
    "--voice",
    "-v",
    default="rachel",
    help="Voice name or ID (default: rachel)",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(path_type=Path),
    help="Save audio to file instead of playing",
)
@click.option(
    "--format",
    "-f",
    default="mp3_44100_128",
    help="Output format (default: mp3_44100_128). Common: mp3_44100_128, pcm_44100, pcm_24000",
)
@click.option(
    "--model",
    "-m",
    default=DEFAULT_MODEL,
    help=f"Model ID (default: {DEFAULT_MODEL}). Run 'elevenlabs-tty-tool list-models' to see all.",
)
def synthesize(
    text: str | None, stdin: bool, voice: str, output: Path | None, format: str, model: str
) -> None:
    """
    Convert text to speech using ElevenLabs TTS.

    By default, synthesizes text and plays through speakers (MP3 format).
    Use --output to save to a file instead. Use --format to change audio format.

    \b
    Examples:

    \b
        # Play text with default voice (rachel) and default model (turbo v2.5)
        elevenlabs-tty-tool synthesize "Hello world"

    \b
        # Use different voice
        elevenlabs-tty-tool synthesize "Hello world" --voice adam

    \b
        # Use highest quality model
        elevenlabs-tty-tool synthesize "Hello world" \\
            --model eleven_multilingual_v2

    \b
        # Ultra-low latency for real-time applications
        elevenlabs-tty-tool synthesize "Hello world" \\
            --model eleven_flash_v2_5

    \b
        # Emotional expression (requires eleven_v3 model)
        elevenlabs-tty-tool synthesize "[happy] Welcome!" \\
            --model eleven_v3

    \b
        # Read from stdin
        echo "Hello world" | elevenlabs-tty-tool synthesize --stdin

    \b
        # Save to MP3 file (default format)
        elevenlabs-tty-tool synthesize "Hello world" --output speech.mp3

    \b
        # Save to WAV file (PCM format, 24kHz)
        elevenlabs-tty-tool synthesize "Hello world" \\
            --output speech.wav --format pcm_24000

    \b
        # Lower quality MP3 (smaller file)
        elevenlabs-tty-tool synthesize "Hello world" \\
            --output speech.mp3 --format mp3_22050_32

    \b
    Output Formats:
        All tiers: mp3_44100_128 (default), mp3_22050_32, pcm_16000,
                   pcm_22050, pcm_24000, ulaw_8000
        Creator+:  mp3_44100_192
        Pro+:      pcm_44100

    \b
    Models:
        Run 'elevenlabs-tty-tool list-models' to see all available models.
        Note: Emotional tags ([happy], [sad], etc.) only work with eleven_v3.
    """
    try:
        # Get text from stdin or argument
        if stdin:
            input_text = read_from_stdin()
        elif text:
            input_text = text
        else:
            click.echo(
                "Error: No text provided.\n"
                "Provide text as argument or use --stdin flag.\n\n"
                "Examples:\n"
                "  elevenlabs-tty-tool synthesize 'Hello world'\n"
                "  echo 'Hello world' | elevenlabs-tty-tool synthesize --stdin",
                err=True,
            )
            sys.exit(1)

        # Validate model
        model_id = validate_model(model)

        # Show deprecation warning if needed
        warning = get_deprecation_warning(model_id)
        if warning:
            click.echo(f"\n{warning}\n", err=True)

        # Initialize client and voice manager
        client = get_client()
        voice_manager = VoiceManager()
        voice_id = voice_manager.get_voice_id(voice)

        # Synthesize and play or save
        if output:
            save_speech(client, input_text, voice_id, output, format, model_id)
            click.echo(f"Audio saved to: {output}")
        else:
            play_speech(client, input_text, voice_id, format, model_id)

    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
