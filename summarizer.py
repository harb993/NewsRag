from langchain_ollama import ChatOllama
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.schema import Document
from typing import List

class Summarizer:
    def __init__(self, model_name: str = "qwen2.5:0.5b"):
        self.llm = ChatOllama(model=model_name, temperature=0.7)
        self.personas = {
            "reporter": "You are a professional news reporter. Provide a factual, neutral, and concise summary of the news. Avoid any personal opinion or bias.",
            "visionary": "You are a tech visionary and futurist. Summarize the news with a focus on innovation, future possibilities, and potential positive impact on society. Be enthusiastic and forward-looking.",
            "skeptic": "You are a critical analyst and skeptic. Summarize the news by highlighting risks, challenges, and potential downsides. Look for the 'catch' and question the hype."
        }

    def _get_persona_prompt(self, persona: str) -> str:
        return self.personas.get(persona, self.personas["reporter"])

    def summarize_brief(self, docs: List[Document], persona: str = "reporter") -> str:
        """
        Creates a 1-2 sentence brief summary using a specific persona.
        """
        persona_instruction = self._get_persona_prompt(persona)
        prompt_template = f"""{persona_instruction}
        Write a very concise 1-2 sentence summary of the following news articles:
        "{{text}}"
        CONCISE SUMMARY:"""
        prompt = PromptTemplate.from_template(prompt_template)
        
        chain = load_summarize_chain(self.llm, chain_type="stuff", prompt=prompt)
        result = chain.invoke(docs)
        return result["output_text"]

    def summarize_detailed(self, docs: List[Document], persona: str = "reporter") -> str:
        """
        Creates a detailed paragraph summary using a specific persona.
        """
        persona_instruction = self._get_persona_prompt(persona)
        
        map_template = f"""{persona_instruction}
        The following is a news article snippet:
        {{text}}
        Based on this, identifying the key takeaway:"""
        map_prompt = PromptTemplate.from_template(map_template)
        
        combine_template = f"""{persona_instruction}
        The following are takeaways from several news articles:
        {{text}}
        Write a detailed paragraph summarizing these news items for the user:
        DETAILED SUMMARY:"""
        combine_prompt = PromptTemplate.from_template(combine_template)
        
        chain = load_summarize_chain(
            self.llm, 
            chain_type="map_reduce", 
            map_prompt=map_prompt, 
            combine_prompt=combine_prompt
        )
        result = chain.invoke(docs)
        return result["output_text"]

if __name__ == "__main__":
    # Test stub
    pass
