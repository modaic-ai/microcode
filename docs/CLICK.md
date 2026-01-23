API
This part of the documentation lists the full API reference of all public classes and functions.

Decorators

Utilities

Commands

Parameters

Context

Types

Exceptions

Formatting

Parsing

Shell Completion

Testing

Decorators
click.command(name: Callable[[...], Any]) → Command
click.command(name: str | None, cls: type[CmdType], **attrs: Any) → Callable[[Callable[[...], Any]], CmdType]
click.command(name: None = None, *, cls: type[CmdType], **attrs: Any) → Callable[[Callable[[...], Any]], CmdType]
click.command(name: str | None = None, cls: None = None, **attrs: Any) → Callable[[Callable[[...], Any]], Command]
Creates a new Command and uses the decorated function as callback. This will also automatically attach all decorated option()s and argument()s as parameters to the command.

The name of the command defaults to the name of the function, converted to lowercase, with underscores _ replaced by dashes -, and the suffixes _command, _cmd, _group, and _grp are removed. For example, init_data_command becomes init-data.

All keyword arguments are forwarded to the underlying command class. For the params argument, any decorated params are appended to the end of the list.

Once decorated the function turns into a Command instance that can be invoked as a command line utility or be attached to a command Group.

Parameters:
name – The name of the command. Defaults to modifying the function’s name as described above.

cls – The command class to create. Defaults to Command.

Changelog
click.group(name: Callable[[...], Any]) → Group
click.group(name: str | None, cls: type[GrpType], **attrs: Any) → Callable[[Callable[[...], Any]], GrpType]
click.group(name: None = None, *, cls: type[GrpType], **attrs: Any) → Callable[[Callable[[...], Any]], GrpType]
click.group(name: str | None = None, cls: None = None, **attrs: Any) → Callable[[Callable[[...], Any]], Group]
Creates a new Group with a function as callback. This works otherwise the same as command() just that the cls parameter is set to Group.

Changelog
click.argument(*param_decls, cls=None, **attrs)
Attaches an argument to the command. All positional arguments are passed as parameter declarations to Argument; all keyword arguments are forwarded unchanged (except cls). This is equivalent to creating an Argument instance manually and attaching it to the Command.params list.

For the default argument class, refer to Argument and Parameter for descriptions of parameters.

Parameters:
cls (type[Argument] | None) – the argument class to instantiate. This defaults to Argument.

param_decls (str) – Passed as positional arguments to the constructor of cls.

attrs (Any) – Passed as keyword arguments to the constructor of cls.

Return type:
Callable[[FC], FC]

click.option(*param_decls, cls=None, **attrs)
Attaches an option to the command. All positional arguments are passed as parameter declarations to Option; all keyword arguments are forwarded unchanged (except cls). This is equivalent to creating an Option instance manually and attaching it to the Command.params list.

For the default option class, refer to Option and Parameter for descriptions of parameters.

Parameters:
cls (type[Option] | None) – the option class to instantiate. This defaults to Option.

param_decls (str) – Passed as positional arguments to the constructor of cls.

attrs (Any) – Passed as keyword arguments to the constructor of cls.

Return type:
Callable[[FC], FC]

click.password_option(*param_decls, **kwargs)
Add a --password option which prompts for a password, hiding input and asking to enter the value again for confirmation.

Parameters:
param_decls (str) – One or more option names. Defaults to the single value "--password".

kwargs (Any) – Extra arguments are passed to option().

Return type:
Callable[[FC], FC]

click.confirmation_option(*param_decls, **kwargs)
Add a --yes option which shows a prompt before continuing if not passed. If the prompt is declined, the program will exit.

Parameters:
param_decls (str) – One or more option names. Defaults to the single value "--yes".

kwargs (Any) – Extra arguments are passed to option().

Return type:
Callable[[FC], FC]

click.version_option(version=None, *param_decls, package_name=None, prog_name=None, message=None, **kwargs)
Add a --version option which immediately prints the version number and exits the program.

If version is not provided, Click will try to detect it using importlib.metadata.version() to get the version for the package_name.

If package_name is not provided, Click will try to detect it by inspecting the stack frames. This will be used to detect the version, so it must match the name of the installed package.

Parameters:
version (str | None) – The version number to show. If not provided, Click will try to detect it.

param_decls (str) – One or more option names. Defaults to the single value "--version".

package_name (str | None) – The package name to detect the version from. If not provided, Click will try to detect it.

prog_name (str | None) – The name of the CLI to show in the message. If not provided, it will be detected from the command.

message (str | None) – The message to show. The values %(prog)s, %(package)s, and %(version)s are available. Defaults to "%(prog)s, version %(version)s".

kwargs (Any) – Extra arguments are passed to option().

Raises:
RuntimeError – version could not be detected.

Return type:
Callable[[FC], FC]

Changelog
click.help_option(*param_decls, **kwargs)
Pre-configured --help option which immediately prints the help page and exits the program.

Parameters:
param_decls (str) – One or more option names. Defaults to the single value "--help".

kwargs (Any) – Extra arguments are passed to option().

Return type:
Callable[[FC], FC]

click.pass_context(f)
Marks a callback as wanting to receive the current context object as first argument.

Parameters:
f (t.Callable[te.Concatenate[Context, P], R])

Return type:
t.Callable[P, R]

click.pass_obj(f)
Similar to pass_context(), but only pass the object on the context onwards (Context.obj). This is useful if that object represents the state of a nested system.

Parameters:
f (t.Callable[te.Concatenate[T, P], R])

Return type:
t.Callable[P, R]

click.make_pass_decorator(object_type, ensure=False)
Given an object type this creates a decorator that will work similar to pass_obj() but instead of passing the object of the current context, it will find the innermost context of type object_type().

This generates a decorator that works roughly like this:

from functools import update_wrapper

def decorator(f):
    @pass_context
    def new_func(ctx, *args, **kwargs):
        obj = ctx.find_object(object_type)
        return ctx.invoke(f, obj, *args, **kwargs)
    return update_wrapper(new_func, f)
return decorator
Parameters:
object_type (type[T]) – the type of the object to pass.

ensure (bool) – if set to True, a new object will be created and remembered on the context if it’s not there yet.

Return type:
t.Callable[[t.Callable[te.Concatenate[T, P], R]], t.Callable[P, R]]

click.decorators.pass_meta_key(key, *, doc_description=None)
Create a decorator that passes a key from click.Context.meta as the first argument to the decorated function.

Parameters:
key (str) – Key in Context.meta to pass.

doc_description (str | None) – Description of the object being passed, inserted into the decorator’s docstring. Defaults to “the ‘key’ key from Context.meta”.

Return type:
t.Callable[[t.Callable[te.Concatenate[T, P], R]], t.Callable[P, R]]

Changelog
Utilities
click.echo(message=None, file=None, nl=True, err=False, color=None)
Print a message and newline to stdout or a file. This should be used instead of print() because it provides better support for different data, files, and environments.

Compared to print(), this does the following:

Ensures that the output encoding is not misconfigured on Linux.

Supports Unicode in the Windows console.

Supports writing to binary outputs, and supports writing bytes to text outputs.

Supports colors and styles on Windows.

Removes ANSI color and style codes if the output does not look like an interactive terminal.

Always flushes the output.

Parameters:
message (Any | None) – The string or bytes to output. Other objects are converted to strings.

file (IO[Any] | None) – The file to write to. Defaults to stdout.

err (bool) – Write to stderr instead of stdout.

nl (bool) – Print a newline after the message. Enabled by default.

color (bool | None) – Force showing or hiding colors and other styles. By default Click will remove color if the output does not look like an interactive terminal.

Return type:
None

Changelog
click.echo_via_pager(text_or_generator, color=None)
This function takes a text and shows it via an environment specific pager on stdout.

Changelog
Parameters:
text_or_generator (Iterable[str] | Callable[[], Iterable[str]] | str) – the text to page, or alternatively, a generator emitting the text to page.

color (bool | None) – controls if the pager supports ANSI colors or not. The default is autodetection.

Return type:
None

click.prompt(text, default=None, hide_input=False, confirmation_prompt=False, type=None, value_proc=None, prompt_suffix=': ', show_default=True, err=False, show_choices=True)
Prompts a user for input. This is a convenience function that can be used to prompt a user for input later.

If the user aborts the input by sending an interrupt signal, this function will catch it and raise a Abort exception.

Parameters:
text (str) – the text to show for the prompt.

default (Any | None) – the default value to use if no input happens. If this is not given it will prompt until it’s aborted.

hide_input (bool) – if this is set to true then the input value will be hidden.

confirmation_prompt (bool | str) – Prompt a second time to confirm the value. Can be set to a string instead of True to customize the message.

type (ParamType | Any | None) – the type to use to check the value against.

value_proc (Callable[[str], Any] | None) – if this parameter is provided it’s a function that is invoked instead of the type conversion to convert a value.

prompt_suffix (str) – a suffix that should be added to the prompt.

show_default (bool) – shows or hides the default value in the prompt.

err (bool) – if set to true the file defaults to stderr instead of stdout, the same as with echo.

show_choices (bool) – Show or hide choices if the passed type is a Choice. For example if type is a Choice of either day or week, show_choices is true and text is “Group by” then the prompt will be “Group by (day, week): “.

Return type:
Any

