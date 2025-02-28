# MIT License
#
# Copyright 2025, Victor Calderon
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from app.utils.logging import get_logger
from app.models.genai.llm_prompt import LLMRequest
from app.utils import aws_utils as au
import os
from functools import cache
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from fastapi import HTTPException
from typing import Dict

__author__ = ["Victor Calderon"]
__all__ = [
    "LLMService",
]

logger = get_logger(__name__)

# Rading in HuggingFace token


# ------------------------------- SECRETS -------------------------------------

HF_TOKEN_SECRET_NAME = os.getenv("HF_CREDENTIALS_SECRET_NAME")
AWS_REGION = os.getenv("AWS_REGION")

# Reading in secret
HF_TOKEN = au.get_aws_secret(
    secret_name=HF_TOKEN_SECRET_NAME,
    region_name=AWS_REGION,
)["HF_TOKEN"]


# --------------------------- CLASS DEFINITION --------------------------------


class LLMService(object):
    def __init__(self, request: LLMRequest):
        # Initializing parameters
        self.prompt = request.prompt
        self.model_name = request.model_name
        self.temperature = request.temperature
        self.max_length = request.max_length

        # Initializing model components
        self.model_obj, self.tokenizer = self.initialize_model()

    @cache
    def initialize_model(self) -> None:
        """
        Method for initializing the model from HuggingFace. It initializes
        the corresponding tokenizer and model from Hugging Face.
        """
        # --- Tokenizer
        tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            token=HF_TOKEN,
        )

        # --- LLM model
        model_obj = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            token=HF_TOKEN,
        )

        return model_obj, tokenizer

    def invoke(self) -> Dict[str, str]:
        """
        Method for invoking the LLM with an input prompt.
        """
        try:
            input_msgs = self.tokenizer(self.prompt, return_tensors="pt")

            with torch.no_grad():
                # Generating output response
                output_encoded = self.model_obj.generate(
                    **input_msgs,
                    temperature=self.temperature,
                    max_length=self.max_length,
                )

            # Decoding tokens
            generated_text = self.tokenizer.decode(
                output_encoded[0],
                skip_special_tokens=True,
            )

            return {"response": generated_text}
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=str(e),
            )
