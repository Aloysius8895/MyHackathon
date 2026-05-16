"""
Codebase navigation and analysis tools for new hire onboarding
Following ADK patterns for tool implementation
"""

import json
import os
import sys
from typing import Dict, List, Optional


from new_hire.database.db_loader import DatabaseLoader

# Initialize database loader
loader = DatabaseLoader()

def search_codebase(query: str, file_type: str = "all") -> dict:
    """Search through codebase for relevant files, functions, and repositories.
    
    Args:
        query: Search term or functionality to find (e.g., "authentication", "payment", "user")
        file_type: Type of files to search - "py", "js", "java", "all" (default: "all")
    
    Returns:
        Dict: Search results with repository information, key files, and code examples
    """
    try:
        codebase_data = loader.load_data("codebase/repositories.json")
        results = []
        query_lower = query.lower()
        
        # Search through repositories
        for repo in codebase_data.get("repositories", []):
            match_score = 0
            repo_info = {
                "repo_name": repo.get("name", ""),
                "description": repo.get("description", ""),
                "language": repo.get("language", ""),
                "framework": repo.get("framework", ""),
                "key_files": repo.get("key_files", []),
                "team": repo.get("team", ""),
                "documentation": repo.get("documentation", ""),
                "examples": repo.get("examples", {})
            }
            
            # Check for matches in name, description, dependencies
            if query_lower in repo.get("name", "").lower():
                match_score += 3
            if query_lower in repo.get("description", "").lower():
                match_score += 2
            if query_lower in str(repo.get("dependencies", [])).lower():
                match_score += 1
            
            if match_score > 0:
                repo_info["match_score"] = match_score
                results.append(repo_info)
        
        # Search through code snippets
        code_snippets = []
        for snippet_key, snippet_data in codebase_data.get("code_snippets", {}).items():
            if query_lower in snippet_key.lower() or query_lower in snippet_data.get("description", "").lower():
                code_snippets.append({
                    "type": snippet_key,
                    "file": snippet_data.get("file", ""),
                    "function": snippet_data.get("function", ""),
                    "code": snippet_data.get("code", ""),
                    "description": snippet_data.get("description", ""),
                    "best_practices": snippet_data.get("best_practices", [])
                })
        
        # Sort results by match score
        results.sort(key=lambda x: x.get("match_score", 0), reverse=True)
        
        return {
            "status": "success",
            "query": query,
            "repositories": results[:5],  # Top 5 repository matches
            "code_snippets": code_snippets[:3],  # Top 3 code examples
            "total_repositories_found": len(results),
            "total_snippets_found": len(code_snippets)
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to search codebase: {str(e)}"
        }

def analyze_dependencies(module_name: str) -> dict:
    """Analyze dependencies and relationships for a given module or service.
    
    Args:
        module_name: Name of the module/service to analyze (e.g., "user-auth-service", "payment-gateway")
    
    Returns:
        Dict: Dependency information, relationships, and architectural context
    """
    try:
        deps_data = loader.load_data("codebase/dependencies.json")
        module_lower = module_name.lower()
        found_module = None
        
        # Find module (case-insensitive)
        for mod_name, mod_data in deps_data.get("modules", {}).items():
            if module_lower in mod_name.lower():
                found_module = mod_name
                break
        
        if found_module:
            module_info = deps_data["modules"][found_module]
            return {
                "status": "success",
                "module": found_module,
                "description": module_info.get("description", ""),
                "dependencies": module_info.get("dependencies", []),
                "dependents": module_info.get("dependents", []),
                "architecture_layer": module_info.get("architecture_layer", ""),
                "communication_methods": module_info.get("communication_methods", []),
                "data_flows": module_info.get("data_flows", []),
                "integration_points": module_info.get("integration_points", [])
            }
        else:
            # Return available modules if not found
            available_modules = list(deps_data.get("modules", {}).keys())
            return {
                "status": "error",
                "error_message": f"Module '{module_name}' not found in dependency graph",
                "available_modules": available_modules,
                "suggestion": "Try searching for one of the available modules listed above"
            }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to analyze dependencies: {str(e)}"
        }

def check_best_practices(code_snippet: str = "", language: str = "python") -> dict:
    """Check code against internal coding standards and best practices.
    
    Args:
        code_snippet: Code to analyze (optional - if empty, returns general guidelines)
        language: Programming language for context (default: "python")
    
    Returns:
        Dict: Best practices analysis, recommendations, and coding standards
    """
    try:
        practices_data = loader.load_data("codebase/best_practices.json")
        
        # Get language-specific practices
        language_practices = practices_data.get("languages", {}).get(language, {})
        general_practices = practices_data.get("general", {})
        
        result = {
            "status": "success",
            "language": language,
            "general_guidelines": general_practices.get("guidelines", []),
            "language_specific": language_practices.get("guidelines", []),
            "code_quality_checklist": practices_data.get("quality_checklist", [])
        }
        
        if code_snippet:
            # Analyze specific code snippet
            violations = []
            recommendations = []
            
            # Check against mock rules
            for rule in practices_data.get("rules", []):
                trigger = rule.get("trigger", "").lower()
                if trigger and trigger in code_snippet.lower():
                    if rule.get("type") == "violation":
                        violations.append({
                            "rule": rule.get("rule", ""),
                            "message": rule.get("message", ""),
                            "severity": rule.get("severity", "medium")
                        })
                    else:
                        recommendations.append({
                            "rule": rule.get("rule", ""),
                            "message": rule.get("message", ""),
                            "improvement": rule.get("improvement", "")
                        })
            
            # Calculate score
            total_checks = len(practices_data.get("rules", []))
            violations_count = len(violations)
            score = max(0, int((total_checks - violations_count) / total_checks * 100))
            
            result.update({
                "code_analysis": {
                    "violations": violations,
                    "recommendations": recommendations,
                    "quality_score": score,
                    "analysis_summary": f"Found {violations_count} potential issues out of {total_checks} checks"
                }
            })
        
        return result
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to check best practices: {str(e)}"
        }

def get_tech_stack_info(component: str = "") -> dict:
    """Get information about the technology stack and tools used.
    
    Args:
        component: Specific component to get info about (optional)
    
    Returns:
        Dict: Technology stack information, tools, and frameworks
    """
    try:
        tech_data = loader.load_data("codebase/tech_stack.json")
        
        if not component:
            # Return overall tech stack
            return {
                "status": "success",
                "overview": tech_data.get("overview", ""),
                "frontend": tech_data.get("frontend", {}),
                "backend": tech_data.get("backend", {}),
                "infrastructure": tech_data.get("infrastructure", {}),
                "tools": tech_data.get("tools", {}),
                "databases": tech_data.get("databases", {})
            }
        
        # Search for specific component
        component_lower = component.lower()
        for category, items in tech_data.items():
            if isinstance(items, dict):
                for key, value in items.items():
                    if component_lower in key.lower():
                        return {
                            "status": "success",
                            "component": key,
                            "category": category,
                            "details": value
                        }
        
        return {
            "status": "error",
            "error_message": f"Component '{component}' not found in tech stack",
            "suggestion": "Try searching for frontend, backend, database, or infrastructure components"
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to get tech stack info: {str(e)}"
        }
