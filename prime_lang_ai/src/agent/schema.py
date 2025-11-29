from pydantic import BaseModel, Field

class GeneralResponse(BaseModel):
    message: str = Field(..., description="The AI response")