import typer
import json
import logging
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table
from rich.progress import Progress
from typing import Dict, Any, Optional
import os

from src.core.rag_service import RAGService
from src.api.meta_ads_api import MetaAdsAPI
from src.utils.validators import CampaignValidator

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize Typer app
app = typer.Typer(help="AI-Powered Meta Ads Campaign Generator")
console = Console()

@app.command()
def create_campaign(
    interactive: bool = typer.Option(
        True, "--interactive/--no-interactive", "-i/-n", 
        help="Run in interactive mode to collect campaign information"
    ),
    input_file: Optional[str] = typer.Option(
        None, "--input", "-f", 
        help="JSON file containing campaign brief"
    ),
    output_file: Optional[str] = typer.Option(
        None, "--output", "-o", 
        help="Output file for generated campaign specification"
    ),
    execute: bool = typer.Option(
        False, "--execute/--no-execute", "-e/-E", 
        help="Execute campaign creation on Meta Ads platform"
    )
):
    """
    Generate and optionally create a Meta Ads campaign using AI.
    
    This command will use a RAG-enhanced LLM to generate a complete campaign 
    specification based on your brief, validate it, and optionally execute it
    on the Meta Ads platform.
    """
    try:
        console.print(Panel(
            Markdown("# AI-Powered Meta Ads Campaign Generator"),
            subtitle="Create effective ad campaigns with minimal input"
        ))
        
        # Initialize services
        rag_service = RAGService()
        
        # Collect campaign brief
        if interactive and not input_file:
            campaign_brief = _collect_campaign_brief_interactive()
        elif input_file:
            campaign_brief = _load_campaign_brief_from_file(input_file)
        else:
            console.print("[bold red]Error:[/bold red] Must either use interactive mode or provide an input file")
            raise typer.Exit(code=1)
        
        # Display campaign brief
        console.print("\n[bold]Campaign Brief:[/bold]")
        for key, value in campaign_brief.items():
            console.print(f"  [bold]{key}:[/bold] {value}")
        
        # Generate campaign specification
        with Progress() as progress:
            task = progress.add_task("[green]Generating campaign specification...", total=1)
            console.print("\n[bold]Generating campaign specification using AI...[/bold]")
            campaign_spec = rag_service.generate_campaign(campaign_brief)
            progress.update(task, advance=1)
        
        # Validate campaign specification
        console.print("\n[bold]Validating campaign specification...[/bold]")
        is_valid, validation_results = CampaignValidator.validate_campaign_specification(campaign_spec)
        
        if not is_valid:
            console.print("[bold red]Campaign specification has validation issues:[/bold red]")
            for issue in validation_results["issues"]:
                console.print(f"  • {issue}")
            
            console.print("\n[bold yellow]Would you like to review the generated specification anyway?[/bold yellow]")
            review_anyway = typer.confirm("Review specification?", default=True)
            
            if not review_anyway:
                console.print("[bold red]Exiting due to validation issues[/bold red]")
                raise typer.Exit(code=1)
        else:
            console.print("[bold green]Campaign specification is valid![/bold green]")
        
        # Display campaign specification summary
        _display_campaign_summary(campaign_spec)
        
        # Save specification if requested
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(campaign_spec, f, indent=2)
            console.print(f"\n[bold green]Campaign specification saved to {output_file}[/bold green]")
        
        # Execute campaign creation if requested
        if execute:
            _execute_campaign(campaign_spec)
        else:
            console.print("\n[bold yellow]Campaign was not executed. Use --execute flag to create it on Meta Ads.[/bold yellow]")
        
    except Exception as e:
        logger.exception("Error in campaign creation")
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        raise typer.Exit(code=1)

