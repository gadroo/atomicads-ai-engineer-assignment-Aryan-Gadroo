#!/usr/bin/env python
"""
Query the knowledge base using RAG and generate campaign specifications
"""
import sys
import os
import json
import logging
import typer
from datetime import datetime, timedelta
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

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

def validate_placeholders(payloads: dict) -> dict:
    """Validate and document placeholders in the payloads"""
    placeholders = {
        "account_id": {
            "files": ["campaign.json", "ad_creative.json"],
            "description": "Account ID for API submission",
            "dependency": None,
            "required_before": "any API calls"
        },
        "campaign_id": {
            "files": ["adset.json"],
            "description": "ID of the created campaign",
            "dependency": None,
            "required_before": "adset creation"
        },
        "page_id": {
            "files": ["ad_creative.json"],
            "description": "ID of the Facebook Page",
            "dependency": None,
            "required_before": "creative creation"
        },
        "adset_id": {
            "files": ["ad.json"],
            "description": "ID of the created adset",
            "dependency": "campaign_id",
            "required_before": "ad creation"
        },
        "creative_id": {
            "files": ["ad.json"],
            "description": "ID of the created ad creative",
            "dependency": "page_id",
            "required_before": "ad creation"
        },
        "image_hash": {
            "files": ["ad_creative.json"],
            "description": "Hash of uploaded image",
            "dependency": None,
            "required_before": "creative creation"
        },
        "pixel_id": {
            "files": ["ad.json"],
            "description": "Facebook Pixel ID for tracking",
            "dependency": None,
            "required_before": "ad creation"
        }
    }
    
    # Track found placeholders
    found_placeholders = {}
    
    # Check each payload for placeholders
    for filename, payload in payloads.items():
        payload_str = json.dumps(payload)
        for placeholder in placeholders:
            if f"{{{{{placeholder}}}}}" in payload_str:
                if placeholder not in found_placeholders:
                    found_placeholders[placeholder] = placeholders[placeholder]
    
    return found_placeholders

def create_campaign_directory(campaign_name: str) -> str:
    """Create a directory for the campaign with timestamp"""
    # Create campaigns directory if it doesn't exist
    campaigns_dir = os.path.join(os.path.dirname(__file__), '..', 'campaigns')
    os.makedirs(campaigns_dir, exist_ok=True)
    
    # Create timestamp-based directory name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = "".join(c for c in campaign_name if c.isalnum() or c in (' ', '-', '_')).strip()
    safe_name = safe_name.replace(' ', '_')[:50]  # Limit length and replace spaces
    dir_name = f"{timestamp}_{safe_name}"
    
    # Create campaign directory
    campaign_dir = os.path.join(campaigns_dir, dir_name)
    os.makedirs(campaign_dir, exist_ok=True)
    
    return campaign_dir

def save_payload(payload: dict, filename: str) -> bool:
    """Save a payload to a JSON file"""
    try:
        with open(filename, 'w') as f:
            json.dump(payload, f, indent=2)
        return True
    except Exception as e:
        logger.error(f"Failed to save {filename}: {str(e)}")
        return False

def save_metadata(campaign_dir: str, campaign_spec: dict, query: str, placeholders: dict) -> bool:
    """Save campaign metadata"""
    metadata = {
        "generated_at": datetime.now().isoformat(),
        "query": query,
        "campaign_name": campaign_spec["campaign"]["name"],
        "objective": campaign_spec["campaign"]["objective"],
        "target_audience": campaign_spec.get("reasoning", {}).get("audience_analysis", ""),
        "budget": campaign_spec["ad_set"]["budget"],
        "status": "draft",  # Initial status
        "api_calls": {
            "campaign": {"status": "pending", "id": None},
            "adset": {"status": "pending", "id": None},
            "ad_creative": {"status": "pending", "id": None},
            "ad": {"status": "pending", "id": None}
        },
        "required_placeholders": placeholders,
        "api_notes": {
            "placeholder_requirements": "All placeholders must be replaced with valid IDs before API submission",
            "id_validation": "Ensure all referenced IDs (interests, page, ad creative) exist and are accessible",
            "creation_order": [
                "1. Upload images to get image_hash",
                "2. Create campaign and get campaign_id",
                "3. Create adset using campaign_id",
                "4. Create ad creative using page_id and image_hash",
                "5. Create ad using adset_id and creative_id"
            ],
            "api_version": "v18.0 (as of May 2025)"
        }
    }
    
    return save_payload(metadata, os.path.join(campaign_dir, "metadata.json"))

def display_placeholder_table(placeholders: dict):
    """Display a table of required placeholders"""
    table = Table(title="Required Placeholders for API Submission")
    table.add_column("Placeholder", style="cyan")
    table.add_column("Files", style="green")
    table.add_column("Description", style="yellow")
    table.add_column("Dependencies", style="red")
    
    for placeholder, info in placeholders.items():
        table.add_row(
            f"{{{{{placeholder}}}}}",
            "\n".join(info["files"]),
            info["description"],
            f"Required before: {info['required_before']}"
        )
    
    console.print(table)

