# agents/reporter_agent.py

def generate_report(validated_output):
    """Formats the final sports trend report for chat interface."""
    
    # Clean, natural chat format
    report = f"""
    <div style="line-height: 1.6;">
        <strong style="font-size: 16px; display: block; margin-bottom: 8px;">{validated_output.title}</strong>
        <p style="margin-bottom: 8px;">{validated_output.summary}</p>
        <p style="font-size: 13px; color: #999; font-style: italic;">{validated_output.impact}</p>
    </div>
    """
    return report.strip()