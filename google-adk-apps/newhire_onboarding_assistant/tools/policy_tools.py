"""
HR policy, security, and compliance tools for company guidelines
Following ADK patterns for tool implementation
"""

import json
import os
import sys
from typing import Dict, List


from new_hire.database.db_loader import DatabaseLoader

# Initialize database loader
loader = DatabaseLoader()

def search_policies(topic: str, policy_type: str = "all") -> dict:
    """Search HR policies and company procedures for specific topics.
    
    Args:
        topic: Topic to search for (e.g., "vacation", "remote work", "benefits")
        policy_type: Type of policy - "hr", "conduct", "benefits", "leave", "all" (default: "all")
    
    Returns:
        Dict: Matching policies with details and references
    """
    try:
        hr_data = loader.load_data("policies/hr_handbook.json")
        topic_lower = topic.lower()
        policy_type_lower = policy_type.lower()
        
        matching_policies = []
        for policy_category, policies in hr_data.get("policies", {}).items():
            # Filter by policy type if specified
            if policy_type != "all" and policy_type_lower not in policy_category.lower():
                continue
            
            for policy in policies:
                relevance_score = 0
                
                # Check title match
                if topic_lower in policy.get("title", "").lower():
                    relevance_score += 3
                
                # Check description match
                if topic_lower in policy.get("description", "").lower():
                    relevance_score += 2
                
                # Check keywords match
                if any(topic_lower in keyword.lower() for keyword in policy.get("keywords", [])):
                    relevance_score += 1
                
                if relevance_score > 0:
                    policy_info = {
                        "category": policy_category,
                        "title": policy.get("title", ""),
                        "description": policy.get("description", ""),
                        "details": policy.get("details", []),
                        "effective_date": policy.get("effective_date", ""),
                        "last_updated": policy.get("last_updated", ""),
                        "contact": policy.get("contact", ""),
                        "keywords": policy.get("keywords", []),
                        "relevance_score": relevance_score
                    }
                    matching_policies.append(policy_info)
        
        # Sort by relevance
        matching_policies.sort(key=lambda x: x["relevance_score"], reverse=True)
        
        if not matching_policies:
            # Return available policy categories
            available_categories = list(hr_data.get("policies", {}).keys())
            return {
                "status": "success",
                "topic": topic,
                "policies_found": 0,
                "available_categories": available_categories,
                "suggestion": "Try searching with different keywords or browse by category"
            }
        
        return {
            "status": "success",
            "topic": topic,
            "policy_type_filter": policy_type,
            "policies_found": len(matching_policies),
            "matching_policies": matching_policies[:5],  # Top 5 matches
            "additional_policies_available": max(0, len(matching_policies) - 5)
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to search policies: {str(e)}"
        }

def check_compliance(scenario: str, regulation_type: str = "") -> dict:
    """Check compliance requirements for specific scenarios or actions.
    
    Args:
        scenario: Description of the scenario or action to check (e.g., "handling customer data")
        regulation_type: Specific regulation to check against (e.g., "GDPR", "SOX") (optional)
    
    Returns:
        Dict: Compliance requirements and guidelines for the scenario
    """
    try:
        compliance_data = loader.load_data("policies/compliance_docs.json")
        scenario_lower = scenario.lower()
        regulation_lower = regulation_type.lower() if regulation_type else ""
        
        applicable_requirements = []
        for regulation, reg_data in compliance_data.get("regulations", {}).items():
            # Filter by regulation type if specified
            if regulation_lower and regulation_lower not in regulation.lower():
                continue
            
            for requirement in reg_data.get("requirements", []):
                # Check if requirement applies to scenario
                if any(keyword.lower() in scenario_lower for keyword in requirement.get("applicable_scenarios", [])):
                    req_info = {
                        "regulation": regulation,
                        "regulation_description": reg_data.get("description", ""),
                        "requirement_title": requirement.get("title", ""),
                        "description": requirement.get("description", ""),
                        "mandatory_actions": requirement.get("mandatory_actions", []),
                        "prohibited_actions": requirement.get("prohibited_actions", []),
                        "documentation_required": requirement.get("documentation_required", []),
                        "compliance_level": requirement.get("compliance_level", "standard"),
                        "penalties": requirement.get("penalties", ""),
                        "review_frequency": requirement.get("review_frequency", ""),
                        "responsible_team": requirement.get("responsible_team", "")
                    }
                    applicable_requirements.append(req_info)
        
        if not applicable_requirements:
            # Return available regulations if no matches
            available_regulations = list(compliance_data.get("regulations", {}).keys())
            return {
                "status": "success",
                "scenario": scenario,
                "applicable_requirements": 0,
                "available_regulations": available_regulations,
                "general_guidance": compliance_data.get("general_guidance", []),
                "suggestion": "Scenario may not have specific compliance requirements, or try rephrasing"
            }
        
        # Group by compliance level
        critical_requirements = [req for req in applicable_requirements if req["compliance_level"] == "critical"]
        standard_requirements = [req for req in applicable_requirements if req["compliance_level"] == "standard"]
        recommended_requirements = [req for req in applicable_requirements if req["compliance_level"] == "recommended"]
        
        return {
            "status": "success",
            "scenario": scenario,
            "regulation_filter": regulation_type if regulation_type else "all",
            "total_requirements": len(applicable_requirements),
            "compliance_summary": {
                "critical_requirements": len(critical_requirements),
                "standard_requirements": len(standard_requirements),
                "recommended_requirements": len(recommended_requirements)
            },
            "critical_requirements": critical_requirements,
            "standard_requirements": standard_requirements[:3],  # Top 3 standard
            "recommended_requirements": recommended_requirements[:2],  # Top 2 recommended
            "general_guidance": compliance_data.get("general_guidance", [])
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to check compliance: {str(e)}"
        }