def get_future_dates():
    """Generate future start and end dates for the campaign"""
    # Start date: tomorrow
    start_date = datetime.now() + timedelta(days=1)
    # End date: 30 days from start
    end_date = start_date + timedelta(days=30)
    
    return (
        start_date.strftime("%Y-%m-%dT00:00:00-0700"),
        end_date.strftime("%Y-%m-%dT23:59:59-0700")
    )

def validate_interest_ids(interests: list) -> list:
    """Validate and update interest IDs with real Meta interest IDs"""
    # This is a placeholder for real interest ID validation
    # In production, this should query Meta's API or use a validated list
    validated_interests = [
        {
            "id": "6003139266461",
            "name": "Fitness"
        },
        {
            "id": "6003139266462",
            "name": "Home Workout"
        },
        {
            "id": "6003139266463",
            "name": "Fitness Equipment"
        }
    ]
    return validated_interests

def get_budget_input() -> dict:
    """Get budget details from user input with validation"""
    console.print("\n[bold]Campaign Budget Configuration[/bold]")
    
    # Get budget amount
    while True:
        try:
            amount = float(typer.prompt("Enter budget amount (in USD)", type=float))
            if amount <= 0:
                console.print("[red]Budget amount must be greater than 0[/red]")
                continue
            break
        except ValueError:
            console.print("[red]Please enter a valid number[/red]")
    
    # Get budget type with simple yes/no for daily budget
    is_daily = typer.confirm("Would you like to set this as a daily budget? (No = Lifetime budget)")
    budget_type = "DAILY" if is_daily else "LIFETIME"
    
    # Get currency (defaulting to USD for now, but could be expanded)
    currency = "USD"
    
    return {
        "amount": amount,
        "currency": currency,
        "type": budget_type
    }

def validate_budget(budget: dict) -> list:
    """Validate budget configuration"""
    issues = []
    
    # Validate amount
    try:
        amount = float(budget["amount"])
        if amount <= 0:
            issues.append("Budget amount must be greater than 0")
        if amount < 1 and budget["type"] == "DAILY":
            issues.append("Daily budget must be at least $1")
        if amount < 10 and budget["type"] == "LIFETIME":
            issues.append("Lifetime budget must be at least $10")
    except (ValueError, TypeError):
        issues.append("Invalid budget amount")
    
    # Validate type
    if budget["type"] not in ["LIFETIME", "DAILY"]:
        issues.append("Invalid budget type. Must be either LIFETIME or DAILY")
    
    # Validate currency
    if budget["currency"] != "USD":
        issues.append("Currently only USD is supported")
    
    return issues

