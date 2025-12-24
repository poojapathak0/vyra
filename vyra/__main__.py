"""Vyra CLI - Command-line interface"""

import sys
import os
import argparse
from pathlib import Path
from rich.console import Console
from rich.syntax import Syntax
from rich.panel import Panel
from rich.markdown import Markdown

from .parser import VyraParser
from .logic_graph import LogicGraph
from .interpreter import VyraInterpreter
from .ai_rewriter import rewrite_source, AiRewriteError, AiRewriteConfig

console = Console()


def run_file(filepath: str, debug: bool = False, visualize: bool = False, ai: bool = False):
    """Run a Vyra file"""
    try:
        # Read source code
        with open(filepath, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        console.print(f"\n[bold cyan]Running:[/bold cyan] {filepath}\n")
        
        # Optional AI rewrite (disabled by default)
        if ai:
            console.print("[yellow]🧠 AI rewrite...[/yellow]")
            try:
                source_code, _info = rewrite_source(source_code, config=AiRewriteConfig(enabled=True))
            except AiRewriteError as e:
                console.print(f"[bold red]❌ AI Rewrite Error:[/bold red] {e}")
                return 1

        # Parse
        console.print("[yellow]📝 Parsing...[/yellow]")
        parser = VyraParser()
        ast = parser.parse(source_code)
        
        if parser.errors:
            console.print("[bold red]❌ Parsing Errors:[/bold red]")
            for error in parser.errors:
                console.print(f"  [red]{error}[/red]")
            return 1
        
        console.print("[green]✓ Parsing successful![/green]")
        
        # Build logic graph
        console.print("[yellow]🔗 Building logic graph...[/yellow]")
        graph = LogicGraph()
        graph.from_ast(ast)
        console.print(f"[green]✓ Graph built ({len(graph.nodes)} nodes, {len(graph.edges)} edges)[/green]")
        
        # Visualize if requested
        if visualize:
            output_dir = Path("graph_output")
            output_dir.mkdir(exist_ok=True)
            viz_path = output_dir / f"{Path(filepath).stem}_graph.png"
            console.print(f"[yellow]📊 Visualizing graph to {viz_path}...[/yellow]")
            graph.visualize(str(viz_path))
        
        # Execute
        console.print("[yellow]🚀 Executing...[/yellow]")
        console.print("[cyan]" + "="*50 + "[/cyan]\n")
        
        interpreter = VyraInterpreter(debug=debug)
        result = interpreter.execute(graph)
        
        console.print(f"\n[cyan]" + "="*50 + "[/cyan]")
        console.print("[green]✓ Execution completed![/green]")
        
        if result is not None:
            console.print(f"[bold]Return value:[/bold] {result}")
        
        return 0
    
    except FileNotFoundError:
        console.print(f"[bold red]❌ Error:[/bold red] File not found: {filepath}")
        return 1
    except Exception as e:
        console.print(f"[bold red]❌ Error:[/bold red] {str(e)}")
        if debug:
            import traceback
            console.print("[red]" + traceback.format_exc() + "[/red]")
        return 1


def repl(ai: bool = False):
    """Interactive REPL for Vyra"""
    console.print(Panel.fit(
        "[bold cyan]Vyra REPL[/bold cyan]\n"
        "Write code in plain English!\n"
        "Type 'exit' or 'quit' to leave, 'help' for commands.",
        border_style="cyan"
    ))
    
    parser = VyraParser()
    interpreter = VyraInterpreter()
    graph = LogicGraph()
    
    # Initialize a persistent context
    line_buffer = []
    
    while True:
        try:
            # Check if we're in multi-line mode (waiting for indented block)
            if line_buffer:
                prompt = "...  "
            else:
                prompt = ">>> "
            
            line = input(prompt)
            
            # Handle special commands
            if not line_buffer and line.lower() in ['exit', 'quit']:
                console.print("[cyan]Goodbye! 👋[/cyan]")
                break
            
            if not line_buffer and line.lower() == 'help':
                console.print("""
[bold cyan]Vyra REPL Commands:[/bold cyan]
  exit, quit     - Exit the REPL
  help           - Show this help message
  clear          - Clear the screen
  vars           - Show all variables
  graph          - Visualize current logic graph
  
[bold cyan]Example code:[/bold cyan]
  Set x to 5.
  Display "Hello, World!".
  If x is greater than 3, display "Big number".
                """)
                continue
            
            if not line_buffer and line.lower() == 'clear':
                os.system('cls' if os.name == 'nt' else 'clear')
                continue
            
            if not line_buffer and line.lower() == 'vars':
                console.print("[cyan]Variables:[/cyan]")
                for var, value in interpreter.context.scopes[-1].items():
                    if not var.startswith('__'):
                        console.print(f"  {var} = {value}")
                continue
            
            if not line_buffer and line.lower() == 'graph':
                try:
                    graph.visualize()
                except Exception as e:
                    console.print(f"[red]Error visualizing: {e}[/red]")
                continue
            
            # Handle multi-line input (blocks with : or indented lines)
            if line.strip().endswith(':') or (line_buffer and line.startswith('  ')):
                line_buffer.append(line)
                continue
            
            # If we have buffered lines, add current line and process
            if line_buffer:
                line_buffer.append(line)
                # Check if block is complete (no more indented lines)
                if not line.startswith('  ') and line.strip():
                    full_code = '\n'.join(line_buffer)
                    line_buffer = []
                else:
                    continue
            else:
                full_code = line
            
            if not full_code.strip():
                continue
            
            # Parse and execute
            try:
                if ai:
                    try:
                        full_code, _info = rewrite_source(full_code, config=AiRewriteConfig(enabled=True))
                    except AiRewriteError as e:
                        console.print(f"[red]AI Rewrite Error: {e}[/red]")
                        continue

                ast = parser.parse(full_code)
                
                if parser.errors:
                    for error in parser.errors:
                        console.print(f"[red]{error}[/red]")
                    parser.errors = []
                    continue
                
                graph = LogicGraph()
                graph.from_ast(ast)
                
                result = interpreter.execute(graph)
                
                if result is not None:
                    console.print(f"[dim]→ {result}[/dim]")
            
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")
        
        except KeyboardInterrupt:
            console.print("\n[yellow]Use 'exit' to quit[/yellow]")
            line_buffer = []
            continue
        except EOFError:
            console.print("\n[cyan]Goodbye! 👋[/cyan]")
            break


def parse_only(filepath: str, output: str = None, ai: bool = False):
    """Parse file and output AST"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            source_code = f.read()

        if ai:
            try:
                source_code, _info = rewrite_source(source_code, config=AiRewriteConfig(enabled=True))
            except AiRewriteError as e:
                console.print(f"[bold red]AI Rewrite Error:[/bold red] {e}")
                return 1
        
        parser = VyraParser()
        ast = parser.parse(source_code)
        
        if parser.errors:
            console.print("[bold red]Parsing Errors:[/bold red]")
            for error in parser.errors:
                console.print(f"  [red]{error}[/red]")
            return 1
        
        # Build and export graph
        graph = LogicGraph()
        graph.from_ast(ast)
        
        graph_json = graph.to_json()
        
        if output:
            with open(output, 'w') as f:
                f.write(graph_json)
            console.print(f"[green]✓ Graph saved to {output}[/green]")
        else:
            console.print(graph_json)
        
        return 0
    
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        return 1


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Vyra - Programming in Plain English",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    vyra run program.intent              Run a program
    vyra run --debug program.intent      Run with debug output
    vyra run --viz program.intent        Run and visualize graph
    vyra repl                            Start interactive REPL
    vyra parse program.intent            Parse and show graph
    vyra parse -o graph.json program     Export graph to JSON
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Run command
    run_parser = subparsers.add_parser('run', help='Run a Vyra program')
    run_parser.add_argument('file', help='Vyra source file (.intent)')
    run_parser.add_argument('-d', '--debug', action='store_true', help='Enable debug output')
    run_parser.add_argument('-v', '--viz', action='store_true', help='Visualize logic graph')
    run_parser.add_argument('--ai', action='store_true', help='Enable optional AI rewrite (requires VYRA_AI_URL and VYRA_AI_MODEL)')
    
    # REPL command
    repl_parser = subparsers.add_parser('repl', help='Start interactive REPL')
    repl_parser.add_argument('--ai', action='store_true', help='Enable optional AI rewrite (requires VYRA_AI_URL and VYRA_AI_MODEL)')
    
    # Parse command
    parse_parser = subparsers.add_parser('parse', help='Parse file and output graph')
    parse_parser.add_argument('file', help='Vyra source file')
    parse_parser.add_argument('-o', '--output', help='Output file for graph JSON')
    parse_parser.add_argument('--ai', action='store_true', help='Enable optional AI rewrite (requires VYRA_AI_URL and VYRA_AI_MODEL)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    if args.command == 'run':
        return run_file(args.file, debug=args.debug, visualize=args.viz, ai=args.ai)
    
    elif args.command == 'repl':
        repl(ai=getattr(args, 'ai', False))
        return 0
    
    elif args.command == 'parse':
        return parse_only(args.file, args.output, ai=args.ai)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
