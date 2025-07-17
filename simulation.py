import os
import openai
from typing import List, Dict, Any
from datetime import datetime

class SimulationEngine:
    """Handles OpenAI GPT-4 simulation - AI responds to each participant's initial message"""
    
    def __init__(self):
        self.client = openai.OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
    
    async def run_simulation(
        self, 
        participants: List[Dict[str, Any]], 
        system_prompt: str, 
        settings: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Run a simulation where AI responds to each participant's initial message
        
        Args:
            participants: List of participant dictionaries with initial_message
            system_prompt: AI mediator system prompt
            settings: Model settings (temperature, max_tokens, etc.)
        
        Returns:
            List of conversation log entries
        """
        conversation_log = []
        
        # Build context for the AI
        context = self._build_context(participants, system_prompt)
        
        # Process each participant's initial message
        for participant in participants:
            # Add participant's message to log
            conversation_log.append({
                "speaker": participant["name"],
                "content": participant["initial_message"],
                "timestamp": datetime.utcnow().isoformat()
            })
            
            # Get AI response to this participant
            ai_response = await self._get_ai_response(
                context,
                participant,
                settings
            )
            
            # Add AI response to log
            conversation_log.append({
                "speaker": "AI",
                "content": ai_response,
                "timestamp": datetime.utcnow().isoformat()
            })
        
        return conversation_log
    
    def _build_context(self, participants: List[Dict[str, Any]], system_prompt: str) -> str:
        """Build context for the AI mediator"""
        context = f"{system_prompt}\n\n"
        context += "PARTICIPANTS IN THIS SESSION:\n"
        
        for participant in participants:
            context += f"- {participant['name']}: {participant['role']}\n"
            context += f"  Perspective: {participant['perspective']}\n"
            context += f"  Emotional state: {', '.join(participant['meta_tags'])}\n\n"
        
        return context
    
    async def _get_ai_response(
        self, 
        context: str, 
        current_participant: Dict[str, Any],
        settings: Dict[str, Any]
    ) -> str:
        """Get AI response to a specific participant's message"""
        try:
            # Just provide the participant's message and context
            user_message = f"{current_participant['name']}: {current_participant['initial_message']}"
            
            messages = [
                {"role": "system", "content": context},
                {"role": "user", "content": user_message}
            ]
            
            response = self.client.chat.completions.create(
                model=settings.get("model", "gpt-4"),
                messages=messages,
                temperature=settings.get("temperature", 0.7),
                max_tokens=settings.get("max_tokens", 400)
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"[AI Error: Unable to generate response - {str(e)}]"

# Global simulation engine instance
simulation_engine = SimulationEngine()