from neo4j_graphrag.retrievers import Text2CypherRetriever
from neo4j_graphrag.llm import LLMInterface
from types import SimpleNamespace
from neo4j_graphrag.types import RawSearchResult
import re
from typing import Dict, Any, Optional

class DeepSeekAdapter(LLMInterface):
    """
    Make the DeepSeek API compatible with the LLMInterface.
    """

    def __init__(self, client, model_name="deepseek_reasoner"):
        self.client = client
        self.model_name = model_name

    def invoke(self, prompt) -> SimpleNamespace:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant for annotating cell types based on marker genes."},
                {"role": "user", "content": prompt}
            ],
            timeout=60
        )

        return SimpleNamespace(content=response.choices[0].message.content)
    
    async def ainvoke(self, prompt: str) -> SimpleNamespace:
        """
        Async version of invoke, required by LLMInterface.
        Here we just delegate to the sync invoke, but you could
        also implement true async I/O if your client supports it.
        """
        return self.invoke(prompt)
    
def extract_cyphers(text: str) -> list:
    """
    Extract all cypher queries and do some simple cleaning.
    """

    blocks = re.findall(f"```(?:cypher)?(.*?)```", text, flags=re.DOTALL)
    if not blocks:
        blocks = [text]
    
    return [b.strip() for b in blocks if b.strip()]

class MultiCypherRetriever(Text2CypherRetriever):
    """
    A retriever that can handle multiple Cypher queries.
    """

    def get_search_results(
        self,
        query_text: str,
        prompt_params: Optional[Dict[str, Any]] = None,
    ) -> RawSearchResult:
        
        prompt = self.custom_prompt.format(
            schema=self.neo4j_schema,
            examples="\n".join(self.examples) if self.examples else "",
            query_text=query_text
        )

        llm_res = self.llm.invoke(prompt)
        full = llm_res.content

        cyphers = extract_cyphers(full)

        all_records = []
        with self.driver.session() as session:
            for c in cyphers:
                result = session.run(c)
                records = list(result)
                all_records.extend(records)

        return RawSearchResult(
            records=all_records,
            metadata={
                "full_text": full,
                "cyphers": cyphers
            }
        )