def find_guidelines(guideline_type: str, specific_topic: str = "") -> dict:
    """Find security guidelines and procedural documentation.
    
    Args:
        guideline_type: Type of guidelines - "security", "development", "operations", "general"
        specific_topic: Specific topic within the guideline type (optional)
    
    Returns:
        Dict: Relevant guidelines, procedures, and best practices
    """
    try:
        security_data = loader.load_data("policies/security_guidelines.json")
        guideline_type_lower = guideline_type.lower()
        topic_lower = specific_topic.lower() if specific_topic else ""
        
        # Find matching guideline category
        matching_guidelines = []
        for category, category_data in security_data.get("guidelines", {}).items():
            # Check if category matches guideline type
            if guideline_type_lower in category.lower() or guideline_type == "general":
                for guideline in category_data.get("items", []):
                    relevance_score = 0
                    
                    # If specific topic provided, check relevance
                    if specific_topic:
                        if topic_lower in guideline.get("title", "").lower():
                            relevance_score += 3
                        if topic_lower in guideline.get("description", "").lower():
                            relevance_score += 2
                        if any(topic_lower in tag.lower() for tag in guideline.get("tags", [])):
                            relevance_score += 1
                        
                        # Skip if not relevant to specific topic
                        if relevance_score == 0:
                            continue
                    else:
                        relevance_score = 1  # Include all if no specific topic
                    
                    guideline_info = {
                        "category": category,
                        "title": guideline.get("title", ""),
                        "description": guideline.get("description", ""),
                        "requirements": guideline.get("requirements", []),
                        "best_practices": guideline.get("best_practices", []),
                        "common_violations": guideline.get("common_violations", []),
                        "implementation_guide": guideline.get("implementation_guide", []),
                        "severity": guideline.get("severity", "medium"),
                        "compliance_frameworks": guideline.get("compliance_frameworks", []),
                        "last_updated": guideline.get("last_updated", ""),
                        "tags": guideline.get("tags", []),
                        "relevance_score": relevance_score
                    }
                    matching_guidelines.append(guideline_info)
        
        # Sort by relevance
        matching_guidelines.sort(key=lambda x: x["relevance_score"], reverse=True)
        
        if not matching_guidelines:
            available_categories = list(security_data.get("guidelines", {}).keys())
            return {
                "status": "success",
                "guideline_type": guideline_type,
                "specific_topic": specific_topic,
                "guidelines_found": 0,
                "available_categories": available_categories,
                "suggestion": "Try a different guideline type or topic from the available categories"
            }
        
        # Group by severity for better organization
        critical_guidelines = [g for g in matching_guidelines if g["severity"] == "critical"]
        high_guidelines = [g for g in matching_guidelines if g["severity"] == "high"]
        medium_guidelines = [g for g in matching_guidelines if g["severity"] == "medium"]
        
        return {
            "status": "success",
            "guideline_type": guideline_type,
            "specific_topic": specific_topic if specific_topic else "all topics",
            "total_guidelines_found": len(matching_guidelines),
            "severity_breakdown": {
                "critical": len(critical_guidelines),
                "high": len(high_guidelines),
                "medium": len(medium_guidelines)
            },
            "critical_guidelines": critical_guidelines,
            "high_priority_guidelines": high_guidelines[:3],  # Top 3 high priority
            "standard_guidelines": medium_guidelines[:5],  # Top 5 standard
            "general_security_principles": security_data.get("general_principles", [])
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to find guidelines: {str(e)}"
        }
