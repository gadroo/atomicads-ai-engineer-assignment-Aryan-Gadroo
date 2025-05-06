import logging
from typing import Dict, Any, List, Tuple, Optional
import json

logger = logging.getLogger(__name__)

class CampaignValidator:
    """Validator for Meta Ads campaign specifications."""
    
    # Meta Ads character limits
    CHARACTER_LIMITS = {
        "campaign_name": 255,
        "ad_set_name": 255,
        "ad_name": 255,
        "ad_title": 125,
        "ad_body": 500,
        "image_description": 200,
    }
    
    # Valid campaign objectives for Meta Ads
    VALID_OBJECTIVES = [
        "OUTCOME_AWARENESS", 
        "OUTCOME_ENGAGEMENT", 
        "OUTCOME_SALES", 
        "OUTCOME_LEAD_GENERATION", 
        "OUTCOME_APP_PROMOTION", 
        "OUTCOME_TRAFFIC"
    ]
    
    # Valid optimization goals by objective
    VALID_OPTIMIZATION_GOALS = {
        "OUTCOME_AWARENESS": ["AD_RECALL_LIFT", "IMPRESSIONS", "REACH"],
        "OUTCOME_ENGAGEMENT": ["LINK_CLICKS", "POST_ENGAGEMENT", "VIDEO_VIEWS"],
        "OUTCOME_SALES": ["OFFSITE_CONVERSIONS", "VALUE", "OMNI_SALES", "STORE_VISITS"],
        "OUTCOME_LEAD_GENERATION": ["LEAD_GENERATION", "LINK_CLICKS"],
        "OUTCOME_APP_PROMOTION": ["APP_INSTALLS", "LINK_CLICKS", "APP_EVENTS", "VALUE"],
        "OUTCOME_TRAFFIC": ["LINK_CLICKS", "LANDING_PAGE_VIEWS", "IMPRESSIONS", "REACH"]
    }
    
    # Valid billing events
    VALID_BILLING_EVENTS = ["IMPRESSIONS", "LINK_CLICKS", "APP_INSTALLS", "OFFER_CLAIMS", "PAGE_LIKES", "POST_ENGAGEMENT"]
    
    # Valid bid strategies
    VALID_BID_STRATEGIES = ["LOWEST_COST_WITHOUT_CAP", "LOWEST_COST_WITH_BID_CAP", "TARGET_COST", "COST_CAP"]
    
    # Valid call to action types
    VALID_CTA_TYPES = [
        "BOOK_TRAVEL", "DONATE", "DOWNLOAD", "GET_OFFER", "GET_QUOTE", "LEARN_MORE",
        "LISTEN_MUSIC", "MESSAGE_PAGE", "NO_BUTTON", "OPEN_LINK", "ORDER_NOW", "PLAY_GAME",
        "SHOP_NOW", "SIGN_UP", "SUBSCRIBE", "USE_APP", "WATCH_MORE", "WATCH_VIDEO"
    ]
    
    # Minimum daily budget in cents
    MINIMUM_DAILY_BUDGET = 100
    
    @classmethod
    def validate_campaign_specification(cls, campaign_spec: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """Validate a complete campaign specification.
        
        Args:
            campaign_spec: The campaign specification to validate
            
        Returns:
            Tuple[bool, Dict[str, Any]]: (is_valid, validation_results)
        """
        issues = []
        missing_fields = []
        
        # Validate campaign structure
        cls._validate_required_sections(campaign_spec, ["campaign", "ad_set", "ad"], missing_fields)
        
        if missing_fields:
            return False, {
                "is_valid": False,
                "missing_required_sections": missing_fields,
                "issues": ["Missing required top-level sections in campaign specification"]
            }
        
        # Validate campaign fields
        campaign_issues = cls._validate_campaign(campaign_spec["campaign"])
        issues.extend(campaign_issues)
        
        # Validate ad set fields
        ad_set_issues = cls._validate_ad_set(campaign_spec["ad_set"], campaign_spec["campaign"].get("objective"))
        issues.extend(ad_set_issues)
        
        # Validate ad fields
        ad_issues = cls._validate_ad(campaign_spec["ad"])
        issues.extend(ad_issues)
        
        # Validate cross-section relationships
        relationship_issues = cls._validate_cross_section_relationships(campaign_spec)
        issues.extend(relationship_issues)
        
        # Return validation results
        is_valid = len(issues) == 0
        
        return is_valid, {
            "is_valid": is_valid,
            "issues": issues
        }
    
    @classmethod
    def _validate_required_sections(cls, data: Dict[str, Any], required_sections: List[str], 
                                   missing_fields: List[str]) -> None:
        """Validate that required sections exist in the data.
        
        Args:
            data: The data to validate
            required_sections: List of required section names
            missing_fields: List to add missing fields to
        """
        for section in required_sections:
            if section not in data:
                missing_fields.append(section)
    
    @classmethod
    def _validate_required_fields(cls, data: Dict[str, Any], required_fields: List[str], 
                                 section: str, missing_fields: List[str]) -> None:
        """Validate that required fields exist in the data.
        
        Args:
            data: The data to validate
            required_fields: List of required field names
            section: Section name for error messages
            missing_fields: List to add missing fields to
        """
        for field in required_fields:
            if field not in data:
                missing_fields.append(f"{section}.{field}")
    
    @classmethod
    def _validate_campaign(cls, campaign: Dict[str, Any]) -> List[str]:
        """Validate campaign section.
        
        Args:
            campaign: Campaign data to validate
            
        Returns:
            List[str]: List of validation issues
        """
        issues = []
        missing_fields = []
        
        # Check required fields
        required_fields = ["name", "objective", "status"]
        cls._validate_required_fields(campaign, required_fields, "campaign", missing_fields)
        
        if missing_fields:
            issues.append(f"Missing required campaign fields: {', '.join(missing_fields)}")
            return issues
        
        # Validate campaign name length
        if len(campaign["name"]) > cls.CHARACTER_LIMITS["campaign_name"]:
            issues.append(f"Campaign name exceeds maximum length of {cls.CHARACTER_LIMITS['campaign_name']} characters")
        
        # Validate objective
        if campaign["objective"] not in cls.VALID_OBJECTIVES:
            issues.append(f"Invalid campaign objective: {campaign['objective']}. Must be one of: {', '.join(cls.VALID_OBJECTIVES)}")
        
        # Validate status
        if campaign["status"] not in ["ACTIVE", "PAUSED", "DELETED", "ARCHIVED"]:
            issues.append(f"Invalid campaign status: {campaign['status']}. Must be one of: ACTIVE, PAUSED, DELETED, ARCHIVED")
        
        return issues
    
    @classmethod
    def _validate_ad_set(cls, ad_set: Dict[str, Any], campaign_objective: Optional[str] = None) -> List[str]:
        """Validate ad set section.
        
        Args:
            ad_set: Ad set data to validate
            campaign_objective: Optional campaign objective for cross-validation
            
        Returns:
            List[str]: List of validation issues
        """
        issues = []
        missing_fields = []
        
        # Check required fields
        required_fields = ["name", "optimization_goal", "billing_event", "bid_strategy", "budget", "targeting"]
        cls._validate_required_fields(ad_set, required_fields, "ad_set", missing_fields)
        
        if missing_fields:
            issues.append(f"Missing required ad set fields: {', '.join(missing_fields)}")
            return issues
        
        # Validate ad set name length
        if len(ad_set["name"]) > cls.CHARACTER_LIMITS["ad_set_name"]:
            issues.append(f"Ad set name exceeds maximum length of {cls.CHARACTER_LIMITS['ad_set_name']} characters")
        
        # Validate optimization goal
        if campaign_objective and ad_set["optimization_goal"] not in cls.VALID_OPTIMIZATION_GOALS.get(campaign_objective, []):
            issues.append(f"Invalid optimization goal '{ad_set['optimization_goal']}' for campaign objective '{campaign_objective}'")
        
        # Validate billing event
        if ad_set["billing_event"] not in cls.VALID_BILLING_EVENTS:
            issues.append(f"Invalid billing event: {ad_set['billing_event']}. Must be one of: {', '.join(cls.VALID_BILLING_EVENTS)}")
        
        # Validate bid strategy
        if ad_set["bid_strategy"] not in cls.VALID_BID_STRATEGIES:
            issues.append(f"Invalid bid strategy: {ad_set['bid_strategy']}. Must be one of: {', '.join(cls.VALID_BID_STRATEGIES)}")
        
        # Validate budget
        budget_issues = cls._validate_budget(ad_set["budget"])
        issues.extend(budget_issues)
        
        # Validate targeting
        targeting_issues = cls._validate_targeting(ad_set["targeting"])
        issues.extend(targeting_issues)
        
        # Validate schedule if present
        if "schedule" in ad_set:
            schedule_issues = cls._validate_schedule(ad_set["schedule"])
            issues.extend(schedule_issues)
        
        return issues
    
    @classmethod
    def _validate_budget(cls, budget: Dict[str, Any]) -> List[str]:
        """Validate budget configuration.
        
        Args:
            budget: Budget data to validate
            
        Returns:
            List[str]: List of validation issues
        """
        issues = []
        missing_fields = []
        
        # Check required fields
        required_fields = ["amount", "type"]
        cls._validate_required_fields(budget, required_fields, "budget", missing_fields)
        
        if missing_fields:
            issues.append(f"Missing required budget fields: {', '.join(missing_fields)}")
            return issues
        
        # Validate budget type
        if budget["type"] not in ["daily", "lifetime"]:
            issues.append(f"Invalid budget type: {budget['type']}. Must be one of: daily, lifetime")
        
        # Validate budget amount
        try:
            amount = float(budget["amount"])
            if amount < cls.MINIMUM_DAILY_BUDGET:
                issues.append(f"Budget amount must be at least {cls.MINIMUM_DAILY_BUDGET} cents")
        except (ValueError, TypeError):
            issues.append(f"Invalid budget amount: {budget['amount']}. Must be a number")
        
        return issues
    
    @classmethod
    def _validate_targeting(cls, targeting: Dict[str, Any]) -> List[str]:
        """Validate targeting configuration.
        
        Args:
            targeting: Targeting data to validate
            
        Returns:
            List[str]: List of validation issues
        """
        issues = []
        
        # Check for geo_locations (required)
        if "geo_locations" not in targeting:
            issues.append("Missing required targeting field: geo_locations")
            return issues
        
        # Validate age range if specified
        if "age_min" in targeting and "age_max" in targeting:
            try:
                age_min = int(targeting["age_min"])
                age_max = int(targeting["age_max"])
                
                if age_min < 13:
                    issues.append("Minimum age cannot be less than 13")
                
                if age_max > 65:
                    issues.append("Maximum age cannot be greater than 65")
                
                if age_min > age_max:
                    issues.append("Minimum age cannot be greater than maximum age")
            except (ValueError, TypeError):
                issues.append("Age values must be integers")
        
        # Validate gender values if specified
        if "genders" in targeting:
            valid_genders = [1, 2]  # 1 = male, 2 = female
            for gender in targeting["genders"]:
                if gender not in valid_genders:
                    issues.append(f"Invalid gender value: {gender}. Must be one of: {valid_genders}")
        
        return issues
    
    @classmethod
    def _validate_schedule(cls, schedule: Dict[str, Any]) -> List[str]:
        """Validate schedule configuration.
        
        Args:
            schedule: Schedule data to validate
            
        Returns:
            List[str]: List of validation issues
        """
        issues = []
        
        # Check start and end times
        if "start_time" in schedule and "end_time" in schedule:
            start_time = schedule["start_time"]
            end_time = schedule["end_time"]
            
            # Simplified validation - in practice would use datetime parsing
            if start_time >= end_time:
                issues.append("Start time must be before end time")
        
        return issues
    
    @classmethod
    def _validate_ad(cls, ad: Dict[str, Any]) -> List[str]:
        """Validate ad section.
        
        Args:
            ad: Ad data to validate
            
        Returns:
            List[str]: List of validation issues
        """
        issues = []
        missing_fields = []
        
        # Check required fields
        required_fields = ["name", "creative"]
        cls._validate_required_fields(ad, required_fields, "ad", missing_fields)
        
        if missing_fields:
            issues.append(f"Missing required ad fields: {', '.join(missing_fields)}")
            return issues
        
        # Validate ad name length
        if len(ad["name"]) > cls.CHARACTER_LIMITS["ad_name"]:
            issues.append(f"Ad name exceeds maximum length of {cls.CHARACTER_LIMITS['ad_name']} characters")
        
        # Validate creative
        creative_issues = cls._validate_creative(ad["creative"])
        issues.extend(creative_issues)
        
        return issues
    
    @classmethod
    def _validate_creative(cls, creative: Dict[str, Any]) -> List[str]:
        """Validate creative configuration.
        
        Args:
            creative: Creative data to validate
            
        Returns:
            List[str]: List of validation issues
        """
        issues = []
        missing_fields = []
        
        # Check required fields
        required_fields = ["title", "body", "call_to_action", "link"]
        cls._validate_required_fields(creative, required_fields, "creative", missing_fields)
        
        if missing_fields:
            issues.append(f"Missing required creative fields: {', '.join(missing_fields)}")
            return issues
        
        # Validate text lengths
        if len(creative["title"]) > cls.CHARACTER_LIMITS["ad_title"]:
            issues.append(f"Ad title exceeds maximum length of {cls.CHARACTER_LIMITS['ad_title']} characters")
        
        if len(creative["body"]) > cls.CHARACTER_LIMITS["ad_body"]:
            issues.append(f"Ad body exceeds maximum length of {cls.CHARACTER_LIMITS['ad_body']} characters")
        
        if "image_description" in creative and len(creative["image_description"]) > cls.CHARACTER_LIMITS["image_description"]:
            issues.append(f"Image description exceeds maximum length of {cls.CHARACTER_LIMITS['image_description']} characters")
        
        # Validate call to action
        if creative["call_to_action"] not in cls.VALID_CTA_TYPES:
            issues.append(f"Invalid call to action: {creative['call_to_action']}. Must be one of: {', '.join(cls.VALID_CTA_TYPES)}")
        
        # Simple URL validation
        if not creative["link"].startswith(("http://", "https://")):
            issues.append("Link URL must start with http:// or https://")
        
        return issues
    
    @classmethod
    def _validate_cross_section_relationships(cls, campaign_spec: Dict[str, Any]) -> List[str]:
        """Validate relationships between different sections.
        
        Args:
            campaign_spec: Complete campaign specification
            
        Returns:
            List[str]: List of validation issues
        """
        issues = []
        
        # Check that optimization goal is compatible with campaign objective
        if "campaign" in campaign_spec and "objective" in campaign_spec["campaign"] and "ad_set" in campaign_spec and "optimization_goal" in campaign_spec["ad_set"]:
            objective = campaign_spec["campaign"]["objective"]
            optimization_goal = campaign_spec["ad_set"]["optimization_goal"]
            
            if objective in cls.VALID_OPTIMIZATION_GOALS and optimization_goal not in cls.VALID_OPTIMIZATION_GOALS[objective]:
                issues.append(f"Optimization goal '{optimization_goal}' is not compatible with campaign objective '{objective}'")
        
        return issues 