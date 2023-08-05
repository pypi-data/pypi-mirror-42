import click
import click_repl

@click.command(
    short_help="Interactive shell",
    help="Launch an interactive shell for launching Tutor commands"
)
def ui():
    click.echo("""Welcome to the Tutor interactive shell UI!
Type "help" to view all available commands.
Type "local quickstart" to configure and launch a new platform from scratch.
""")
    click_repl.repl(click.get_current_context())
