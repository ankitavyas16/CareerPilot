"""Analysis schemas"""
from typing import List

from pydantic import BaseModel


class SkillGapSchema(BaseModel):
	"""Skill gap analysis"""

	matching_required_skills: List[str]
	missing_required_skills: List[str]
	matching_preferred_skills: List[str]
	missing_preferred_skills: List[str]
	required_match_percentage: float
	learning_priority: List[dict]
	difficulty_assessment: str