def _collect_campaign_brief_interactive() -> Dict[str, Any]:
    """Collect campaign brief information interactively.
    
    Returns:
        Dict[str, Any]: Campaign brief dictionary
    """
    console.print("\n[bold]Please provide information about your campaign:[/bold]")
    
    brief = {}
    
    # Basic campaign information
    brief["platform"] = "Meta"
    brief["product_name"] = typer.prompt("Product/Service Name")
    brief["product_description"] = typer.prompt("Product/Service Description (1-2 sentences)")
    
    # Campaign objective
    objectives = {
        "awareness": "OUTCOME_AWARENESS",
        "engagement": "OUTCOME_ENGAGEMENT",
        "conversions": "OUTCOME_SALES",
        "leads": "OUTCOME_LEAD_GENERATION",
        "app_installs": "OUTCOME_APP_PROMOTION",
        "traffic": "OUTCOME_TRAFFIC"
    }
    
    objective_options = list(objectives.keys())
    
    console.print("\n[bold]Campaign Objective:[/bold]")
    for i, obj in enumerate(objective_options):
        console.print(f"  {i+1}. {obj.title()}")
    
    objective_index = typer.prompt(
        "Select campaign objective (1-6)", 
        type=int,
        default=1
    )
    
    while objective_index < 1 or objective_index > len(objective_options):
        console.print("[bold red]Invalid selection. Please try again.[/bold red]")
        objective_index = typer.prompt(
            "Select campaign objective (1-6)", 
            type=int,
            default=1
        )
    
    brief["objective"] = objectives[objective_options[objective_index - 1]]
    
    # Budget
    brief["daily_budget"] = typer.prompt("Daily Budget (in USD)", type=float, default=10.0)
    
    # Schedule
    brief["start_date"] = typer.prompt("Start Date (YYYY-MM-DD)", default="2023-10-01")
    brief["end_date"] = typer.prompt("End Date (YYYY-MM-DD)", default="2023-10-31")
    
    # Target audience
    brief["target_audience"] = typer.prompt("Target Audience Description")
    brief["age_min"] = typer.prompt("Minimum Age", type=int, default=18)
    brief["age_max"] = typer.prompt("Maximum Age", type=int, default=65)
    
    gender_options = ["All", "Men", "Women"]
    console.print("\n[bold]Target Gender:[/bold]")
    for i, gender in enumerate(gender_options):
        console.print(f"  {i+1}. {gender}")
    
    gender_index = typer.prompt(
        "Select target gender (1-3)", 
        type=int,
        default=1
    )
    
    while gender_index < 1 or gender_index > len(gender_options):
        console.print("[bold red]Invalid selection. Please try again.[/bold red]")
        gender_index = typer.prompt(
            "Select target gender (1-3)", 
            type=int,
            default=1
        )
    
    brief["gender"] = gender_options[gender_index - 1]
    
    # Locations
    brief["locations"] = typer.prompt("Target Locations (comma-separated)")
    
    # Creative guidelines
    brief["brand_voice"] = typer.prompt("Brand Voice/Tone")
    brief["key_selling_points"] = typer.prompt("Key Selling Points (comma-separated)")
    brief["call_to_action"] = typer.prompt("Call to Action", default="Learn More")
    brief["website_url"] = typer.prompt("Website URL")
    
    return brief

def _load_campaign_brief_from_file(file_path: str) -> Dict[str, Any]:
    """Load campaign brief from a JSON file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        Dict[str, Any]: Campaign brief dictionary
    """
    try:
        with open(file_path, 'r') as f:
            brief = json.load(f)
        return brief
    except Exception as e:
        console.print(f"[bold red]Error loading brief from file:[/bold red] {str(e)}")
        raise