Changed in version 8.3.1: A space is no longer appended to the prompt.

Changelog
click.confirm(text, default=False, abort=False, prompt_suffix=': ', show_default=True, err=False)
Prompts for confirmation (yes/no question).

If the user aborts the input by sending a interrupt signal this function will catch it and raise a Abort exception.

Parameters:
text (str) – the question to ask.

default (bool | None) – The default value to use when no input is given. If None, repeat until input is given.

abort (bool) – if this is set to True a negative answer aborts the exception by raising Abort.

prompt_suffix (str) – a suffix that should be added to the prompt.

show_default (bool) – shows or hides the default value in the prompt.

err (bool) – if set to true the file defaults to stderr instead of stdout, the same as with echo.

Return type:
bool

Changed in version 8.3.1: A space is no longer appended to the prompt.

Changelog
click.progressbar(*, length: int, label: str | None = None, hidden: bool = False, show_eta: bool = True, show_percent: bool | None = None, show_pos: bool = False, fill_char: str = '#', empty_char: str = '-', bar_template: str = '%(label)s  [%(bar)s]  %(info)s', info_sep: str = '  ', width: int = 36, file: TextIO | None = None, color: bool | None = None, update_min_steps: int = 1) → ProgressBar[int]
click.progressbar(iterable: Iterable[V] | None = None, length: int | None = None, label: str | None = None, hidden: bool = False, show_eta: bool = True, show_percent: bool | None = None, show_pos: bool = False, item_show_func: Callable[[V | None], str | None] | None = None, fill_char: str = '#', empty_char: str = '-', bar_template: str = '%(label)s  [%(bar)s]  %(info)s', info_sep: str = '  ', width: int = 36, file: TextIO | None = None, color: bool | None = None, update_min_steps: int = 1) → ProgressBar[V]
This function creates an iterable context manager that can be used to iterate over something while showing a progress bar. It will either iterate over the iterable or length items (that are counted up). While iteration happens, this function will print a rendered progress bar to the given file (defaults to stdout) and will attempt to calculate remaining time and more. By default, this progress bar will not be rendered if the file is not a terminal.

The context manager creates the progress bar. When the context manager is entered the progress bar is already created. With every iteration over the progress bar, the iterable passed to the bar is advanced and the bar is updated. When the context manager exits, a newline is printed and the progress bar is finalized on screen.

Note: The progress bar is currently designed for use cases where the total progress can be expected to take at least several seconds. Because of this, the ProgressBar class object won’t display progress that is considered too fast, and progress where the time between steps is less than a second.

No printing must happen or the progress bar will be unintentionally destroyed.

Example usage:

with progressbar(items) as bar:
    for item in bar:
        do_something_with(item)
Alternatively, if no iterable is specified, one can manually update the progress bar through the update() method instead of directly iterating over the progress bar. The update method accepts the number of steps to increment the bar with:

with progressbar(length=chunks.total_bytes) as bar:
    for chunk in chunks:
        process_chunk(chunk)
        bar.update(chunks.bytes)
The update() method also takes an optional value specifying the current_item at the new position. This is useful when used together with item_show_func to customize the output for each manual step:

with click.progressbar(
    length=total_size,
    label='Unzipping archive',
    item_show_func=lambda a: a.filename
) as bar:
    for archive in zip_file:
        archive.extract()
        bar.update(archive.size, archive)
Parameters:
iterable – an iterable to iterate over. If not provided the length is required.

length – the number of items to iterate over. By default the progressbar will attempt to ask the iterator about its length, which might or might not work. If an iterable is also provided this parameter can be used to override the length. If an iterable is not provided the progress bar will iterate over a range of that length.

label – the label to show next to the progress bar.

hidden – hide the progressbar. Defaults to False. When no tty is detected, it will only print the progressbar label. Setting this to False also disables that.

show_eta – enables or disables the estimated time display. This is automatically disabled if the length cannot be determined.

show_percent – enables or disables the percentage display. The default is True if the iterable has a length or False if not.

show_pos – enables or disables the absolute position display. The default is False.

item_show_func – A function called with the current item which can return a string to show next to the progress bar. If the function returns None nothing is shown. The current item can be None, such as when entering and exiting the bar.

fill_char – the character to use to show the filled part of the progress bar.

empty_char – the character to use to show the non-filled part of the progress bar.

bar_template – the format string to use as template for the bar. The parameters in it are label for the label, bar for the progress bar and info for the info section.

info_sep – the separator between multiple info items (eta etc.)

width – the width of the progress bar in characters, 0 means full terminal width

file – The file to write to. If this is not a terminal then only the label is printed.

color – controls if the terminal supports ANSI colors or not. The default is autodetection. This is only needed if ANSI codes are included anywhere in the progress bar output which is not the case by default.

update_min_steps – Render only when this many updates have completed. This allows tuning for very fast iterators.

Changelog
click.clear()
Clears the terminal screen. This will have the effect of clearing the whole visible space of the terminal and moving the cursor to the top left. This does not do anything if not connected to a terminal.

Changelog
Return type:
None

click.style(text, fg=None, bg=None, bold=None, dim=None, underline=None, overline=None, italic=None, blink=None, reverse=None, strikethrough=None, reset=True)
Styles a text with ANSI styles and returns the new string. By default the styling is self contained which means that at the end of the string a reset code is issued. This can be prevented by passing reset=False.

Examples:

click.echo(click.style('Hello World!', fg='green'))
click.echo(click.style('ATTENTION!', blink=True))
click.echo(click.style('Some things', reverse=True, fg='cyan'))
click.echo(click.style('More colors', fg=(255, 12, 128), bg=117))
Supported color names:

black (might be a gray)

red

green

yellow (might be an orange)

blue

magenta

cyan

white (might be light gray)

bright_black

bright_red

bright_green

bright_yellow

bright_blue

bright_magenta

bright_cyan

bright_white

reset (reset the color code only)

If the terminal supports it, color may also be specified as:

An integer in the interval [0, 255]. The terminal must support 8-bit/256-color mode.

An RGB tuple of three integers in [0, 255]. The terminal must support 24-bit/true-color mode.

See https://en.wikipedia.org/wiki/ANSI_color and https://gist.github.com/XVilka/8346728 for more information.

Parameters:
text (Any) – the string to style with ansi codes.

fg (int | tuple[int, int, int] | str | None) – if provided this will become the foreground color.

bg (int | tuple[int, int, int] | str | None) – if provided this will become the background color.

bold (bool | None) – if provided this will enable or disable bold mode.

dim (bool | None) – if provided this will enable or disable dim mode. This is badly supported.

underline (bool | None) – if provided this will enable or disable underline.

overline (bool | None) – if provided this will enable or disable overline.

italic (bool | None) – if provided this will enable or disable italic.

blink (bool | None) – if provided this will enable or disable blinking.

reverse (bool | None) – if provided this will enable or disable inverse rendering (foreground becomes background and the other way round).

strikethrough (bool | None) – if provided this will enable or disable striking through text.

reset (bool) – by default a reset-all code is added at the end of the string which means that styles do not carry over. This can be disabled to compose styles.

Return type:
str

Changelog
click.unstyle(text)
Removes ANSI styling information from a string. Usually it’s not necessary to use this function as Click’s echo function will automatically remove styling if necessary.

Changelog
Parameters:
text (str) – the text to remove style information from.

Return type:
str

click.secho(message=None, file=None, nl=True, err=False, color=None, **styles)
This function combines echo() and style() into one call. As such the following two calls are the same:

click.secho('Hello World!', fg='green')
click.echo(click.style('Hello World!', fg='green'))
All keyword arguments are forwarded to the underlying functions depending on which one they go with.

Non-string types will be converted to str. However, bytes are passed directly to echo() without applying style. If you want to style bytes that represent text, call bytes.decode() first.

Changelog
Parameters:
message (Any | None)

file (IO | None)

nl (bool)

err (bool)

color (bool | None)

styles (Any)

Return type:
None

click.edit(text: bytes | bytearray, editor: str | None = None, env: Mapping[str, str] | None = None, require_save: bool = False, extension: str = '.txt') → bytes | None
click.edit(text: str, editor: str | None = None, env: Mapping[str, str] | None = None, require_save: bool = True, extension: str = '.txt') → str | None
click.edit(text: None = None, editor: str | None = None, env: Mapping[str, str] | None = None, require_save: bool = True, extension: str = '.txt', filename: str | Iterable[str] | None = None) → None
Edits the given text in the defined editor. If an editor is given (should be the full path to the executable but the regular operating system search path is used for finding the executable) it overrides the detected editor. Optionally, some environment variables can be used. If the editor is closed without changes, None is returned. In case a file is edited directly the return value is always None and require_save and extension are ignored.

If the editor cannot be opened a UsageError is raised.

Note for Windows: to simplify cross-platform usage, the newlines are automatically converted from POSIX to Windows and vice versa. As such, the message here will have \n as newline markers.

Parameters:
text – the text to edit.

editor – optionally the editor to use. Defaults to automatic detection.

env – environment variables to forward to the editor.

require_save – if this is true, then not saving in the editor will make the return value become None.

extension – the extension to tell the editor about. This defaults to .txt but changing this might change syntax highlighting.

