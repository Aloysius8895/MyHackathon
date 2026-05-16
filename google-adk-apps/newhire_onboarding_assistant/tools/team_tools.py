"""
Team integration and collaboration tools for new hires
Following ADK patterns for tool implementation
"""

import json
import os
import sys
from typing import Dict, List


from new_hire.database.db_loader import DatabaseLoader

# Initialize database loader
loader = DatabaseLoader()

def get_team_info(team_name: str = "") -> dict:
    """Get information about team structure, members, and dynamics.
    
    Args:
        team_name: Specific team name to get info about (optional)
    
    Returns:
        Dict: Team structure, members, and organizational information
    """
    try:
        team_data = loader.load_data("teams/team_structure.json")
        
        if not team_name:
            # Return overall team structure
            teams_list = []
            for team, info in team_data.get("teams", {}).items():
                teams_list.append({
                    "name": team,
                    "description": info.get("description", ""),
                    "size": len(info.get("members", [])),
                    "manager": info.get("manager", ""),
                    "focus_areas": info.get("focus_areas", [])
                })
            return {
                "status": "success",
                "organization_structure": team_data.get("organization_structure", {}),
                "teams": teams_list,
                "total_teams": len(teams_list),
                "message": "Specify a team_name to get detailed information"
            }
        
        # Find specific team
        team_name_lower = team_name.lower()
        found_team = None
        for team, info in team_data.get("teams", {}).items():
            if team_name_lower in team.lower():
                found_team = team
                break
        
        if not found_team:
            return {
                "status": "error",
                "error_message": f"Team '{team_name}' not found",
                "available_teams": list(team_data.get("teams", {}).keys()),
                "suggestion": "Try searching for one of the available teams listed above"
            }
        
        team_info = team_data["teams"][found_team]
        return {
            "status": "success",
            "team_name": found_team,
            "description": team_info.get("description", ""),
            "manager": team_info.get("manager", ""),
            "size": len(team_info.get("members", [])),
            "members": team_info.get("members", []),
            "focus_areas": team_info.get("focus_areas", []),
            "collaboration_tools": team_info.get("collaboration_tools", []),
            "meeting_schedule": team_info.get("meeting_schedule", {}),
            "key_projects": team_info.get("key_projects", []),
            "team_culture": team_info.get("team_culture", "")
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to get team information: {str(e)}"
        }

def find_team_member(name: str = "", expertise: str = "", role: str = "") -> dict:
    """Find team members by name, expertise, or role.
    
    Args:
        name: Name of the team member to find (optional)
        expertise: Area of expertise to search for (optional)
        role: Specific role to search for (optional)
    
    Returns:
        Dict: Matching team members with their information
    """
    try:
        team_data = loader.load_data("teams/team_members.json")
        members_data = team_data.get("members", [])
        
        if not any([name, expertise, role]):
            return {
                "status": "error",
                "error_message": "Please provide at least one search criterion: name, expertise, or role",
                "available_roles": list(set(m.get("role", "") for m in members_data)),
                "expertise_areas": list(set(exp for m in members_data for exp in m.get("expertise", [])))
            }
        
        matching_members = []
        name_lower = name.lower() if name else ""
        expertise_lower = expertise.lower() if expertise else ""
        role_lower = role.lower() if role else ""
        
        for member in members_data:
            relevance_score = 0
            
            # Check name match
            if name and name_lower in member.get("name", "").lower():
                relevance_score += 5
            
            # Check expertise match
            if expertise and any(expertise_lower in exp.lower() for exp in member.get("expertise", [])):
                relevance_score += 3
            
            # Check role match
            if role and role_lower in member.get("role", "").lower():
                relevance_score += 2
            
            if relevance_score > 0:
                member_info = {
                    "name": member.get("name", ""),
                    "role": member.get("role", ""),
                    "team": member.get("team", ""),
                    "email": member.get("email", ""),
                    "slack_handle": member.get("slack_handle", ""),
                    "expertise": member.get("expertise", []),
                    "bio": member.get("bio", ""),
                    "location": member.get("location", ""),
                    "timezone": member.get("timezone", ""),
                    "availability": member.get("availability", ""),
                    "fun_fact": member.get("fun_fact", ""),
                    "relevance_score": relevance_score
                }
                matching_members.append(member_info)
        
        # Sort by relevance
        matching_members.sort(key=lambda x: x["relevance_score"], reverse=True)
        
        if not matching_members:
            return {
                "status": "success",
                "search_criteria": {
                    "name": name if name else None,
                    "expertise": expertise if expertise else None,
                    "role": role if role else None
                },
                "members_found": 0,
                "message": "No team members found matching your criteria"
            }
        
        return {
            "status": "success",
            "search_criteria": {
                "name": name if name else None,
                "expertise": expertise if expertise else None,
                "role": role if role else None
            },
            "members_found": len(matching_members),
            "matching_members": matching_members[:10],  # Top 10 matches
            "additional_members_available": max(0, len(matching_members) - 10)
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to find team members: {str(e)}"
        }

def schedule_meeting(with_person: str, purpose: str, duration: str = "30 minutes") -> dict:
    """Schedule a meeting with a team member.
    
    Args:
        with_person: Name or email of the person to meet with
        purpose: Purpose or topic of the meeting
        duration: Meeting duration (default: "30 minutes")
    
    Returns:
        Dict: Meeting scheduling information and next steps
    """
    try:
        # Load team member data to validate person
        team_data = loader.load_data("teams/team_members.json")
        members_data = team_data.get("members", [])
        
        # Find the person
        person_lower = with_person.lower()
        found_person = None
        for member in members_data:
            if (person_lower in member.get("name", "").lower() or
                person_lower in member.get("email", "").lower()):
                found_person = member
                break
        
        if not found_person:
            return {
                "status": "error",
                "error_message": f"Person '{with_person}' not found in the team directory",
                "suggestion": "Please use find_team_member to search for the correct name or email"
            }
        
        # Mock scheduling data
        scheduling_data = loader.load_data("teams/scheduling.json")
        
        # Simulate finding available slots
        meeting_info = {
            "status": "success",
            "meeting_with": found_person.get("name", ""),
            "email": found_person.get("email", ""),
            "purpose": purpose,
            "duration": duration,
            "suggested_times": scheduling_data.get("default_slots", []),
            "timezone": found_person.get("timezone", "UTC"),
            "calendar_link": f"https://calendar.company.com/schedule/{found_person.get('email', '').split('@')[0]}",
            "meeting_tips": scheduling_data.get("meeting_tips", {}).get(purpose.lower(), []),
            "next_steps": [
                f"Click the calendar link to see {found_person.get('name', '')}'s availability",
                "Choose a time slot that works for both of you",
                "Include the meeting purpose in your invitation",
                "Prepare any questions or topics you'd like to discuss"
            ]
        }
        
        # Add specific recommendations based on purpose
        purpose_lower = purpose.lower()
        if "introduction" in purpose_lower or "meet" in purpose_lower:
            meeting_info["preparation_tips"] = [
                "Prepare a brief introduction about yourself",
                "Think about what you'd like to learn from them",
                "Review their expertise areas beforehand",
                "Have questions ready about their work"
            ]
        elif "help" in purpose_lower or "question" in purpose_lower:
            meeting_info["preparation_tips"] = [
                "Document your specific questions or issues",
                "Gather any relevant context or error messages",
                "Be specific about what kind of help you need",
                "Consider what you've already tried"
            ]
        
        return meeting_info
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to schedule meeting: {str(e)}"
        }
