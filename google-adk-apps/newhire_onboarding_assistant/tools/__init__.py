"""
Tools module for ADK Onboarding Assistant
Export all tools for easy import in agent.py
"""

from .codebase_tools import (
    search_codebase,
    analyze_dependencies,
    check_best_practices,
    get_tech_stack_info
)

from .documentation_tools import (
    search_documentation,
    find_wiki_content,
    get_api_docs
)

from .troubleshooting_tools import (
    analyze_error,
    find_solutions,
    run_diagnostics
)

from .policy_tools import (
    search_policies,
    check_compliance,
    find_guidelines
)

from .team_tools import (
    get_team_info,
    find_team_member,
    schedule_meeting
)

# Export all tools
__all__ = [
    # Codebase tools
    'search_codebase',
    'analyze_dependencies',
    'check_best_practices',
    'get_tech_stack_info',
    # Documentation tools
    'search_documentation',
    'find_wiki_content',
    'get_api_docs',
    # Troubleshooting tools
    'analyze_error',
    'find_solutions',
    'run_diagnostics',
    # Policy tools
    'search_policies',
    'check_compliance',
    'find_guidelines',
    # Team tools
    'get_team_info',
    'find_team_member',
    'schedule_meeting'
]
