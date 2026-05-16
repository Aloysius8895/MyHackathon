"""
Troubleshooting and error resolution tools for development issues
Following ADK patterns for tool implementation
"""

import json
import os
import re
import sys
from typing import Dict, List


from new_hire.database.db_loader import DatabaseLoader

# Initialize database loader
loader = DatabaseLoader()

def analyze_error(error_message: str, context: str = "") -> dict:
    """Analyze error messages and provide detailed diagnosis.
    
    Args:
        error_message: The error message or stack trace to analyze
        context: Additional context about when/where the error occurred (optional)
    
    Returns:
        Dict: Error analysis with type, cause, and suggested solutions
    """
    try:
        error_data = loader.load_data("troubleshooting/common_errors.json")
        error_lower = error_message.lower()
        context_lower = context.lower() if context else ""
        
        # Find matching error patterns
        matches = []
        for error_category, error_info in error_data.get("error_patterns", {}).items():
            for pattern in error_info.get("patterns", []):
                if pattern.lower() in error_lower:
                    matches.append({
                        "category": error_category,
                        "type": error_info.get("type", ""),
                        "description": error_info.get("description", ""),
                        "common_causes": error_info.get("common_causes", []),
                        "initial_steps": error_info.get("initial_steps", []),
                        "severity": error_info.get("severity", "medium"),
                        "pattern_matched": pattern
                    })
        
        if not matches:
            # Generic analysis if no specific pattern found
            generic_analysis = {
                "category": "unknown",
                "type": "Unrecognized Error",
                "description": "This error pattern is not in our common issues database",
                "suggested_approach": [
                    "Check the full stack trace for more context",
                    "Look for similar errors in logs",
                    "Check recent code changes",
                    "Verify environment configuration"
                ],
                "severity": "unknown"
            }
            return {
                "status": "success",
                "error_message": error_message,
                "analysis": generic_analysis,
                "context": context,
                "recommendation": "Try using find_solutions to search for similar issues or run_diagnostics for system checks"
            }
        
        # Return the best match (first one found)
        best_match = matches[0]
        return {
            "status": "success",
            "error_message": error_message,
            "analysis": {
                "error_category": best_match["category"],
                "error_type": best_match["type"],
                "description": best_match["description"],
                "severity": best_match["severity"],
                "common_causes": best_match["common_causes"],
                "initial_troubleshooting_steps": best_match["initial_steps"],
                "pattern_matched": best_match["pattern_matched"]
            },
            "context": context,
            "additional_matches": len(matches) - 1 if len(matches) > 1 else 0
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to analyze error: {str(e)}"
        }

def find_solutions(problem_description: str, category: str = "") -> dict:
    """Search for solutions to specific problems or error scenarios.
    
    Args:
        problem_description: Description of the problem or issue
        category: Optional category to narrow search (e.g., "database", "authentication")
    
    Returns:
        Dict: Matching solutions with step-by-step resolution guides
    """
    try:
        solutions_data = loader.load_data("troubleshooting/solutions.json")
        problem_lower = problem_description.lower()
        category_lower = category.lower() if category else ""
        
        matching_solutions = []
        for solution in solutions_data.get("solutions", []):
            relevance_score = 0
            
            # Check problem description match
            if any(keyword.lower() in problem_lower for keyword in solution.get("keywords", [])):
                relevance_score += 2
            
            # Check title match
            if any(word in solution.get("title", "").lower() for word in problem_lower.split()):
                relevance_score += 1
            
            # Check category match if specified
            if category_lower and category_lower in solution.get("category", "").lower():
                relevance_score += 3
            
            if relevance_score > 0:
                solution_info = {
                    "title": solution.get("title", ""),
                    "category": solution.get("category", ""),
                    "description": solution.get("description", ""),
                    "difficulty": solution.get("difficulty", "medium"),
                    "estimated_time": solution.get("estimated_time", ""),
                    "prerequisites": solution.get("prerequisites", []),
                    "steps": solution.get("steps", []),
                    "verification": solution.get("verification", []),
                    "prevention": solution.get("prevention", []),
                    "related_issues": solution.get("related_issues", []),
                    "relevance_score": relevance_score
                }
                matching_solutions.append(solution_info)
        
        # Sort by relevance
        matching_solutions.sort(key=lambda x: x["relevance_score"], reverse=True)
        
        if not matching_solutions:
            # Get available categories if no solutions found
            categories = list(set(sol.get("category", "") for sol in solutions_data.get("solutions", [])))
            return {
                "status": "success",
                "problem_description": problem_description,
                "solutions_found": 0,
                "available_categories": categories,
                "suggestion": "Try rephrasing your problem or specify a category from the available list"
            }
        
        return {
            "status": "success",
            "problem_description": problem_description,
            "category_filter": category if category else "all",
            "solutions_found": len(matching_solutions),
            "top_solutions": matching_solutions[:3],  # Return top 3 solutions
            "additional_solutions_available": max(0, len(matching_solutions) - 3)
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to find solutions: {str(e)}"
        }

