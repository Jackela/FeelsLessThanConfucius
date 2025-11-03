from dataclasses import dataclass
from typing import Literal


Risk = Literal["low", "medium", "high"]
Action = Literal["pass", "alter", "reject"]


@dataclass
class SafetyDecision:
    risk: Risk
    action: Action
    reason: str


def classify_risk(text: str) -> Risk:
    # Placeholder heuristic: escalate if certain keywords appear
    high_terms = ("仇恨", "暴力", "人身攻击")
    med_terms = ("攻击", "极端", "侮辱")
    if any(t in text for t in high_terms):
        return "high"
    if any(t in text for t in med_terms):
        return "medium"
    return "low"


def decide_policy(text: str) -> SafetyDecision:
    risk = classify_risk(text)
    if risk == "high":
        return SafetyDecision(risk=risk, action="reject", reason="高风险内容，拒绝输出")
    if risk == "medium":
        return SafetyDecision(risk=risk, action="alter", reason="中风险内容，已安全改写")
    return SafetyDecision(risk=risk, action="pass", reason="通过")

