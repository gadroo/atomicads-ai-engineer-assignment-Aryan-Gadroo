(venv) (base) beehoney413@Winston atomicads-ai-engineer-assignment-Aryan-Gadro                              % ./run_query.sh "Generate a Meta ad campaign for a high-end fitness equipment brand targeting fitness enthusiasts aged 28-50 interested in home workouts and prem./run_query.sh "Generate a Meta ad campaign for a high-end fitness equipment brand targeting fitness enthusiasts aged 28-50 interested in home workouts and premium fitness gear"
2025-05-11 18:36:19,143 - src.database.vector_store - INFO - Successfully connected to Pinecone index: ad-campaign-knowledge

Campaign Budget Configuration
Enter budget amount (in USD): 100
Would you like to set this as a daily budget? (No = Lifetime budget) [y/N]: Y
2025-05-11 18:36:31,173 - __main__ - INFO - Generating campaign specification...
2025-05-11 18:36:34,210 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
2025-05-11 18:36:52,266 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2025-05-11 18:36:52,276 - __main__ - INFO - Campaign specification generated successfully
Saved campaign.json

campaign.json Preview:
{
  "name": "High-End Fitness Equipment Sales Campaign",
  "objective": "OUTCOME_SALES",
  "status": "PAUSED",
  "special_ad_categories": [],
  "campaign_budget_optimization_on": true,
  "account_id": "{{account_id}}"
}
Saved adset.json

adset.json Preview:
{
  "name": "Fitness Enthusiasts Targeting",
  "campaign_id": "{{campaign_id}}",
  "optimization_goal": "CONVERSIONS",
  "billing_event": "IMPRESSIONS",
  "bid_strategy": "LOWEST_COST",
  "daily_budget": 100.0,
  "status": "PAUSED",
  "targeting": {
    "geo_locations": {
      "countries": [
        "US"
      ]
    },
    "age_min": 28,
    "age_max": 50,
    "genders": [
      1,
      2
    ],
    "flexible_spec": [
      {
        "interests": [
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
    "facebook": [
      "feed",
      "marketplace"
    ],
    "instagram": [
      "stream",
      "explore"
    ],
    "audience_network": [],
    "messenger": []
  },
  "start_time": "2025-05-12T00:00:00-0700",
  "end_time": "2025-06-11T23:59:59-0700"
}
Saved ad_creative.json

ad_creative.json Preview:
{
  "name": "Premium Fitness Gear Ad - Creative",
  "object_story_spec": {
    "page_id": "{{page_id}}",
    "link_data": {
      "name": "Elevate Your Home Workouts",
      "message": "Discover our high-end fitness equipment designed for serious fitness enthusiasts. 
Transform your home into a premium workout space!",
      "link": "https://www.highendfitness.com/shop",
      "call_to_action": {
        "type": "SHOP_NOW"
      },
      "image_hash": "{{image_hash}}"
    }
  },
  "account_id": "{{account_id}}",
  "asset_customization_specs": {
    "description_specs": [
      {
        "description": "Transform your home into a premium fitness space with our high-end equipment, 
designed for serious fitness enthusiasts."
      }
    ]
  }
}
Saved ad.json

ad.json Preview:
{
  "name": "Premium Fitness Gear Ad",
  "adset_id": "{{adset_id}}",
  "creative": {
    "creative_id": "{{creative_id}}"
  },
  "status": "PAUSED",
  "tracking_specs": [
    {
      "action.type": [
        "offsite_conversion"
      ],
      "fb_pixel": [
        "{{pixel_id}}"
      ]
    }
  ]
}
Saved campaign metadata

Campaign Components Generated:
Campaign directory: 
/Users/beehoney413/Desktop/atomicads-ai-engineer-assignment-Aryan-Gadroo/scripts/../campaigns/20250511_18365
2_High-End_Fitness_Equipment_Sales_Campaign
1. Campaign creation payload (campaign.json)
2. Ad Set creation payload (adset.json)
3. Ad Creative creation payload (ad_creative.json)
4. Ad creation payload (ad.json)
5. Campaign metadata (metadata.json)

Required Placeholders:
                                  Required Placeholders for API Submission                                  
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Placeholder     ┃ Files            ┃ Description                    ┃ Dependencies                       ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ {{account_id}}  │ campaign.json    │ Account ID for API submission  │ Required before: any API calls     │
│                 │ ad_creative.json │                                │                                    │
│ {{campaign_id}} │ adset.json       │ ID of the created campaign     │ Required before: adset creation    │
│ {{page_id}}     │ ad_creative.json │ ID of the Facebook Page        │ Required before: creative creation │
│ {{image_hash}}  │ ad_creative.json │ Hash of uploaded image         │ Required before: creative creation │
│ {{adset_id}}    │ ad.json          │ ID of the created adset        │ Required before: ad creation       │
│ {{creative_id}} │ ad.json          │ ID of the created ad creative  │ Required before: ad creation       │
│ {{pixel_id}}    │ ad.json          │ Facebook Pixel ID for tracking │ Required before: ad creation       │
└─────────────────┴──────────────────┴────────────────────────────────┴────────────────────────────────────┘

Important Notes:
1. All placeholders ({{...}}) must be replaced with valid IDs before API submission
2. Ensure all referenced IDs (interests, page, ad creative) exist and are accessible
3. Follow the creation order in metadata.json for proper ID dependencies
4. Using Meta Marketing API version v18.0 (as of May 2025)
5. Campaign uses daily budget of $100.0
6. Campaign dates are set to future dates
7. Interest IDs are validated against Meta's targeting options

Campaign Reasoning:

audience_analysis:
Targeting fitness enthusiasts aged 28-50 aligns with the demographic that typically invests in premium 
fitness gear for home workouts.

creative_strategy:
The ad copy emphasizes the transformation of home workouts with high-end equipment, appealing to the target 
audience's desire for quality and effectiveness.

budget_rationale:
A daily budget of $100 is reasonable for testing the campaign's effectiveness and aligns with industry 
benchmarks for sales-focused campaigns.

expected_performance:
With a well-defined target audience and compelling ad creative, we expect a strong conversion rate from 
users interested in premium fitness gear.

documentation_references:
[
    'Meta Ads Best Practices - Campaign Objectives',
    'Meta Ads Best Practices - Audience Size and Targeting',
    'Meta Ads Best Practices - Budget Optimization'
]