filename – if provided it will edit this file instead of the provided text contents. It will not use a temporary file as an indirection in that case. If the editor supports editing multiple files at once, a sequence of files may be passed as well. Invoke click.file once per file instead if multiple files cannot be managed at once or editing the files serially is desired.

Changelog
click.launch(url, wait=False, locate=False)
This function launches the given URL (or filename) in the default viewer application for this file type. If this is an executable, it might launch the executable in a new session. The return value is the exit code of the launched application. Usually, 0 indicates success.

Examples:

click.launch('https://click.palletsprojects.com/')
click.launch('/my/downloaded/file', locate=True)
Changelog
Parameters:
url (str) – URL or filename of the thing to launch.

wait (bool) – Wait for the program to exit before returning. This only works if the launched program blocks. In particular, xdg-open on Linux does not block.

locate (bool) – if this is set to True then instead of launching the application associated with the URL it will attempt to launch a file manager with the file located. This might have weird effects if the URL does not point to the filesystem.

Return type:
int

click.getchar(echo=False)
Fetches a single character from the terminal and returns it. This will always return a unicode character and under certain rare circumstances this might return more than one character. The situations which more than one character is returned is when for whatever reason multiple characters end up in the terminal buffer or standard input was not actually a terminal.

Note that this will always read from the terminal, even if something is piped into the standard input.

Note for Windows: in rare cases when typing non-ASCII characters, this function might wait for a second character and then return both at once. This is because certain Unicode characters look like special-key markers.

Changelog
Parameters:
echo (bool) – if set to True, the character read will also show up on the terminal. The default is to not show it.

Return type:
str

click.pause(info=None, err=False)
This command stops execution and waits for the user to press any key to continue. This is similar to the Windows batch “pause” command. If the program is not run through a terminal, this command will instead do nothing.

Changelog
Parameters:
info (str | None) – The message to print before pausing. Defaults to "Press any key to continue...".

err (bool) – if set to message goes to stderr instead of stdout, the same as with echo.

Return type:
None

click.get_binary_stream(name)
Returns a system stream for byte processing.

Parameters:
name (Literal['stdin', 'stdout', 'stderr']) – the name of the stream to open. Valid names are 'stdin', 'stdout' and 'stderr'

Return type:
BinaryIO

click.get_text_stream(name, encoding=None, errors='strict')
Returns a system stream for text processing. This usually returns a wrapped stream around a binary stream returned from get_binary_stream() but it also can take shortcuts for already correctly configured streams.

Parameters:
name (Literal['stdin', 'stdout', 'stderr']) – the name of the stream to open. Valid names are 'stdin', 'stdout' and 'stderr'

encoding (str | None) – overrides the detected default encoding.

errors (str | None) – overrides the default error mode.

Return type:
TextIO

click.open_file(filename, mode='r', encoding=None, errors='strict', lazy=False, atomic=False)
Open a file, with extra behavior to handle '-' to indicate a standard stream, lazy open on write, and atomic write. Similar to the behavior of the File param type.

If '-' is given to open stdout or stdin, the stream is wrapped so that using it in a context manager will not close it. This makes it possible to use the function without accidentally closing a standard stream:

with open_file(filename) as f:
    ...
Parameters:
filename (str | PathLike[str]) – The name or Path of the file to open, or '-' for stdin/stdout.

mode (str) – The mode in which to open the file.

encoding (str | None) – The encoding to decode or encode a file opened in text mode.

errors (str | None) – The error handling mode.

lazy (bool) – Wait to open the file until it is accessed. For read mode, the file is temporarily opened to raise access errors early, then closed until it is read again.

atomic (bool) – Write to a temporary file and replace the given file on close.

Return type:
IO[Any]

Changelog
click.get_app_dir(app_name, roaming=True, force_posix=False)
Returns the config folder for the application. The default behavior is to return whatever is most appropriate for the operating system.

To give you an idea, for an app called "Foo Bar", something like the following folders could be returned:

Mac OS X:
~/Library/Application Support/Foo Bar

Mac OS X (POSIX):
~/.foo-bar

Unix:
~/.config/foo-bar

Unix (POSIX):
~/.foo-bar

Windows (roaming):
C:\Users\<user>\AppData\Roaming\Foo Bar

Windows (not roaming):
C:\Users\<user>\AppData\Local\Foo Bar

Changelog
Parameters:
app_name (str) – the application name. This should be properly capitalized and can contain whitespace.

roaming (bool) – controls if the folder should be roaming or not on Windows. Has no effect otherwise.

force_posix (bool) – if this is set to True then on any POSIX system the folder will be stored in the home folder with a leading dot instead of the XDG config home or darwin’s application support folder.

Return type:
str

click.format_filename(filename, shorten=False)
Format a filename as a string for display. Ensures the filename can be displayed by replacing any invalid bytes or surrogate escapes in the name with the replacement character �.

Invalid bytes or surrogate escapes will raise an error when written to a stream with errors="strict". This will typically happen with stdout when the locale is something like en_GB.UTF-8.

Many scenarios are safe to write surrogates though, due to PEP 538 and PEP 540, including:

Writing to stderr, which uses errors="backslashreplace".

The system has LANG=C.UTF-8, C, or POSIX. Python opens stdout and stderr with errors="surrogateescape".

None of LANG/LC_* are set. Python assumes LANG=C.UTF-8.

Python is started in UTF-8 mode with PYTHONUTF8=1 or -X utf8. Python opens stdout and stderr with errors="surrogateescape".

Parameters:
filename (str | bytes | PathLike[str] | PathLike[bytes]) – formats a filename for UI display. This will also convert the filename into unicode without failing.

shorten (bool) – this optionally shortens the filename to strip of the path that leads up to it.

Return type:
str

Commands
click.BaseCommand
alias of _BaseCommand

class click.Command(name, context_settings=None, callback=None, params=None, help=None, epilog=None, short_help=None, options_metavar='[OPTIONS]', add_help_option=True, no_args_is_help=False, hidden=False, deprecated=False)
Commands are the basic building block of command line interfaces in Click. A basic command handles command line parsing and might dispatch more parsing to commands nested below it.

Parameters:
name (str | None) – the name of the command to use unless a group overrides it.

context_settings (cabc.MutableMapping[str, t.Any] | None) – an optional dictionary with defaults that are passed to the context object.

callback (t.Callable[..., t.Any] | None) – the callback to invoke. This is optional.

params (list[Parameter] | None) – the parameters to register with this command. This can be either Option or Argument objects.

help (str | None) – the help string to use for this command.

epilog (str | None) – like the help string but it’s printed at the end of the help page after everything else.

short_help (str | None) – the short help to use for this command. This is shown on the command listing of the parent command.

add_help_option (bool) – by default each command registers a --help option. This can be disabled by this parameter.

no_args_is_help (bool) – this controls what happens if no arguments are provided. This option is disabled by default. If enabled this will add --help as argument if no arguments are passed

hidden (bool) – hide this command from help outputs.

deprecated (bool | str) – If True or non-empty string, issues a message indicating that the command is deprecated and highlights its deprecation in –help. The message can be customized by using a string as the value.

options_metavar (str | None)

Changelog
context_class
alias of Context

allow_extra_args = False
the default for the Context.allow_extra_args flag.

allow_interspersed_args = True
the default for the Context.allow_interspersed_args flag.

ignore_unknown_options = False
the default for the Context.ignore_unknown_options flag.

name
the name the command thinks it has. Upon registering a command on a Group the group will default the command name with this information. You should instead use the Context's info_name attribute.

context_settings: MutableMapping[str, Any]
an optional dictionary with defaults passed to the context.

callback
the callback to execute when the command fires. This might be None in which case nothing happens.

params: list[Parameter]
the list of parameters for this command in the order they should show up in the help page and execute. Eager parameters will automatically be handled before non eager ones.

get_usage(ctx)
Formats the usage line into a string and returns it.

Calls format_usage() internally.

Parameters:
ctx (Context)

Return type:
str

format_usage(ctx, formatter)
Writes the usage line into the formatter.

This is a low-level method called by get_usage().

Parameters:
ctx (Context)

formatter (HelpFormatter)

Return type:
None

collect_usage_pieces(ctx)
Returns all the pieces that go into the usage line and returns it as a list of strings.

Parameters:
ctx (Context)

Return type:
list[str]

get_help_option_names(ctx)
Returns the names for the help option.

Parameters:
ctx (Context)

Return type:
list[str]

get_help_option(ctx)
Returns the help option object.

Skipped if add_help_option is False.

Changelog
Parameters:
ctx (Context)

Return type:
Option | None

make_parser(ctx)
Creates the underlying option parser for this command.

Parameters:
ctx (Context)

Return type:
_OptionParser

get_help(ctx)
Formats the help into a string and returns it.

Calls format_help() internally.

Parameters:
ctx (Context)

Return type:
str

get_short_help_str(limit=45)
Gets short help for the command or makes it by shortening the long help string.

Parameters:
limit (int)

Return type:
str

format_help(ctx, formatter)
Writes the help into the formatter if it exists.

This is a low-level method called by get_help().

This calls the following methods:

format_usage()

format_help_text()

format_options()

format_epilog()

Parameters:
ctx (Context)

formatter (HelpFormatter)

Return type:
None

format_help_text(ctx, formatter)
Writes the help text to the formatter if it exists.

Parameters:
ctx (Context)

formatter (HelpFormatter)

Return type:
None

