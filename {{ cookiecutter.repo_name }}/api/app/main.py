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

import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api_exceptions import ApiException
from app.routers import routers
from app.utils.logging import setup_logging

__author__ = ["Traversaal.ai"]
__copyright__ = ["Copyright 2023 Traversaal.ai"]
__maintainer__ = ["Traversaal.ai"]
__all__ = []

# ----------------------- ENVIRONMENT VARIABLES -------------------------------

OUTPUT_PORT = 8000
HOST = "0.0.0.0"

# -------------------------- APP DEFINITION -----------------------------------

# --- Defining Application
app = FastAPI()

# --- Adding routes to the application
for router in routers:
    app.include_router(router=router)

# --- Adding application middleware
# NOTE: For reference: https://fastapi.tiangolo.com/tutorial/middleware/
app.add_middleware(
    CORSMiddleware,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


# -------------------------- APP EXCEPTIONS -----------------------------------


@app.exception_handler(ApiException)
async def api_exception_handler(request: Request, exc: ApiException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message},
    )


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": str(exc)},
    )


# --------------------------- APP SCRIPTS -------------------------------------


def start():
    """
    Main function for starting the FastAPI application.
    """
    # Setting up logging
    setup_logging()
    # Running application
    uvicorn.run(
        "app.main:app",
        host=HOST,
        port=OUTPUT_PORT,
        log_level="info",
        reload=False,
    )


def dev():
    """
    Main function for starting the FastAPI application.
    This function is used for debugging purposes.
    """
    # Setting up logging
    setup_logging()
    # Running application
    uvicorn.run(
        "app.main:app",
        host=HOST,
        port=OUTPUT_PORT,
        log_level="debug",
        reload=True,
    )


if __name__ == "__main__":
    start()
