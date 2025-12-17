from agents.master_agent import MasterAgent
from typing import Dict
import uuid

class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, MasterAgent] = {}

    def get_agent(self, session_id: str) -> MasterAgent:
        if session_id not in self.sessions:
            self.sessions[session_id] = MasterAgent()
        return self.sessions[session_id]

    def create_session(self) -> str:
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = MasterAgent()
        return session_id

    def reset_session(self, session_id: str):
        self.sessions[session_id] = MasterAgent()