format_options(ctx, formatter)
Writes all the options into the formatter if they exist.

Parameters:
ctx (Context)

formatter (HelpFormatter)

Return type:
None

format_epilog(ctx, formatter)
Writes the epilog into the formatter if it exists.

Parameters:
ctx (Context)

formatter (HelpFormatter)

Return type:
None

make_context(info_name, args, parent=None, **extra)
This function when given an info name and arguments will kick off the parsing and create a new Context. It does not invoke the actual command callback though.

To quickly customize the context class used without overriding this method, set the context_class attribute.

Parameters:
info_name (str | None) – the info name for this invocation. Generally this is the most descriptive name for the script or command. For the toplevel script it’s usually the name of the script, for commands below it’s the name of the command.

args (list[str]) – the arguments to parse as list of strings.

parent (Context | None) – the parent context if available.

extra (Any) – extra keyword arguments forwarded to the context constructor.

Return type:
Context

Changelog
invoke(ctx)
Given a context, this invokes the attached callback (if it exists) in the right way.

Parameters:
ctx (Context)

Return type:
Any

shell_complete(ctx, incomplete)
Return a list of completions for the incomplete value. Looks at the names of options and chained multi-commands.

Any command could be part of a chained multi-command, so sibling commands are valid at any point during command completion.

Parameters:
ctx (Context) – Invocation context for this command.

incomplete (str) – Value being completed. May be empty.

Return type:
list[CompletionItem]

Changelog
main(args: Sequence[str] | None = None, prog_name: str | None = None, complete_var: str | None = None, standalone_mode: Literal[True] = True, **extra: Any) → NoReturn
main(args: Sequence[str] | None = None, prog_name: str | None = None, complete_var: str | None = None, standalone_mode: bool = True, **extra: Any) → Any
This is the way to invoke a script with all the bells and whistles as a command line application. This will always terminate the application after a call. If this is not wanted, SystemExit needs to be caught.

This method is also available by directly calling the instance of a Command.

Parameters:
args – the arguments that should be used for parsing. If not provided, sys.argv[1:] is used.

prog_name – the program name that should be used. By default the program name is constructed by taking the file name from sys.argv[0].

complete_var – the environment variable that controls the bash completion support. The default is "_<prog_name>_COMPLETE" with prog_name in uppercase.

standalone_mode – the default behavior is to invoke the script in standalone mode. Click will then handle exceptions and convert them into error messages and the function will never return but shut down the interpreter. If this is set to False they will be propagated to the caller and the return value of this function is the return value of invoke().

windows_expand_args – Expand glob patterns, user dir, and env vars in command line args on Windows.

extra – extra keyword arguments are forwarded to the context constructor. See Context for more information.

Changelog
click.MultiCommand
alias of _MultiCommand

class click.Group(name=None, commands=None, invoke_without_command=False, no_args_is_help=None, subcommand_metavar=None, chain=False, result_callback=None, **kwargs)
A group is a command that nests other commands (or more groups).

Parameters:
name (str | None) – The name of the group command.

commands (cabc.MutableMapping[str, Command] | cabc.Sequence[Command] | None) – Map names to Command objects. Can be a list, which will use Command.name as the keys.

invoke_without_command (bool) – Invoke the group’s callback even if a subcommand is not given.

no_args_is_help (bool | None) – If no arguments are given, show the group’s help and exit. Defaults to the opposite of invoke_without_command.

subcommand_metavar (str | None) – How to represent the subcommand argument in help. The default will represent whether chain is set or not.

chain (bool) – Allow passing more than one subcommand argument. After parsing a command’s arguments, if any arguments remain another command will be matched, and so on.

result_callback (t.Callable[..., t.Any] | None) – A function to call after the group’s and subcommand’s callbacks. The value returned by the subcommand is passed. If chain is enabled, the value will be a list of values returned by all the commands. If invoke_without_command is enabled, the value will be the value returned by the group’s callback, or an empty list if chain is enabled.

kwargs (t.Any) – Other arguments passed to Command.

Changelog
allow_extra_args = True
the default for the Context.allow_extra_args flag.

allow_interspersed_args = False
the default for the Context.allow_interspersed_args flag.

command_class: type[Command] | None = None
If set, this is used by the group’s command() decorator as the default Command class. This is useful to make all subcommands use a custom command class.

Changelog
group_class: type[Group] | type[type] | None = None
If set, this is used by the group’s group() decorator as the default Group class. This is useful to make all subgroups use a custom group class.

If set to the special value type (literally group_class = type), this group’s class will be used as the default class. This makes a custom group class continue to make custom groups.

Changelog
commands: MutableMapping[str, Command]
The registered subcommands by their exported names.

add_command(cmd, name=None)
Registers another Command with this group. If the name is not provided, the name of the command is used.

Parameters:
cmd (Command)

name (str | None)

Return type:
None

command(__func: Callable[[...], Any]) → Command
command(*args: Any, **kwargs: Any) → Callable[[Callable[[...], Any]], Command]
A shortcut decorator for declaring and attaching a command to the group. This takes the same arguments as command() and immediately registers the created command with this group by calling add_command().

To customize the command class used, set the command_class attribute.

Changelog
group(__func: Callable[[...], Any]) → Group
group(*args: Any, **kwargs: Any) → Callable[[Callable[[...], Any]], Group]
A shortcut decorator for declaring and attaching a group to the group. This takes the same arguments as group() and immediately registers the created group with this group by calling add_command().

To customize the group class used, set the group_class attribute.

Changelog
result_callback(replace=False)
Adds a result callback to the command. By default if a result callback is already registered this will chain them but this can be disabled with the replace parameter. The result callback is invoked with the return value of the subcommand (or the list of return values from all subcommands if chaining is enabled) as well as the parameters as they would be passed to the main callback.

Example:

@click.group()
@click.option('-i', '--input', default=23)
def cli(input):
    return 42

@cli.result_callback()
def process_result(result, input):
    return result + input
Parameters:
replace (bool) – if set to True an already existing result callback will be removed.

Return type:
Callable[[F], F]

Changelog
get_command(ctx, cmd_name)
Given a context and a command name, this returns a Command object if it exists or returns None.

Parameters:
ctx (Context)

cmd_name (str)

Return type:
Command | None

list_commands(ctx)
Returns a list of subcommand names in the order they should appear.

Parameters:
ctx (Context)

Return type:
list[str]

collect_usage_pieces(ctx)
Returns all the pieces that go into the usage line and returns it as a list of strings.

Parameters:
ctx (Context)

Return type:
list[str]

format_options(ctx, formatter)
Writes all the options into the formatter if they exist.

Parameters:
ctx (Context)

formatter (HelpFormatter)

Return type:
None

format_commands(ctx, formatter)
Extra format methods for multi methods that adds all the commands after the options.

Parameters:
ctx (Context)

formatter (HelpFormatter)

Return type:
None

invoke(ctx)
Given a context, this invokes the attached callback (if it exists) in the right way.

Parameters:
ctx (Context)

Return type:
Any

shell_complete(ctx, incomplete)
Return a list of completions for the incomplete value. Looks at the names of options, subcommands, and chained multi-commands.

Parameters:
ctx (Context) – Invocation context for this command.

incomplete (str) – Value being completed. May be empty.

Return type:
list[CompletionItem]

Changelog
class click.CommandCollection(name=None, sources=None, **kwargs)
A Group that looks up subcommands on other groups. If a command is not found on this group, each registered source is checked in order. Parameters on a source are not added to this group, and a source’s callback is not invoked when invoking its commands. In other words, this “flattens” commands in many groups into this one group.

Parameters:
name (str | None) – The name of the group command.

sources (list[Group] | None) – A list of Group objects to look up commands from.

kwargs (t.Any) – Other arguments passed to Group.

Changelog
sources: list[Group]
The list of registered groups.

add_source(group)
Add a group as a source of commands.

Parameters:
group (Group)

Return type:
None

get_command(ctx, cmd_name)
Given a context and a command name, this returns a Command object if it exists or returns None.

Parameters:
ctx (Context)

cmd_name (str)

Return type:
Command | None

list_commands(ctx)
Returns a list of subcommand names in the order they should appear.

Parameters:
ctx (Context)

Return type:
list[str]

Parameters
class click.Parameter(param_decls=None, type=None, required=False, default=UNSET, callback=None, nargs=None, multiple=False, metavar=None, expose_value=True, is_eager=False, envvar=None, shell_complete=None, deprecated=False)
A parameter to a command comes in two versions: they are either Options or Arguments. Other subclasses are currently not supported by design as some of the internals for parsing are intentionally not finalized.

Some settings are supported by both options and arguments.

Parameters:
param_decls (cabc.Sequence[str] | None) – the parameter declarations for this option or argument. This is a list of flags or argument names.

type (types.ParamType | t.Any | None) – the type that should be used. Either a ParamType or a Python type. The latter is converted into the former automatically if supported.

required (bool) – controls if this is optional or not.

default (t.Any | t.Callable[[], t.Any] | None) – the default value if omitted. This can also be a callable, in which case it’s invoked when the default is needed without any arguments.

callback (t.Callable[[Context, Parameter, t.Any], t.Any] | None) – A function to further process or validate the value after type conversion. It is called as f(ctx, param, value) and must return the value. It is called for all sources, including prompts.

