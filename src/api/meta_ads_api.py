import logging
import time
from typing import Dict, Any, List, Optional
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.ad import Ad
from facebook_business.exceptions import FacebookRequestError

from src.config.config import config

logger = logging.getLogger(__name__)

class MetaAdsAPI:
    def __init__(self):
        """Initialize the Meta Ads API client."""
        try:
            # Initialize the Facebook Ads API
            FacebookAdsApi.init(
                app_id=config.meta_ads.app_id,
                app_secret=config.meta_ads.app_secret,
                access_token=config.meta_ads.access_token
            )
            
            # Set up the Ad Account object
            self.ad_account = AdAccount(f'act_{config.meta_ads.ad_account_id}')
            
            logger.info(f"Meta Ads API initialized for account: {config.meta_ads.ad_account_id}")
        except Exception as e:
            logger.error(f"Failed to initialize Meta Ads API: {str(e)}")
            raise
    
    def create_campaign(self, campaign_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Create a campaign in Meta Ads.
        
        Args:
            campaign_spec: Campaign specification dictionary
            
        Returns:
            Dict[str, Any]: Response with campaign ID or error
        """
        try:
            campaign_data = campaign_spec["campaign"]
            
            # Prepare params for campaign creation
            params = {
                'name': campaign_data["name"],
                'objective': campaign_data["objective"],
                'status': campaign_data["status"],
                'special_ad_categories': campaign_data.get("special_ad_categories", []),
            }
            
            # Add optional campaign budget optimization if enabled
            if campaign_data.get("budget_optimization", False):
                params['daily_budget'] = campaign_spec["ad_set"]["budget"]["amount"]
            
            # Create the campaign
            campaign = self.ad_account.create_campaign(params=params)
            
            logger.info(f"Campaign created with ID: {campaign['id']}")
            
            # Return campaign ID and response
            return {
                "success": True,
                "campaign_id": campaign["id"],
                "data": campaign
            }
        except FacebookRequestError as e:
            logger.error(f"Facebook API error creating campaign: {e.api_error_code()}: {e.api_error_message()}")
            return {
                "success": False,
                "error_code": e.api_error_code(),
                "error_message": e.api_error_message(),
                "error_type": e.api_error_type(),
                "error_subcode": e.api_error_subcode()
            }
        except Exception as e:
            logger.error(f"Error creating campaign: {str(e)}")
            return {
                "success": False,
                "error_message": str(e)
            }
    
    def create_ad_set(self, campaign_id: str, campaign_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Create an ad set in Meta Ads.
        
        Args:
            campaign_id: ID of the parent campaign
            campaign_spec: Campaign specification dictionary
            
        Returns:
            Dict[str, Any]: Response with ad set ID or error
        """
        try:
            ad_set_data = campaign_spec["ad_set"]
            
            # Prepare targeting specs
            targeting = ad_set_data["targeting"]
            
            # Prepare params for ad set creation
            params = {
                'name': ad_set_data["name"],
                'campaign_id': campaign_id,
                'optimization_goal': ad_set_data["optimization_goal"],
                'billing_event': ad_set_data["billing_event"],
                'bid_strategy': ad_set_data["bid_strategy"],
                'targeting': targeting,
                'status': campaign_spec["campaign"]["status"],
            }
            
            # Add budget if not using campaign budget optimization
            if not campaign_spec["campaign"].get("budget_optimization", False):
                budget_data = ad_set_data["budget"]
                budget_type = budget_data["type"]
                
                if budget_type == "daily":
                    params['daily_budget'] = budget_data["amount"]
                elif budget_type == "lifetime":
                    params['lifetime_budget'] = budget_data["amount"]
            
            # Add scheduling if provided
            if "schedule" in ad_set_data:
                schedule = ad_set_data["schedule"]
                if "start_time" in schedule:
                    params['start_time'] = schedule["start_time"]
                if "end_time" in schedule:
                    params['end_time'] = schedule["end_time"]
            
            # Create the ad set
            ad_set = self.ad_account.create_ad_set(params=params)
            
            logger.info(f"Ad Set created with ID: {ad_set['id']}")
            
            # Return ad set ID and response
            return {
                "success": True,
                "ad_set_id": ad_set["id"],
                "data": ad_set
            }
        except FacebookRequestError as e:
            logger.error(f"Facebook API error creating ad set: {e.api_error_code()}: {e.api_error_message()}")
            return {
                "success": False,
                "error_code": e.api_error_code(),
                "error_message": e.api_error_message(),
                "error_type": e.api_error_type(),
                "error_subcode": e.api_error_subcode()
            }
        except Exception as e:
            logger.error(f"Error creating ad set: {str(e)}")
            return {
                "success": False,
                "error_message": str(e)
            }
    
    def create_ad(self, ad_set_id: str, campaign_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Create an ad in Meta Ads.
        
        Args:
            ad_set_id: ID of the parent ad set
            campaign_spec: Campaign specification dictionary
            
        Returns:
            Dict[str, Any]: Response with ad ID or error
        """
        try:
            ad_data = campaign_spec["ad"]
            creative_data = ad_data["creative"]
            
            # Create a creative first (for demonstration, using a simple link ad)
            creative_params = {
                'name': f"{ad_data['name']} Creative",
                'title': creative_data["title"],
                'body': creative_data["body"],
                'link': creative_data["link"],
                'call_to_action_type': creative_data["call_to_action"],
                'object_story_spec': {
                    'page_id': config.meta_ads.business_id,
                    'link_data': {
                        'message': creative_data["body"],
                        'link': creative_data["link"],
                        'caption': creative_data.get("caption", ""),
                        'description': creative_data.get("image_description", ""),
                        'call_to_action': {
                            'type': creative_data["call_to_action"],
                            'value': {'link': creative_data["link"]}
                        }
                    }
                }
            }
            
            creative = self.ad_account.create_ad_creative(params=creative_params)
            
            # Create the ad
            ad_params = {
                'name': ad_data["name"],
                'adset_id': ad_set_id,
                'creative': {'creative_id': creative["id"]},
                'status': campaign_spec["campaign"]["status"]
            }
            
            ad = self.ad_account.create_ad(params=ad_params)
            
            logger.info(f"Ad created with ID: {ad['id']}")
            
            # Return ad ID and response
            return {
                "success": True,
                "ad_id": ad["id"],
                "creative_id": creative["id"],
                "data": ad
            }
        except FacebookRequestError as e:
            logger.error(f"Facebook API error creating ad: {e.api_error_code()}: {e.api_error_message()}")
            return {
                "success": False,
                "error_code": e.api_error_code(),
                "error_message": e.api_error_message(),
                "error_type": e.api_error_type(),
                "error_subcode": e.api_error_subcode()
            }
        except Exception as e:
            logger.error(f"Error creating ad: {str(e)}")
            return {
                "success": False,
                "error_message": str(e)
            }
    
    def create_full_campaign(self, campaign_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Create a full campaign structure (campaign, ad set, ad).
        
        Args:
            campaign_spec: Complete campaign specification dictionary
            
        Returns:
            Dict[str, Any]: Response with all IDs or error information
        """
        try:
            # Step 1: Create Campaign
            campaign_response = self.create_campaign(campaign_spec)
            
            if not campaign_response["success"]:
                return {
                    "success": False,
                    "stage": "campaign",
                    "error": campaign_response
                }
            
            campaign_id = campaign_response["campaign_id"]
            
            # Wait briefly to ensure campaign creation is processed
            time.sleep(2)
            
            # Step 2: Create Ad Set
            ad_set_response = self.create_ad_set(campaign_id, campaign_spec)
            
            if not ad_set_response["success"]:
                return {
                    "success": False,
                    "stage": "ad_set",
                    "campaign_id": campaign_id,
                    "error": ad_set_response
                }
            
            ad_set_id = ad_set_response["ad_set_id"]
            
            # Wait briefly to ensure ad set creation is processed
            time.sleep(2)
            
            # Step 3: Create Ad
            ad_response = self.create_ad(ad_set_id, campaign_spec)
            
            if not ad_response["success"]:
                return {
                    "success": False,
                    "stage": "ad",
                    "campaign_id": campaign_id,
                    "ad_set_id": ad_set_id,
                    "error": ad_response
                }
            
            # Return success response with all IDs
            return {
                "success": True,
                "campaign_id": campaign_id,
                "ad_set_id": ad_set_id,
                "ad_id": ad_response["ad_id"],
                "creative_id": ad_response["creative_id"]
            }
        except Exception as e:
            logger.error(f"Error in campaign creation pipeline: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            } 