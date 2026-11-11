from rm_copilot.config import Settings, settings
from rm_copilot.knowledge import KnowledgeIndex
from rm_copilot.orchestrator import ControlledBriefingOrchestrator
from rm_copilot.repository import BankingRepository
from rm_copilot.tools import ReadOnlyRMTools


def build_orchestrator(config: Settings = settings) -> ControlledBriefingOrchestrator:
    repository = BankingRepository(config.data_dir)
    knowledge = KnowledgeIndex(config.knowledge_dir, config.knowledge_dimensions)
    return ControlledBriefingOrchestrator(ReadOnlyRMTools(repository, knowledge))