def _display_campaign_summary(campaign_spec: Dict[str, Any]) -> None:
    """Display a summary of the generated campaign specification.
    
    Args:
        campaign_spec: Campaign specification dictionary
    """
    console.print("\n[bold]Campaign Specification Summary:[/bold]")
    
    # Campaign table
    campaign_table = Table(title="Campaign Details", show_header=True)
    campaign_table.add_column("Property", style="cyan")
    campaign_table.add_column("Value", style="green")
    
    campaign = campaign_spec["campaign"]
    campaign_table.add_row("Name", campaign["name"])
    campaign_table.add_row("Objective", campaign["objective"])
    campaign_table.add_row("Status", campaign["status"])
    campaign_table.add_row("Special Ad Categories", ", ".join(campaign.get("special_ad_categories", [])))
    
    console.print(campaign_table)
    
    # Ad Set table
    ad_set_table = Table(title="Ad Set Details", show_header=True)
    ad_set_table.add_column("Property", style="cyan")
    ad_set_table.add_column("Value", style="green")
    
    ad_set = campaign_spec["ad_set"]
    ad_set_table.add_row("Name", ad_set["name"])
    ad_set_table.add_row("Optimization Goal", ad_set["optimization_goal"])
    ad_set_table.add_row("Billing Event", ad_set["billing_event"])
    ad_set_table.add_row("Bid Strategy", ad_set["bid_strategy"])
    
    budget = ad_set["budget"]
    ad_set_table.add_row("Budget Type", budget["type"])
    ad_set_table.add_row("Budget Amount", f"${budget['amount']/100:.2f}")
    
    if "schedule" in ad_set:
        schedule = ad_set["schedule"]
        ad_set_table.add_row("Start Time", schedule.get("start_time", "N/A"))
        ad_set_table.add_row("End Time", schedule.get("end_time", "N/A"))
    
    console.print(ad_set_table)
    
    # Targeting table
    targeting_table = Table(title="Targeting Details", show_header=True)
    targeting_table.add_column("Property", style="cyan")
    targeting_table.add_column("Value", style="green")
    
    targeting = ad_set["targeting"]
    
    if "age_min" in targeting and "age_max" in targeting:
        targeting_table.add_row("Age Range", f"{targeting['age_min']} - {targeting['age_max']}")
    
    if "genders" in targeting:
        genders = []
        for gender in targeting["genders"]:
            if gender == 1:
                genders.append("Men")
            elif gender == 2:
                genders.append("Women")
        targeting_table.add_row("Genders", ", ".join(genders) if genders else "All")
    
    if "geo_locations" in targeting:
        geo = targeting["geo_locations"]
        locations = []
        
        if "countries" in geo:
            locations.append(f"Countries: {', '.join(geo['countries'])}")
        if "cities" in geo:
            city_names = [city.get("name", "Unknown") for city in geo.get("cities", [])]
            locations.append(f"Cities: {', '.join(city_names)}")
        
        targeting_table.add_row("Locations", "\n".join(locations))
    
    console.print(targeting_table)
    
    # Ad Creative table
    creative_table = Table(title="Ad Creative Details", show_header=True)
    creative_table.add_column("Property", style="cyan")
    creative_table.add_column("Value", style="green")
    
    ad = campaign_spec["ad"]
    creative = ad["creative"]
    
    creative_table.add_row("Ad Name", ad["name"])
    creative_table.add_row("Title", creative["title"])
    creative_table.add_row("Body", creative["body"])
    creative_table.add_row("Call to Action", creative["call_to_action"])
    creative_table.add_row("Link", creative["link"])
    
    if "image_description" in creative:
        creative_table.add_row("Image Description", creative["image_description"])
    
    console.print(creative_table)
    
    # Reasoning/Analysis
    if "reasoning" in campaign_spec:
        reasoning = campaign_spec["reasoning"]
        
        reasoning_panel = Panel(
            Markdown("\n".join([
                f"### Audience Analysis\n{reasoning.get('audience_analysis', 'N/A')}",
                f"\n### Creative Strategy\n{reasoning.get('creative_strategy', 'N/A')}",
                f"\n### Budget Rationale\n{reasoning.get('budget_rationale', 'N/A')}",
                f"\n### Expected Performance\n{reasoning.get('expected_performance', 'N/A')}"
            ])),
            title="Campaign Analysis & Reasoning",
            expand=False
        )
        
        console.print(reasoning_panel)

def _execute_campaign(campaign_spec: Dict[str, Any]) -> None:
    """Execute campaign creation on Meta Ads platform.
    
    Args:
        campaign_spec: Campaign specification dictionary
    """
    try:
        console.print("\n[bold]Executing campaign creation on Meta Ads platform...[/bold]")
        
        # Initialize Meta Ads API client
        meta_ads_api = MetaAdsAPI()
        
        # Create the campaign
        with Progress() as progress:
            task = progress.add_task("[green]Creating campaign...", total=1)
            
            response = meta_ads_api.create_full_campaign(campaign_spec)
            
            progress.update(task, advance=1)
        
        # Check response
        if response["success"]:
            console.print("[bold green]Campaign created successfully![/bold green]")
            console.print(f"  Campaign ID: {response['campaign_id']}")
            console.print(f"  Ad Set ID: {response['ad_set_id']}")
            console.print(f"  Ad ID: {response['ad_id']}")
            console.print(f"  Creative ID: {response['creative_id']}")
        else:
            console.print("[bold red]Failed to create campaign:[/bold red]")
            console.print(f"  Stage: {response.get('stage', 'unknown')}")
            console.print(f"  Error: {response.get('error', 'unknown error')}")
            
    except Exception as e:
        console.print(f"[bold red]Error executing campaign:[/bold red] {str(e)}")
        raise

if __name__ == "__main__":
    app() 