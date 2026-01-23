import os
import re
import sys
import click
from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import ANSI
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.lexers import Lexer
from prompt_toolkit.styles import Style

_SESSION = None
_PASTE_THRESHOLD = int(os.getenv("MICROCODE_PASTE_THRESHOLD", "2000"))
_LAST_PASTE = None
_PLACEHOLDER_RE = re.compile(r"^\[pasted \d+\+ chars\]$")


class _PlaceholderLexer(Lexer):
    def lex_document(self, document):
        lines = document.lines

        def get_line(lineno: int):
            line = lines[lineno]
            if _PLACEHOLDER_RE.match(line):
                return [("class:paste_placeholder", line)]
            return [("", line)]

        return get_line


def _get_session() -> PromptSession | None:
    global _SESSION
    if PromptSession is None:
        return None

    if _SESSION is None:
        bindings = KeyBindings()

        @bindings.add("enter")
        def _accept(event) -> None:
            event.app.exit(result=event.app.current_buffer.text)

        @bindings.add("c-j")
        def _insert_newline(event) -> None:
            event.app.current_buffer.insert_text("\n")

        if Keys is not None:

            @bindings.add(Keys.BracketedPaste)
            def _handle_bracketed_paste(event) -> None:
                pasted = event.data or ""
                if _PASTE_THRESHOLD > 0 and len(pasted) > _PASTE_THRESHOLD:
                    placeholder = f"[pasted {len(pasted)}+ chars]"
                    _store_paste(pasted, placeholder)
                    event.app.current_buffer.insert_text(placeholder)
                else:
                    _clear_paste()
                    event.app.current_buffer.insert_text(pasted)

        placeholder_style = None
        placeholder_lexer = None
        if Style is not None and Lexer is not None:
            placeholder_style = Style.from_dict({"paste_placeholder": "fg:ansimagenta"})
            placeholder_lexer = _PlaceholderLexer()

        _SESSION = PromptSession(
            multiline=True,
            key_bindings=bindings,
            style=placeholder_style,
            lexer=placeholder_lexer,
        )
    return _SESSION


def read_user_input(
    prompt: str,
) -> str:
    if not sys.stdin.isatty():
        if prompt:
            click.echo(prompt, nl=False)
        return sys.stdin.readline().rstrip("\n")

    try:
        session = _get_session()
        if session is None:
            return click.prompt(prompt, prompt_suffix="", show_default=False)

        formatted_prompt = ANSI(prompt) if ANSI is not None else prompt
        text = session.prompt(formatted_prompt)

        if _PASTE_THRESHOLD > 0 and len(text) > _PASTE_THRESHOLD:
            placeholder = f"[pasted {len(text)}+ chars]"
            _store_paste(text, placeholder)
            return placeholder

        return text

    except (click.Abort, KeyboardInterrupt, EOFError) as exc:
        raise KeyboardInterrupt from exc


def consume_paste_for_input(user_input: str) -> dict | None:
    global _LAST_PASTE
    if _LAST_PASTE is None:
        return None
    placeholder = _LAST_PASTE.get("placeholder")
    if placeholder and placeholder in user_input:
        payload = _LAST_PASTE
        _LAST_PASTE = None
        return payload
    _LAST_PASTE = None
    return None


def _store_paste(text: str, placeholder: str) -> None:
    global _LAST_PASTE
    _LAST_PASTE = {"text": text, "placeholder": placeholder}


def _clear_paste() -> None:
    global _LAST_PASTE
    _LAST_PASTE = None
