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
        Run a group mediation simulation where all participants speak first, then AI mediates
        
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
        
        # Step 1: All participants share their initial messages first
        for participant in participants:
            conversation_log.append({
                "speaker": participant["name"],
                "content": participant["initial_message"],
                "timestamp": datetime.utcnow().isoformat()
            })
        
        # Step 2: AI mediator responds to the full group conversation
        ai_response = await self._get_ai_group_response(
            context,
            conversation_log,
            settings
        )
        
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
        
        context += "IMPORTANT INSTRUCTIONS:\n"
        context += "- You are the AI mediator facilitating a group conversation.\n"
        context += "- All participants have shared their opening thoughts.\n"
        context += "- Respond to the group as a whole, addressing themes and facilitating dialogue.\n" 
        context += "- Do not include any speaker labels or prefixes in your response.\n"
        context += "- Do not simulate or speak for participants.\n"
        context += "- Your response should be your direct words to the group.\n\n"
        
        return context
    
    async def _get_ai_group_response(
        self, 
        context: str, 
        conversation_log: List[Dict[str, Any]],
        settings: Dict[str, Any]
    ) -> str:
        """Get AI mediator response to the full group conversation"""
        try:
            # Format all participant messages for the AI
            participant_messages = []
            for msg in conversation_log:
                if msg["speaker"] != "AI":
                    participant_messages.append(f"{msg['speaker']}: {msg['content']}")
            
            conversation_text = "\n\n".join(participant_messages)
            
            user_message = f"Here's what each participant has shared:\n\n{conversation_text}\n\nAs the group mediator, please respond to facilitate dialogue and understanding between all participants."
            
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