"""
Documentation search and access tools for internal knowledge bases
Following ADK patterns for tool implementation
"""

import json
import os
import sys
from typing import Dict, List


from new_hire.database.db_loader import DatabaseLoader

# Initialize database loader
loader = DatabaseLoader()

def search_documentation(query: str, doc_type: str = "all") -> dict:
    """Search through all internal documentation for relevant information.
    
    Args:
        query: Search term or topic (e.g., "API authentication", "deployment process")
        doc_type: Type of documentation - "wiki", "api", "tutorial", "all" (default: "all")
    
    Returns:
        Dict: Search results from multiple documentation sources
    """
    try:
        results = {
            "status": "success",
            "query": query,
            "wiki_results": [],
            "api_results": [],
            "tutorial_results": [],
            "total_found": 0
        }
        
        query_lower = query.lower()
        
        # Search wiki pages if requested
        if doc_type in ["all", "wiki"]:
            wiki_data = loader.load_data("documentation/wiki_pages.json")
            for page in wiki_data.get("pages", []):
                if (query_lower in page.get("title", "").lower() or
                    query_lower in page.get("content", "").lower() or
                    any(query_lower in tag.lower() for tag in page.get("tags", []))):
                    results["wiki_results"].append({
                        "title": page.get("title", ""),
                        "url": page.get("url", ""),
                        "summary": page.get("summary", ""),
                        "last_updated": page.get("last_updated", ""),
                        "author": page.get("author", ""),
                        "tags": page.get("tags", [])
                    })
        
        # Search API documentation if requested
        if doc_type in ["all", "api"]:
            api_data = loader.load_data("documentation/api_docs.json")
            for api in api_data.get("apis", []):
                if (query_lower in api.get("name", "").lower() or
                    query_lower in api.get("description", "").lower()):
                    results["api_results"].append({
                        "name": api.get("name", ""),
                        "description": api.get("description", ""),
                        "version": api.get("version", ""),
                        "base_url": api.get("base_url", ""),
                        "documentation_url": api.get("documentation_url", ""),
                        "key_endpoints": api.get("key_endpoints", [])
                    })
        
        # Search tutorials if requested
        if doc_type in ["all", "tutorial"]:
            tutorial_data = loader.load_data("documentation/tutorials.json")
            for tutorial in tutorial_data.get("tutorials", []):
                if (query_lower in tutorial.get("title", "").lower() or
                    query_lower in tutorial.get("description", "").lower() or
                    any(query_lower in topic.lower() for topic in tutorial.get("topics", []))):
                    results["tutorial_results"].append({
                        "title": tutorial.get("title", ""),
                        "description": tutorial.get("description", ""),
                        "difficulty": tutorial.get("difficulty", ""),
                        "estimated_time": tutorial.get("estimated_time", ""),
                        "url": tutorial.get("url", ""),
                        "topics": tutorial.get("topics", [])
                    })
        
        # Calculate total results
        results["total_found"] = (len(results["wiki_results"]) +
                                  len(results["api_results"]) +
                                  len(results["tutorial_results"]))
        
        return results
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to search documentation: {str(e)}"
        }

def find_wiki_content(topic: str) -> dict:
    """Find specific wiki pages and content for a given topic.
    
    Args:
        topic: Specific topic to find wiki content for (e.g., "authentication", "deployment")
    
    Returns:
        Dict: Detailed wiki content and related pages
    """
    try:
        wiki_data = loader.load_data("documentation/wiki_pages.json")
        topic_lower = topic.lower()
        main_pages = []
        related_pages = []
        
        for page in wiki_data.get("pages", []):
            relevance_score = 0
            
            # Check title match (highest priority)
            if topic_lower in page.get("title", "").lower():
                relevance_score += 3
            
            # Check content match
            if topic_lower in page.get("content", "").lower():
                relevance_score += 2
            
            # Check tags match
            if any(topic_lower in tag.lower() for tag in page.get("tags", [])):
                relevance_score += 1
            
            page_info = {
                "title": page.get("title", ""),
                "url": page.get("url", ""),
                "summary": page.get("summary", ""),
                "content": page.get("content", "")[:500] + "..." if len(page.get("content", "")) > 500 else page.get("content", ""),
                "last_updated": page.get("last_updated", ""),
                "author": page.get("author", ""),
                "tags": page.get("tags", []),
                "relevance_score": relevance_score
            }
            
            if relevance_score >= 3:
                main_pages.append(page_info)
            elif relevance_score > 0:
                related_pages.append(page_info)
        
        # Sort by relevance
        main_pages.sort(key=lambda x: x["relevance_score"], reverse=True)
        related_pages.sort(key=lambda x: x["relevance_score"], reverse=True)
        
        return {
            "status": "success",
            "topic": topic,
            "main_pages": main_pages[:3],  # Top 3 most relevant
            "related_pages": related_pages[:5],  # Top 5 related
            "total_pages_found": len(main_pages) + len(related_pages)
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to find wiki content: {str(e)}"
        }

def get_api_docs(api_name: str = "", endpoint: str = "") -> dict:
    """Get detailed API documentation and endpoint information.
    
    Args:
        api_name: Name of the API service (e.g., "auth-service", "payment-api")
        endpoint: Specific endpoint to get info about (optional)
    
    Returns:
        Dict: API documentation, endpoints, and usage examples
    """
    try:
        api_data = loader.load_data("documentation/api_docs.json")
        
        if not api_name:
            # Return list of available APIs
            api_list = []
            for api in api_data.get("apis", []):
                api_list.append({
                    "name": api.get("name", ""),
                    "description": api.get("description", ""),
                    "version": api.get("version", ""),
                    "status": api.get("status", "")
                })
            return {
                "status": "success",
                "available_apis": api_list,
                "message": "Specify an api_name to get detailed information"
            }
        
        # Find specific API
        api_name_lower = api_name.lower()
        target_api = None
        for api in api_data.get("apis", []):
            if api_name_lower in api.get("name", "").lower():
                target_api = api
                break
        
        if not target_api:
            return {
                "status": "error",
                "error_message": f"API '{api_name}' not found",
                "available_apis": [api.get("name", "") for api in api_data.get("apis", [])]
            }
        
        result = {
            "status": "success",
            "api_name": target_api.get("name", ""),
            "description": target_api.get("description", ""),
            "version": target_api.get("version", ""),
            "base_url": target_api.get("base_url", ""),
            "authentication": target_api.get("authentication", {}),
            "documentation_url": target_api.get("documentation_url", ""),
            "status": target_api.get("status", ""),
            "endpoints": target_api.get("key_endpoints", [])
        }
        
        # If specific endpoint requested, filter to that
        if endpoint:
            endpoint_lower = endpoint.lower()
            matching_endpoints = []
            for ep in target_api.get("key_endpoints", []):
                if (endpoint_lower in ep.get("path", "").lower() or
                    endpoint_lower in ep.get("description", "").lower()):
                    matching_endpoints.append(ep)
            result["endpoints"] = matching_endpoints
            result["endpoint_filter"] = endpoint
        
        return result
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to get API information: {str(e)}"
        }