def run_diagnostics(component: str = "system", check_type: str = "basic") -> dict:
    """Run diagnostic checks on system components and services.
    
    Args:
        component: Component to check - "system", "database", "network", "services" (default: "system")
        check_type: Type of check - "basic", "detailed", "performance" (default: "basic")
    
    Returns:
        Dict: Diagnostic results with status and recommendations
    """
    try:
        diagnostics_data = loader.load_data("troubleshooting/diagnostics.json")
        
        # Get diagnostic checks for the specified component
        component_checks = diagnostics_data.get("components", {}).get(component, {})
        
        if not component_checks:
            available_components = list(diagnostics_data.get("components", {}).keys())
            return {
                "status": "error",
                "error_message": f"Component '{component}' not available for diagnostics",
                "available_components": available_components
            }
        
        # Get checks based on type
        checks_to_run = component_checks.get(check_type, {})
        
        if not checks_to_run:
            available_check_types = list(component_checks.keys())
            return {
                "status": "error",
                "error_message": f"Check type '{check_type}' not available for component '{component}'",
                "available_check_types": available_check_types
            }
        
        # Simulate running checks (with mock results)
        diagnostic_results = {
            "status": "success",
            "component": component,
            "check_type": check_type,
            "timestamp": "2025-01-01T12:00:00Z",
            "overall_status": "healthy",
            "checks_performed": [],
            "issues_found": [],
            "recommendations": []
        }
        
        # Process each check
        total_checks = len(checks_to_run.get("checks", []))
        passed_checks = 0
        
        for check in checks_to_run.get("checks", []):
            # Simulate check execution with mock results
            check_result = {
                "name": check.get("name", ""),
                "description": check.get("description", ""),
                "status": check.get("mock_status", "pass"),  # Mock status for demo
                "value": check.get("mock_value", "OK"),
                "expected": check.get("expected", ""),
                "message": check.get("mock_message", "Check completed successfully")
            }
            
            diagnostic_results["checks_performed"].append(check_result)
            
            if check_result["status"] == "pass":
                passed_checks += 1
            else:
                # Add to issues if check failed
                diagnostic_results["issues_found"].append({
                    "check": check_result["name"],
                    "issue": check_result["message"],
                    "severity": check.get("severity", "medium"),
                    "suggested_action": check.get("suggested_action", "Review check details")
                })
        
        # Determine overall status
        if passed_checks == total_checks:
            diagnostic_results["overall_status"] = "healthy"
        elif passed_checks >= total_checks * 0.8:
            diagnostic_results["overall_status"] = "warning"
        else:
            diagnostic_results["overall_status"] = "critical"
        
        # Add general recommendations
        diagnostic_results["recommendations"] = checks_to_run.get("recommendations", [])
        
        # Add summary
        diagnostic_results["summary"] = {
            "total_checks": total_checks,
            "passed_checks": passed_checks,
            "failed_checks": total_checks - passed_checks,
            "health_score": int((passed_checks / total_checks) * 100) if total_checks > 0 else 0
        }
        
        return diagnostic_results
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to run diagnostics: {str(e)}"
        }