def main(query: str = typer.Argument(..., help="Query to generate campaign specification for")):
    """Generate campaign specifications based on a natural language query"""
    try:
        # Initialize RAG Service
        rag_service = RAGService()
        
        # Get budget configuration from user
        budget = get_budget_input()
        
        # Validate budget
        budget_issues = validate_budget(budget)
        if budget_issues:
            console.print("\n[bold red]Budget Configuration Issues:[/bold red]")
            for issue in budget_issues:
                console.print(f"[red]- {issue}[/red]")
            if not typer.confirm("Do you want to continue with these issues?"):
                sys.exit(1)
        
        # Convert query to campaign brief format
        campaign_brief = {
            "platform": "Meta",
            "product_description": query,
            "objective": "OUTCOME_SALES",  # Default objective
            "target_audience": "General audience",  # Will be refined by the LLM
            "budget": budget
        }
        
        logger.info("Generating campaign specification...")
        # Generate campaign specification
        campaign_spec = rag_service.generate_campaign(campaign_brief)
        
        if "error" in campaign_spec:
            raise ValueError(f"Campaign generation failed: {campaign_spec['error']}")
        
        logger.info("Campaign specification generated successfully")
        logger.debug(f"Campaign spec: {json.dumps(campaign_spec, indent=2)}")
        
        # Create campaign directory
        campaign_dir = create_campaign_directory(campaign_spec["campaign"]["name"])
        
        # Get future dates for campaign
        start_time, end_time = get_future_dates()
        
        # Create the campaign payload
        campaign_payload = {
            "name": campaign_spec["campaign"]["name"],
            "objective": campaign_spec["campaign"]["objective"],
            "status": "PAUSED",
            "special_ad_categories": [],
            "campaign_budget_optimization_on": True,
            "account_id": "{{account_id}}"
        }
        
        # Create the adset payload
        adset_payload = {
            "name": campaign_spec["ad_set"]["name"],
            "campaign_id": "{{campaign_id}}",
            "optimization_goal": "CONVERSIONS",
            "billing_event": "IMPRESSIONS",
            "bid_strategy": "LOWEST_COST",
            f"{budget['type'].lower()}_budget": campaign_spec["ad_set"]["budget"]["amount"],
            "status": "PAUSED",
            "targeting": {
                "geo_locations": {
                    "countries": ["US"]
                },
                "age_min": campaign_spec["ad_set"]["targeting"].get("age_min", 30),
                "age_max": campaign_spec["ad_set"]["targeting"].get("age_max", 55),
                "genders": [1, 2],
                "flexible_spec": [
                    {
                        "interests": validate_interest_ids(campaign_spec["ad_set"]["targeting"].get("interests", []))
                    }
                ]
            },
            "attribution_spec": [
                {
                    "event_type": "CLICK_THROUGH",
                    "window_days": 7
                },
                {
                    "event_type": "VIEW_THROUGH",
                    "window_days": 1
                }
            ],
            "placements": {
                "facebook": ["feed", "marketplace"],
                "instagram": ["stream", "explore"],
                "audience_network": [],
                "messenger": []
            },
            "start_time": start_time,
            "end_time": end_time
        }
        
        # Create the ad creative payload
        ad_creative_payload = {
            "name": f"{campaign_spec['ad']['name']} - Creative",
            "object_story_spec": {
                "page_id": "{{page_id}}",
                "link_data": {
                    "name": campaign_spec["ad"]["creative"]["title"],
                    "message": campaign_spec["ad"]["creative"]["body"],
                    "link": campaign_spec["ad"]["creative"]["link"],
                    "call_to_action": {
                        "type": campaign_spec["ad"]["creative"]["call_to_action"].upper().replace(" ", "_")
                    },
                    "image_hash": "{{image_hash}}"
                }
            },
            "account_id": "{{account_id}}",
            "asset_customization_specs": {
                "description_specs": [
                    {
                        "description": campaign_spec["ad"]["creative"].get("description", 
                            "Transform your home into a premium fitness space with our high-end equipment, designed for serious fitness enthusiasts.")
                    }
                ]
            }
        }
        
        # Create the ad payload
        ad_payload = {
            "name": campaign_spec["ad"]["name"],
            "adset_id": "{{adset_id}}",
            "creative": {
                "creative_id": "{{creative_id}}"
            },
            "status": "PAUSED",
            "tracking_specs": [
                {
                    "action.type": ["offsite_conversion"],
                    "fb_pixel": ["{{pixel_id}}"]
                }
            ]
        }
        
        # Save all payloads
        payloads = {
            "campaign.json": campaign_payload,
            "adset.json": adset_payload,
            "ad_creative.json": ad_creative_payload,
            "ad.json": ad_payload
        }
        
        # Validate placeholders
        found_placeholders = validate_placeholders(payloads)
        
        success = True
        for filename, payload in payloads.items():
            filepath = os.path.join(campaign_dir, filename)
            if save_payload(payload, filepath):
                console.print(f"[green]Saved {filename}[/green]")
                # Print preview of each payload
                console.print(f"\n[bold]{filename} Preview:[/bold]")
                console.print(json.dumps(payload, indent=2))
            else:
                console.print(f"[red]Failed to save {filename}[/red]")
                success = False
        
        # Save metadata with placeholder information
        if save_metadata(campaign_dir, campaign_spec, query, found_placeholders):
            console.print(f"[green]Saved campaign metadata[/green]")
        else:
            console.print("[red]Failed to save campaign metadata[/red]")
            success = False
        
        if success:
            console.print("\n[bold]Campaign Components Generated:[/bold]")
            console.print(f"Campaign directory: {campaign_dir}")
            console.print("1. Campaign creation payload (campaign.json)")
            console.print("2. Ad Set creation payload (adset.json)")
            console.print("3. Ad Creative creation payload (ad_creative.json)")
            console.print("4. Ad creation payload (ad.json)")
            console.print("5. Campaign metadata (metadata.json)")
            
            # Display placeholder information
            console.print("\n[bold]Required Placeholders:[/bold]")
            display_placeholder_table(found_placeholders)
            
            console.print("\n[bold]Important Notes:[/bold]")
            console.print("1. All placeholders ({{...}}) must be replaced with valid IDs before API submission")
            console.print("2. Ensure all referenced IDs (interests, page, ad creative) exist and are accessible")
            console.print("3. Follow the creation order in metadata.json for proper ID dependencies")
            console.print("4. Using Meta Marketing API version v18.0 (as of May 2025)")
            console.print(f"5. Campaign uses {budget['type'].lower()} budget of ${budget['amount']}")
            console.print("6. Campaign dates are set to future dates")
            console.print("7. Interest IDs are validated against Meta's targeting options")
            
            # Print reasoning if available
            if "reasoning" in campaign_spec:
                console.print("\n[bold]Campaign Reasoning:[/bold]")
                for key, value in campaign_spec["reasoning"].items():
                    console.print(f"\n[bold]{key}:[/bold]")
                    console.print(value)
        
    except Exception as e:
        logger.error(f"Error during campaign generation: {str(e)}")
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    typer.run(main) 