nargs (int | None) – the number of arguments to match. If not 1 the return value is a tuple instead of single value. The default for nargs is 1 (except if the type is a tuple, then it’s the arity of the tuple). If nargs=-1, all remaining parameters are collected.

metavar (str | None) – how the value is represented in the help page.

expose_value (bool) – if this is True then the value is passed onwards to the command callback and stored on the context, otherwise it’s skipped.

is_eager (bool) – eager values are processed before non eager ones. This should not be set for arguments or it will inverse the order of processing.

envvar (str | cabc.Sequence[str] | None) – environment variable(s) that are used to provide a default value for this parameter. This can be a string or a sequence of strings. If a sequence is given, only the first non-empty environment variable is used for the parameter.

shell_complete (t.Callable[[Context, Parameter, str], list[CompletionItem] | list[str]] | None) – A function that returns custom shell completions. Used instead of the param’s type completion if given. Takes ctx, param, incomplete and must return a list of CompletionItem or a list of strings.

deprecated (bool | str) – If True or non-empty string, issues a message indicating that the argument is deprecated and highlights its deprecation in –help. The message can be customized by using a string as the value. A deprecated parameter cannot be required, a ValueError will be raised otherwise.

multiple (bool)

Changelog
to_info_dict()
Gather information that could be useful for a tool generating user-facing documentation.

Use click.Context.to_info_dict() to traverse the entire CLI structure.

Changed in version 8.3.0: Returns None for the default if it was not set.

Changelog
Return type:
dict[str, Any]

property human_readable_name: str
Returns the human readable name of this parameter. This is the same as the name for options, but the metavar for arguments.

get_default(ctx: Context, call: Literal[True] = True) → Any | None
get_default(ctx: Context, call: bool = True) → Any | Callable[[], Any] | None
Get the default for the parameter. Tries Context.lookup_default() first, then the local default.

Parameters:
ctx – Current context.

call – If the default is a callable, call it. Disable to return the callable instead.

Changelog
type_cast_value(ctx, value)
Convert and validate a value against the parameter’s type, multiple, and nargs.

Parameters:
ctx (Context)

value (Any)

Return type:
Any

get_error_hint(ctx)
Get a stringified version of the param for use in error messages to indicate which param caused the error.

Parameters:
ctx (Context)

Return type:
str

shell_complete(ctx, incomplete)
Return a list of completions for the incomplete value. If a shell_complete function was given during init, it is used. Otherwise, the type shell_complete() function is used.

Parameters:
ctx (Context) – Invocation context for this command.

incomplete (str) – Value being completed. May be empty.

Return type:
list[CompletionItem]

Changelog
class click.Option(param_decls=None, show_default=None, prompt=False, confirmation_prompt=False, prompt_required=True, hide_input=False, is_flag=None, flag_value=UNSET, multiple=False, count=False, allow_from_autoenv=True, type=None, help=None, hidden=False, show_choices=True, show_envvar=False, deprecated=False, **attrs)
Options are usually optional values on the command line and have some extra features that arguments don’t have.

All other parameters are passed onwards to the parameter constructor.

Parameters:
show_default (bool | str | None) – Show the default value for this option in its help text. Values are not shown by default, unless Context.show_default is True. If this value is a string, it shows that string in parentheses instead of the actual value. This is particularly useful for dynamic options. For single option boolean flags, the default remains hidden if its value is False.

show_envvar (bool) – Controls if an environment variable should be shown on the help page and error messages. Normally, environment variables are not shown.

prompt (bool | str) – If set to True or a non empty string then the user will be prompted for input. If set to True the prompt will be the option name capitalized. A deprecated option cannot be prompted.

confirmation_prompt (bool | str) – Prompt a second time to confirm the value if it was prompted for. Can be set to a string instead of True to customize the message.

prompt_required (bool) – If set to False, the user will be prompted for input only when the option was specified as a flag without a value.

hide_input (bool) – If this is True then the input on the prompt will be hidden from the user. This is useful for password input.

is_flag (bool | None) – forces this option to act as a flag. The default is auto detection.

flag_value (t.Any) – which value should be used for this flag if it’s enabled. This is set to a boolean automatically if the option string contains a slash to mark two options.

multiple (bool) – if this is set to True then the argument is accepted multiple times and recorded. This is similar to nargs in how it works but supports arbitrary number of arguments.

count (bool) – this flag makes an option increment an integer.

allow_from_autoenv (bool) – if this is enabled then the value of this parameter will be pulled from an environment variable in case a prefix is defined on the context.

help (str | None) – the help string.

hidden (bool) – hide this option from help outputs.

attrs (t.Any) – Other command arguments described in Parameter.

param_decls (cabc.Sequence[str] | None)

type (types.ParamType | t.Any | None)

show_choices (bool)

deprecated (bool | str)

Changelog
class click.Argument(param_decls, required=None, **attrs)
Arguments are positional parameters to a command. They generally provide fewer features than options but can have infinite nargs and are required by default.

All parameters are passed onwards to the constructor of Parameter.

Parameters:
param_decls (cabc.Sequence[str])

required (bool | None)

attrs (t.Any)

Context
class click.Context(command, parent=None, info_name=None, obj=None, auto_envvar_prefix=None, default_map=None, terminal_width=None, max_content_width=None, resilient_parsing=False, allow_extra_args=None, allow_interspersed_args=None, ignore_unknown_options=None, help_option_names=None, token_normalize_func=None, color=None, show_default=None)
The context is a special internal object that holds state relevant for the script execution at every single level. It’s normally invisible to commands unless they opt-in to getting access to it.

The context is useful as it can pass internal objects around and can control special execution features such as reading data from environment variables.

A context can be used as context manager in which case it will call close() on teardown.

Parameters:
command (Command) – the command class for this context.

parent (Context | None) – the parent context.

info_name (str | None) – the info name for this invocation. Generally this is the most descriptive name for the script or command. For the toplevel script it is usually the name of the script, for commands below it it’s the name of the script.

obj (t.Any | None) – an arbitrary object of user data.

auto_envvar_prefix (str | None) – the prefix to use for automatic environment variables. If this is None then reading from environment variables is disabled. This does not affect manually set environment variables which are always read.

default_map (cabc.MutableMapping[str, t.Any] | None) – a dictionary (like object) with default values for parameters.

terminal_width (int | None) – the width of the terminal. The default is inherit from parent context. If no context defines the terminal width then auto detection will be applied.

max_content_width (int | None) – the maximum width for content rendered by Click (this currently only affects help pages). This defaults to 80 characters if not overridden. In other words: even if the terminal is larger than that, Click will not format things wider than 80 characters by default. In addition to that, formatters might add some safety mapping on the right.

resilient_parsing (bool) – if this flag is enabled then Click will parse without any interactivity or callback invocation. Default values will also be ignored. This is useful for implementing things such as completion support.

allow_extra_args (bool | None) – if this is set to True then extra arguments at the end will not raise an error and will be kept on the context. The default is to inherit from the command.

allow_interspersed_args (bool | None) – if this is set to False then options and arguments cannot be mixed. The default is to inherit from the command.

ignore_unknown_options (bool | None) – instructs click to ignore options it does not know and keeps them for later processing.

help_option_names (list[str] | None) – optionally a list of strings that define how the default help parameter is named. The default is ['--help'].

token_normalize_func (t.Callable[[str], str] | None) – an optional function that is used to normalize tokens (options, choices, etc.). This for instance can be used to implement case insensitive behavior.

color (bool | None) – controls if the terminal supports ANSI colors or not. The default is autodetection. This is only needed if ANSI codes are used in texts that Click prints which is by default not the case. This for instance would affect help output.

show_default (bool | None) – Show the default value for commands. If this value is not set, it defaults to the value from the parent context. Command.show_default overrides this default for the specific command.

Changelog
formatter_class
alias of HelpFormatter

parent
the parent context or None if none exists.

command
the Command for this context.

info_name
the descriptive information name

params: dict[str, Any]
Map of parameter names to their parsed values. Parameters with expose_value=False are not stored.

args: list[str]
the leftover arguments.

obj: Any
the user object stored.

invoked_subcommand: str | None
This flag indicates if a subcommand is going to be executed. A group callback can use this information to figure out if it’s being executed directly or because the execution flow passes onwards to a subcommand. By default it’s None, but it can be the name of the subcommand to execute.

If chaining is enabled this will be set to '*' in case any commands are executed. It is however not possible to figure out which ones. If you require this knowledge you should use a result_callback().

terminal_width: int | None
The width of the terminal (None is autodetection).

max_content_width: int | None
The maximum width of formatted content (None implies a sensible default which is 80 for most things).

allow_extra_args
Indicates if the context allows extra args or if it should fail on parsing.

Changelog
allow_interspersed_args: bool
Indicates if the context allows mixing of arguments and options or not.

Changelog
ignore_unknown_options: bool
Instructs click to ignore options that a command does not understand and will store it on the context for later processing. This is primarily useful for situations where you want to call into external programs. Generally this pattern is strongly discouraged because it’s not possibly to losslessly forward all arguments.

Changelog
help_option_names: list[str]
The names for the help options.

token_normalize_func: Callable[[str], str] | None
An optional normalization function for tokens. This is options, choices, commands etc.

resilient_parsing: bool
Indicates if resilient parsing is enabled. In that case Click will do its best to not cause any failures and default values will be ignored. Useful for completion.

