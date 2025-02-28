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
from fastapi import APIRouter
from app.models.genai.llm_prompt import LLMRequest, LLMResponse
from app.service.llm_service import LLMService

__author__ = ["Victor Calderon"]
__maintainer__ = ["Victor Calderon"]

logger = get_logger(__name__)

# ---------------------------- ROUTER DEFINITION ------------------------------

router = APIRouter(
    prefix="/api/genai",
    tags=["genai"],
)

# -------------------------------- ROUTES -------------------------------------


@router.post("/llm", response_model=LLMResponse)
def make_llm_call(request: LLMRequest):
    """
    Function to make an LLM call.
    """
    # Initializing service
    llm_service = LLMService(request=request)

    return llm_service.invoke()
