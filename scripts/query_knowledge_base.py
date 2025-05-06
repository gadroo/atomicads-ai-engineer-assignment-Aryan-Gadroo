#!/usr/bin/env python
"""
Query the knowledge base using RAG
"""
import sys
import os
import logging
import typer
from rich.console import Console
from rich.panel import Panel

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.rag_service import RAGService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)
console = Console()

def main(query: str = typer.Argument(..., help="Query to search for in the knowledge base")):
    """Query the knowledge base with a natural language query"""
    try:
        # Initialize RAG Service
        rag_service = RAGService()
        
        # Get the response
        response = rag_service.query(query)
        
        # Print the response in a rich panel
        console.print(Panel(response, title="🤖 Response", border_style="green"))
        
        # Print the sources/context used
        console.print("\n[bold]Sources/Context Used:[/bold]")
        for i, source in enumerate(rag_service.last_context_chunks, 1):
            if "metadata" in source and "source" in source["metadata"]:
                console.print(f"[cyan]{i}.[/cyan] {source['metadata']['source']}")
            else:
                console.print(f"[cyan]{i}.[/cyan] Unknown source")
        
    except Exception as e:
        logger.error(f"Error during query: {str(e)}")
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    typer.run(main) 