color: bool | None
Controls if styling output is wanted or not.

show_default: bool | None
Show option default values when formatting help text.

to_info_dict()
Gather information that could be useful for a tool generating user-facing documentation. This traverses the entire CLI structure.

with Context(cli) as ctx:
    info = ctx.to_info_dict()
Changelog
Return type:
dict[str, Any]

scope(cleanup=True)
This helper method can be used with the context object to promote it to the current thread local (see get_current_context()). The default behavior of this is to invoke the cleanup functions which can be disabled by setting cleanup to False. The cleanup functions are typically used for things such as closing file handles.

If the cleanup is intended the context object can also be directly used as a context manager.

Example usage:

with ctx.scope():
    assert get_current_context() is ctx
This is equivalent:

with ctx:
    assert get_current_context() is ctx
Changelog
Parameters:
cleanup (bool) – controls if the cleanup functions should be run or not. The default is to run these functions. In some situations the context only wants to be temporarily pushed in which case this can be disabled. Nested pushes automatically defer the cleanup.

Return type:
Iterator[Context]

property meta: dict[str, Any]
This is a dictionary which is shared with all the contexts that are nested. It exists so that click utilities can store some state here if they need to. It is however the responsibility of that code to manage this dictionary well.

The keys are supposed to be unique dotted strings. For instance module paths are a good choice for it. What is stored in there is irrelevant for the operation of click. However what is important is that code that places data here adheres to the general semantics of the system.

Example usage:

LANG_KEY = f'{__name__}.lang'

def set_language(value):
    ctx = get_current_context()
    ctx.meta[LANG_KEY] = value

def get_language():
    return get_current_context().meta.get(LANG_KEY, 'en_US')
Changelog
make_formatter()
Creates the HelpFormatter for the help and usage output.

To quickly customize the formatter class used without overriding this method, set the formatter_class attribute.

Changelog
Return type:
HelpFormatter

with_resource(context_manager)
Register a resource as if it were used in a with statement. The resource will be cleaned up when the context is popped.

Uses contextlib.ExitStack.enter_context(). It calls the resource’s __enter__() method and returns the result. When the context is popped, it closes the stack, which calls the resource’s __exit__() method.

To register a cleanup function for something that isn’t a context manager, use call_on_close(). Or use something from contextlib to turn it into a context manager first.

@click.group()
@click.option("--name")
@click.pass_context
def cli(ctx):
    ctx.obj = ctx.with_resource(connect_db(name))
Parameters:
context_manager (AbstractContextManager[V]) – The context manager to enter.

Returns:
Whatever context_manager.__enter__() returns.

Return type:
V

Changelog
call_on_close(f)
Register a function to be called when the context tears down.

This can be used to close resources opened during the script execution. Resources that support Python’s context manager protocol which would be used in a with statement should be registered with with_resource() instead.

Parameters:
f (Callable[[...], Any]) – The function to execute on teardown.

Return type:
Callable[[…], Any]

close()
Invoke all close callbacks registered with call_on_close(), and exit all context managers entered with with_resource().

Return type:
None

property command_path: str
The computed command path. This is used for the usage information on the help page. It’s automatically created by combining the info names of the chain of contexts to the root.

find_root()
Finds the outermost context.

Return type:
Context

find_object(object_type)
Finds the closest object of a given type.

Parameters:
object_type (type[V])

Return type:
V | None

ensure_object(object_type)
Like find_object() but sets the innermost object to a new instance of object_type if it does not exist.

Parameters:
object_type (type[V])

Return type:
V

lookup_default(name: str, call: Literal[True] = True) → Any | None
lookup_default(name: str, call: Literal[False] = True) → Any | Callable[[], Any] | None
Get the default for a parameter from default_map.

Parameters:
name – Name of the parameter.

call – If the default is a callable, call it. Disable to return the callable instead.

Changelog
fail(message)
Aborts the execution of the program with a specific error message.

Parameters:
message (str) – the error message to fail with.

Return type:
NoReturn

abort()
Aborts the script.

Return type:
NoReturn

exit(code=0)
Exits the application with a given exit code.

Changelog
Parameters:
code (int)

Return type:
NoReturn

get_usage()
Helper method to get formatted usage string for the current context and command.

Return type:
str

get_help()
Helper method to get formatted help page for the current context and command.

Return type:
str

invoke(callback: Callable[[...], V], /, *args: Any, **kwargs: Any) → V
invoke(callback: Command, /, *args: Any, **kwargs: Any) → Any
Invokes a command callback in exactly the way it expects. There are two ways to invoke this method:

the first argument can be a callback and all other arguments and keyword arguments are forwarded directly to the function.

the first argument is a click command object. In that case all arguments are forwarded as well but proper click parameters (options and click arguments) must be keyword arguments and Click will fill in defaults.

Changelog
forward(cmd, /, *args, **kwargs)
Similar to invoke() but fills in default keyword arguments from the current context if the other command expects it. This cannot invoke callbacks directly, only other commands.

Changelog
Parameters:
cmd (Command)

args (Any)

kwargs (Any)

Return type:
Any

set_parameter_source(name, source)
Set the source of a parameter. This indicates the location from which the value of the parameter was obtained.

Parameters:
name (str) – The name of the parameter.

source (ParameterSource) – A member of ParameterSource.

Return type:
None

get_parameter_source(name)
Get the source of a parameter. This indicates the location from which the value of the parameter was obtained.

This can be useful for determining when a user specified a value on the command line that is the same as the default value. It will be DEFAULT only if the value was actually taken from the default.

Parameters:
name (str) – The name of the parameter.

Return type:
ParameterSource

Changelog
click.get_current_context(silent: Literal[False] = False) → Context
click.get_current_context(silent: bool = False) → Context | None
Returns the current click context. This can be used as a way to access the current context object from anywhere. This is a more implicit alternative to the pass_context() decorator. This function is primarily useful for helpers such as echo() which might be interested in changing its behavior based on the current context.

To push the current context, Context.scope() can be used.

Changelog
Parameters:
silent – if set to True the return value is None if no context is available. The default behavior is to raise a RuntimeError.

class click.core.ParameterSource(*values)
This is an Enum that indicates the source of a parameter’s value.

Use click.Context.get_parameter_source() to get the source for a parameter by name.

Changelog
COMMANDLINE = 1
The value was provided by the command line args.

ENVIRONMENT = 2
The value was provided with an environment variable.

DEFAULT = 3
Used the default specified by the parameter.

DEFAULT_MAP = 4
Used a default provided by Context.default_map.

PROMPT = 5
Used a prompt to confirm a default or provide a value.

Types
click.STRING = STRING
Parameters:
value (t.Any)

param (Parameter | None)

ctx (Context | None)

Return type:
t.Any

click.INT = INT
Parameters:
value (t.Any)

param (Parameter | None)

ctx (Context | None)

Return type:
t.Any

click.FLOAT = FLOAT
Parameters:
value (t.Any)

param (Parameter | None)

ctx (Context | None)

Return type:
t.Any

click.BOOL = BOOL
Parameters:
value (t.Any)

param (Parameter | None)

ctx (Context | None)

Return type:
t.Any

click.UUID = UUID
Parameters:
value (t.Any)

param (Parameter | None)

ctx (Context | None)

Return type:
t.Any

click.UNPROCESSED = UNPROCESSED
Parameters:
value (t.Any)

param (Parameter | None)

ctx (Context | None)

Return type:
t.Any

class click.File(mode='r', encoding=None, errors='strict', lazy=None, atomic=False)
Declares a parameter to be a file for reading or writing. The file is automatically closed once the context tears down (after the command finished working).

Files can be opened for reading or writing. The special value - indicates stdin or stdout depending on the mode.

By default, the file is opened for reading text data, but it can also be opened in binary mode or for writing. The encoding parameter can be used to force a specific encoding.

The lazy flag controls if the file should be opened immediately or upon first IO. The default is to be non-lazy for standard input and output streams as well as files opened for reading, lazy otherwise. When opening a file lazily for reading, it is still opened temporarily for validation, but will not be held open until first IO. lazy is mainly useful when opening for writing to avoid creating the file until it is needed.

Files can also be opened atomically in which case all writes go into a separate file in the same folder and upon completion the file will be moved over to the original location. This is useful if a file regularly read by other users is modified.

See File Arguments for more information.

Changelog
Parameters:
mode (str)

encoding (str | None)

errors (str | None)

lazy (bool | None)

atomic (bool)

class click.Path(exists=False, file_okay=True, dir_okay=True, writable=False, readable=True, resolve_path=False, allow_dash=False, path_type=None, executable=False)
The Path type is similar to the File type, but returns the filename instead of an open file. Various checks can be enabled to validate the type of file and permissions.

Parameters:
exists (bool) – The file or directory needs to exist for the value to be valid. If this is not set to True, and the file does not exist, then all further checks are silently skipped.

file_okay (bool) – Allow a file as a value.

dir_okay (bool) – Allow a directory as a value.

readable (bool) – if true, a readable check is performed.

writable (bool) – if true, a writable check is performed.

executable (bool) – if true, an executable check is performed.

resolve_path (bool) – Make the value absolute and resolve any symlinks. A ~ is not expanded, as this is supposed to be done by the shell only.

