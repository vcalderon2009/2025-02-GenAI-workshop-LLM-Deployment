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

import logging

from fastapi import APIRouter
from app.models.initial import Initial

__author__ = ["Traversaal.ai"]
__copyright__ = ["Copyright 2023 Traversaal.ai"]
__maintainer__ = ["Traversaal.ai"]
__all__ = []

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# ---------------------------- ROUTER DEFINITION ------------------------------

router = APIRouter(
    prefix="/api/initial",
    tags=["initial"],
)

# -------------------------------- ROUTES -------------------------------------


@router.get("", response_model=Initial)
def example_route():
    return {"message": "This is an example route."}
