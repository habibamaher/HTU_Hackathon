def plan_mission(mission_prompt: str) -> list:
    """Breaks the mission into logical subtasks."""
    if "golf" in mission_prompt.lower():
        return [
            "Fetch top golf news from APIs",
            "Filter repeated topics",
            "Check for tournament or financial impact",
            "Summarize most important golf trend"
        ]
    return ["No tasks – prompt not golf-related"]