allow_dash (bool) – Allow a single dash as a value, which indicates a standard stream (but does not open it). Use open_file() to handle opening this value.

path_type (type[t.Any] | None) – Convert the incoming path value to this type. If None, keep Python’s default, which is str. Useful to convert to pathlib.Path.

Changelog
class click.Choice(choices, case_sensitive=True)
The choice type allows a value to be checked against a fixed set of supported values.

You may pass any iterable value which will be converted to a tuple and thus will only be iterated once.

The resulting value will always be one of the originally passed choices. See normalize_choice() for more info on the mapping of strings to choices. See Choice for an example.

Parameters:
case_sensitive (bool) – Set to false to make choices case insensitive. Defaults to true.

choices (cabc.Iterable[ParamTypeValue])

Changelog
name: str = 'choice'
the descriptive name of this type

to_info_dict()
Gather information that could be useful for a tool generating user-facing documentation.

Use click.Context.to_info_dict() to traverse the entire CLI structure.

Changelog
Return type:
dict[str, Any]

normalize_choice(choice, ctx)
Normalize a choice value, used to map a passed string to a choice. Each choice must have a unique normalized value.

By default uses Context.token_normalize_func() and if not case sensitive, convert it to a casefolded value.

Changelog
Parameters:
choice (ParamTypeValue)

ctx (Context | None)

Return type:
str

get_metavar(param, ctx)
Returns the metavar default for this param if it provides one.

Parameters:
param (Parameter)

ctx (Context)

Return type:
str | None

get_missing_message(param, ctx)
Message shown when no choice is passed.

Changelog
Parameters:
param (Parameter)

ctx (Context | None)

Return type:
str

convert(value, param, ctx)
For a given value from the parser, normalize it and find its matching normalized value in the list of choices. Then return the matched “original” choice.

Parameters:
value (t.Any)

param (Parameter | None)

ctx (Context | None)

Return type:
ParamTypeValue

get_invalid_choice_message(value, ctx)
Get the error message when the given choice is invalid.

Parameters:
value (t.Any) – The invalid value.

ctx (Context | None)

Return type:
str

Changelog
shell_complete(ctx, param, incomplete)
Complete choices that start with the incomplete value.

Parameters:
ctx (Context) – Invocation context for this command.

param (Parameter) – The parameter that is requesting completion.

incomplete (str) – Value being completed. May be empty.

Return type:
list[CompletionItem]

Changelog
class click.IntRange(min=None, max=None, min_open=False, max_open=False, clamp=False)
Restrict an click.INT value to a range of accepted values. See Int and Float Ranges.

If min or max are not passed, any value is accepted in that direction. If min_open or max_open are enabled, the corresponding boundary is not included in the range.

If clamp is enabled, a value outside the range is clamped to the boundary instead of failing.

Changelog
Parameters:
min (float | None)

max (float | None)

min_open (bool)

max_open (bool)

clamp (bool)

class click.FloatRange(min=None, max=None, min_open=False, max_open=False, clamp=False)
Restrict a click.FLOAT value to a range of accepted values. See Int and Float Ranges.

If min or max are not passed, any value is accepted in that direction. If min_open or max_open are enabled, the corresponding boundary is not included in the range.

If clamp is enabled, a value outside the range is clamped to the boundary instead of failing. This is not supported if either boundary is marked open.

Changelog
Parameters:
min (float | None)

max (float | None)

min_open (bool)

max_open (bool)

clamp (bool)

class click.DateTime(formats=None)
The DateTime type converts date strings into datetime objects.

The format strings which are checked are configurable, but default to some common (non-timezone aware) ISO 8601 formats.

When specifying DateTime formats, you should only pass a list or a tuple. Other iterables, like generators, may lead to surprising results.

The format strings are processed using datetime.strptime, and this consequently defines the format strings which are allowed.

Parsing is tried using each format, in order, and the first format which parses successfully is used.

Parameters:
formats (cabc.Sequence[str] | None) – A list or tuple of date format strings, in the order in which they should be tried. Defaults to '%Y-%m-%d', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S'.

class click.Tuple(types)
The default behavior of Click is to apply a type on a value directly. This works well in most cases, except for when nargs is set to a fixed count and different types should be used for different items. In this case the Tuple type can be used. This type can only be used if nargs is set to a fixed number.

For more information see Multi Value Options as Tuples.

This can be selected by using a Python tuple literal as a type.

Parameters:
types (cabc.Sequence[type[t.Any] | ParamType]) – a list of types that should be used for the tuple items.

class click.ParamType
Represents the type of a parameter. Validates and converts values from the command line or Python into the correct type.

To implement a custom type, subclass and implement at least the following:

The name class attribute must be set.

Calling an instance of the type with None must return None. This is already implemented by default.

convert() must convert string values to the correct type.

convert() must accept values that are already the correct type.

It must be able to convert a value if the ctx and param arguments are None. This can occur when converting prompt input.

name: str
the descriptive name of this type

envvar_list_splitter: ClassVar[str | None] = None
if a list of this type is expected and the value is pulled from a string environment variable, this is what splits it up. None means any whitespace. For all parameters the general rule is that whitespace splits them up. The exception are paths and files which are split by os.path.pathsep by default (“:” on Unix and “;” on Windows).

to_info_dict()
Gather information that could be useful for a tool generating user-facing documentation.

Use click.Context.to_info_dict() to traverse the entire CLI structure.

Changelog
Return type:
dict[str, Any]

get_metavar(param, ctx)
Returns the metavar default for this param if it provides one.

Parameters:
param (Parameter)

ctx (Context)

Return type:
str | None

get_missing_message(param, ctx)
Optionally might return extra information about a missing parameter.

Changelog
Parameters:
param (Parameter)

ctx (Context | None)

Return type:
str | None

convert(value, param, ctx)
Convert the value to the correct type. This is not called if the value is None (the missing value).

This must accept string values from the command line, as well as values that are already the correct type. It may also convert other compatible types.

The param and ctx arguments may be None in certain situations, such as when converting prompt input.

If the value cannot be converted, call fail() with a descriptive message.

Parameters:
value (t.Any) – The value to convert.

param (Parameter | None) – The parameter that is using this type to convert its value. May be None.

ctx (Context | None) – The current context that arrived at this value. May be None.

Return type:
t.Any

split_envvar_value(rv)
Given a value from an environment variable this splits it up into small chunks depending on the defined envvar list splitter.

If the splitter is set to None, which means that whitespace splits, then leading and trailing whitespace is ignored. Otherwise, leading and trailing splitters usually lead to empty items being included.

Parameters:
rv (str)

Return type:
Sequence[str]

fail(message, param=None, ctx=None)
Helper method to fail with an invalid value message.

Parameters:
message (str)

param (Parameter | None)

ctx (Context | None)

Return type:
t.NoReturn

shell_complete(ctx, param, incomplete)
Return a list of CompletionItem objects for the incomplete value. Most types do not provide completions, but some do, and this allows custom types to provide custom completions as well.

Parameters:
ctx (Context) – Invocation context for this command.

param (Parameter) – The parameter that is requesting completion.

incomplete (str) – Value being completed. May be empty.

Return type:
list[CompletionItem]

Changelog
Exceptions
exception click.ClickException(message)
An exception that Click can handle and show to the user.

Parameters:
message (str)

Return type:
None

exception click.Abort
An internal signalling exception that signals Click to abort.

exception click.UsageError(message, ctx=None)
An internal exception that signals a usage error. This typically aborts any further handling.

Parameters:
message (str) – the error message to display.

ctx (Context | None) – optionally the context that caused this error. Click will fill in the context automatically in some situations.

Return type:
None

exception click.BadParameter(message, ctx=None, param=None, param_hint=None)
An exception that formats out a standardized error message for a bad parameter. This is useful when thrown from a callback or type as Click will attach contextual information to it (for instance, which parameter it is).

Changelog
Parameters:
param (Parameter | None) – the parameter object that caused this error. This can be left out, and Click will attach this info itself if possible.

param_hint (cabc.Sequence[str] | str | None) – a string that shows up as parameter name. This can be used as alternative to param in cases where custom validation should happen. If it is a string it’s used as such, if it’s a list then each item is quoted and separated.

message (str)

ctx (Context | None)

Return type:
None

exception click.FileError(filename, hint=None)
Raised if a file cannot be opened.

Parameters:
filename (str)

hint (str | None)

Return type:
None

exception click.NoSuchOption(option_name, message=None, possibilities=None, ctx=None)
Raised if click attempted to handle an option that does not exist.

Changelog
Parameters:
option_name (str)

message (str | None)

possibilities (cabc.Sequence[str] | None)

ctx (Context | None)

Return type:
None

exception click.BadOptionUsage(option_name, message, ctx=None)
Raised if an option is generally supplied but the use of the option was incorrect. This is for instance raised if the number of arguments for an option is not correct.

Changelog
Parameters:
option_name (str) – the name of the option being used incorrectly.

message (str)

ctx (Context | None)

Return type:
None

exception click.BadArgumentUsage(message, ctx=None)
Raised if an argument is generally supplied but the use of the argument was incorrect. This is for instance raised if the number of values for an argument is not correct.

Changelog
Parameters:
message (str)

ctx (Context | None)

Return type:
None

Formatting
class click.HelpFormatter(indent_increment=2, width=None, max_width=None)
This class helps with formatting text-based help pages. It’s usually just needed for very special internal cases, but it’s also exposed so that developers can write their own fancy outputs.

