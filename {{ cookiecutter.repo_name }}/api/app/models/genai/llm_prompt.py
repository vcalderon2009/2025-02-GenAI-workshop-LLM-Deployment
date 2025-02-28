# MIT License
#
# Copyright {% now 'utc', '%Y' %}, {{ cookiecutter.author_name }}
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

from pydantic import BaseModel, Field
from typing import Optional


class LLMRequest(BaseModel):
    prompt: str = Field(..., description="Prompt for the LLM")
    model_name: str = Field(..., description="Name of the LLM model to use")
    temperature: Optional[float] = Field(0.1, description="Model temperature")
    max_length: Optional[int] = Field(100, description="Maximum token length")


class LLMResponse(BaseModel):
    response: str = Field(..., description="LLM Response")
