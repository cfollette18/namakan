# This file now imports Prisma-generated models
# The actual models are generated from schema.prisma
# Run `prisma generate` to update these imports

from prisma.models import (
    User,
    Project,
    Agent,
    AgentEvent,
    Learning,
    Collaboration,
    Template
)

# Type hints for better IDE support
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from prisma.models import User as UserModel
    from prisma.models import Project as ProjectModel
    from prisma.models import Agent as AgentModel
    from prisma.models import AgentEvent as AgentEventModel
    from prisma.models import Learning as LearningModel
    from prisma.models import Collaboration as CollaborationModel
    from prisma.models import Template as TemplateModel

# Re-export for backward compatibility
__all__ = [
    "User",
    "Project",
    "Agent",
    "AgentEvent",
    "Learning",
    "Collaboration",
    "Template"
]