At present, it always writes into memory.

Parameters:
indent_increment (int) – the additional increment for each level.

width (int | None) – the width for the text. This defaults to the terminal width clamped to a maximum of 78.

max_width (int | None)

write(string)
Writes a unicode string into the internal buffer.

Parameters:
string (str)

Return type:
None

indent()
Increases the indentation.

Return type:
None

dedent()
Decreases the indentation.

Return type:
None

write_usage(prog, args='', prefix=None)
Writes a usage line into the buffer.

Parameters:
prog (str) – the program name.

args (str) – whitespace separated list of arguments.

prefix (str | None) – The prefix for the first line. Defaults to "Usage: ".

Return type:
None

write_heading(heading)
Writes a heading into the buffer.

Parameters:
heading (str)

Return type:
None

write_paragraph()
Writes a paragraph into the buffer.

Return type:
None

write_text(text)
Writes re-indented text into the buffer. This rewraps and preserves paragraphs.

Parameters:
text (str)

Return type:
None

write_dl(rows, col_max=30, col_spacing=2)
Writes a definition list into the buffer. This is how options and commands are usually formatted.

Parameters:
rows (Sequence[tuple[str, str]]) – a list of two item tuples for the terms and values.

col_max (int) – the maximum width of the first column.

col_spacing (int) – the number of spaces between the first and second column.

Return type:
None

section(name)
Helpful context manager that writes a paragraph, a heading, and the indents.

Parameters:
name (str) – the section name that is written as heading.

Return type:
Iterator[None]

indentation()
A context manager that increases the indentation.

Return type:
Iterator[None]

getvalue()
Returns the buffer contents.

Return type:
str

click.wrap_text(text, width=78, initial_indent='', subsequent_indent='', preserve_paragraphs=False)
A helper function that intelligently wraps text. By default, it assumes that it operates on a single paragraph of text but if the preserve_paragraphs parameter is provided it will intelligently handle paragraphs (defined by two empty lines).

If paragraphs are handled, a paragraph can be prefixed with an empty line containing the \b character (\x08) to indicate that no rewrapping should happen in that block.

Parameters:
text (str) – the text that should be rewrapped.

width (int) – the maximum width for the text.

initial_indent (str) – the initial indent that should be placed on the first line as a string.

subsequent_indent (str) – the indent string that should be placed on each consecutive line.

preserve_paragraphs (bool) – if this flag is set then the wrapping will intelligently handle paragraphs.

Return type:
str

Parsing
click.OptionParser
alias of _OptionParser

Shell Completion
See Shell Completion for information about enabling and customizing Click’s shell completion system.

class click.shell_completion.CompletionItem(value, type='plain', help=None, **kwargs)
Represents a completion value and metadata about the value. The default metadata is type to indicate special shell handling, and help if a shell supports showing a help string next to the value.

Arbitrary parameters can be passed when creating the object, and accessed using item.attr. If an attribute wasn’t passed, accessing it returns None.

Parameters:
value (t.Any) – The completion suggestion.

type (str) – Tells the shell script to provide special completion support for the type. Click uses "dir" and "file".

help (str | None) – String shown next to the value if supported.

kwargs (t.Any) – Arbitrary metadata. The built-in implementations don’t use this, but custom type completions paired with custom shell support could use it.

class click.shell_completion.ShellComplete(cli, ctx_args, prog_name, complete_var)
Base class for providing shell completion support. A subclass for a given shell will override attributes and methods to implement the completion instructions (source and complete).

Parameters:
cli (Command) – Command being called.

prog_name (str) – Name of the executable in the shell.

complete_var (str) – Name of the environment variable that holds the completion instruction.

ctx_args (cabc.MutableMapping[str, t.Any])

Changelog
name: ClassVar[str]
Name to register the shell as with add_completion_class(). This is used in completion instructions ({name}_source and {name}_complete).

source_template: ClassVar[str]
Completion script template formatted by source(). This must be provided by subclasses.

property func_name: str
The name of the shell function defined by the completion script.

source_vars()
Vars for formatting source_template.

By default this provides complete_func, complete_var, and prog_name.

Return type:
dict[str, Any]

source()
Produce the shell script that defines the completion function. By default this %-style formats source_template with the dict returned by source_vars().

Return type:
str

get_completion_args()
Use the env vars defined by the shell script to return a tuple of args, incomplete. This must be implemented by subclasses.

Return type:
tuple[list[str], str]

get_completions(args, incomplete)
Determine the context and last complete command or parameter from the complete args. Call that object’s shell_complete method to get the completions for the incomplete value.

Parameters:
args (list[str]) – List of complete args before the incomplete value.

incomplete (str) – Value being completed. May be empty.

Return type:
list[CompletionItem]

format_completion(item)
Format a completion item into the form recognized by the shell script. This must be implemented by subclasses.

Parameters:
item (CompletionItem) – Completion item to format.

Return type:
str

complete()
Produce the completion data to send back to the shell.

By default this calls get_completion_args(), gets the completions, then calls format_completion() for each completion.

Return type:
str

click.shell_completion.add_completion_class(cls, name=None)
Register a ShellComplete subclass under the given name. The name will be provided by the completion instruction environment variable during completion.

Parameters:
cls (ShellCompleteType) – The completion class that will handle completion for the shell.

name (str | None) – Name to register the class under. Defaults to the class’s name attribute.

Return type:
ShellCompleteType

Testing
class click.testing.CliRunner(charset='utf-8', env=None, echo_stdin=False, catch_exceptions=True)
The CLI runner provides functionality to invoke a Click command line script for unittesting purposes in a isolated environment. This only works in single-threaded systems without any concurrency as it changes the global interpreter state.

Parameters:
charset (str) – the character set for the input and output data.

env (cabc.Mapping[str, str | None] | None) – a dictionary with environment variables for overriding.

echo_stdin (bool) – if this is set to True, then reading from <stdin> writes to <stdout>. This is useful for showing examples in some circumstances. Note that regular prompts will automatically echo the input.

catch_exceptions (bool) – Whether to catch any exceptions other than SystemExit when running invoke().

Changelog
get_default_prog_name(cli)
Given a command object it will return the default program name for it. The default is the name attribute or "root" if not set.

Parameters:
cli (Command)

Return type:
str

make_env(overrides=None)
Returns the environment overrides for invoking a script.

Parameters:
overrides (Mapping[str, str | None] | None)

Return type:
Mapping[str, str | None]

isolation(input=None, env=None, color=False)
A context manager that sets up the isolation for invoking of a command line tool. This sets up <stdin> with the given input data and os.environ with the overrides from the given dictionary. This also rebinds some internals in Click to be mocked (like the prompt functionality).

This is automatically done in the invoke() method.

Parameters:
input (str | bytes | IO[Any] | None) – the input stream to put into sys.stdin.

env (Mapping[str, str | None] | None) – the environment overrides as dictionary.

color (bool) – whether the output should contain color codes. The application can still override this explicitly.

Return type:
Iterator[tuple[BytesIO, BytesIO, BytesIO]]

Changelog
invoke(cli, args=None, input=None, env=None, catch_exceptions=None, color=False, **extra)
Invokes a command in an isolated environment. The arguments are forwarded directly to the command line script, the extra keyword arguments are passed to the main() function of the command.

This returns a Result object.

Parameters:
cli (Command) – the command to invoke

args (str | cabc.Sequence[str] | None) – the arguments to invoke. It may be given as an iterable or a string. When given as string it will be interpreted as a Unix shell command. More details at shlex.split().

input (str | bytes | t.IO[t.Any] | None) – the input data for sys.stdin.

env (cabc.Mapping[str, str | None] | None) – the environment overrides.

catch_exceptions (bool | None) – Whether to catch any other exceptions than SystemExit. If None, the value from CliRunner is used.

extra (t.Any) – the keyword arguments to pass to main().

color (bool) – whether the output should contain color codes. The application can still override this explicitly.

Return type:
Result

Changelog
isolated_filesystem(temp_dir=None)
A context manager that creates a temporary directory and changes the current working directory to it. This isolates tests that affect the contents of the CWD to prevent them from interfering with each other.

Parameters:
temp_dir (str | PathLike[str] | None) – Create the temporary directory under this directory. If given, the created directory is not removed when exiting.

Return type:
Iterator[str]

Changelog
class click.testing.Result(runner, stdout_bytes, stderr_bytes, output_bytes, return_value, exit_code, exception, exc_info=None)
Holds the captured result of an invoked CLI script.

Parameters:
runner (CliRunner) – The runner that created the result

stdout_bytes (bytes) – The standard output as bytes.

stderr_bytes (bytes) – The standard error as bytes.

output_bytes (bytes) – A mix of stdout_bytes and stderr_bytes, as the user would see it in its terminal.

return_value (t.Any) – The value returned from the invoked command.

exit_code (int) – The exit code as integer.

exception (BaseException | None) – The exception that happened if one did.

exc_info (tuple[type[BaseException], BaseException, TracebackType] | None) – Exception information (exception type, exception instance, traceback type).

Changelog
property output: str
The terminal output as unicode string, as the user would see it.

Changelog
property stdout: str
The standard output as unicode string.

property stderr: str
The standard error as unicode string.

Changelog