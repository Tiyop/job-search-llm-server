from __future__ import annotations
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Tuple, Union

from langchain import LLMChain
from langchain.callbacks.manager import CallbackManagerForChainRun
from langchain.chains.base import Chain
from langchain.chains.sequential import SequentialChain
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain.prompts import ChatPromptTemplate
from langchain.schema import BasePromptTemplate
from langchain.schema.language_model import BaseLanguageModel
from langchain.tools import APIOperation
from langchain.utilities.openapi import OpenAPISpec
from langchain.chains.openai_functions.openapi import openapi_spec_to_openai_fn


def get_openapi_llm(
    spec: Union[OpenAPISpec, str],
    llm: Optional[BaseLanguageModel] = None,
    prompt: Optional[BasePromptTemplate] = None,
    llm_chain_kwargs: Optional[Dict] = None,
    verbose: bool = False,
) -> LLMChain:
    """Create an LLMChain which provides request API string from a OpenAPI spec.

    Args:
        spec: OpenAPISpec or url/file/text string corresponding to one.
        llm: language model, should be an OpenAI function-calling model, e.g.
            `ChatOpenAI(model="gpt-3.5-turbo-0613")`.
        prompt: Main prompt template to use.
        request_chain: Chain for taking the functions output and executing the request.
    """
    if isinstance(spec, str):
        for conversion in (
            OpenAPISpec.from_url,
            OpenAPISpec.from_file,
            OpenAPISpec.from_text,
        ):
            try:
                spec = conversion(spec)  # type: ignore[arg-type]
                break
            except Exception:  # noqa: E722
                pass
        if isinstance(spec, str):
            raise ValueError(f"Unable to parse spec from source {spec}")
    openai_fns, call_api_fn = openapi_spec_to_openai_fn(spec)
    llm = llm or ChatOpenAI(
        model="gpt-3.5-turbo-0613",
    )
    prompt = prompt or ChatPromptTemplate.from_template(
        "Use the provided API's to respond to this user query:\n\n{query}"
    )
    return LLMChain(
        llm=llm,
        prompt=prompt,
        llm_kwargs={"functions": openai_fns},
        # output_parser=JsonOutputFunctionsParser(args_only=False),
        # output_key="function",
        verbose=verbose,
        **(llm_chain_kwargs or {}),
    )