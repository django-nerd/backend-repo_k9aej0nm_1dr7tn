"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional, Literal

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Add your own schemas here:
# --------------------------------------------------

CategoryType = Literal[
    "Structural",
    "Civil",
    "Geotechnical",
    "New Enquiry",
    "Other",
]

class CallLog(BaseModel):
    """
    Caller records from AI receptionist
    Collection name: "calllog"
    """
    caller_name: Optional[str] = Field(None, description="Name of the caller, if provided")
    phone: Optional[str] = Field(None, description="Phone number")
    email: Optional[str] = Field(None, description="Email address if provided")
    company: Optional[str] = Field(None, description="Company or organization")
    category: CategoryType = Field(..., description="Call category")
    subject: Optional[str] = Field(None, description="Short subject or title")
    message: Optional[str] = Field(None, description="Transcribed message or notes")
    source: str = Field("ai-receptionist", description="Source system that created the log")
    assigned_to: Optional[str] = Field(None, description="Engineer or team assigned")
    priority: Optional[Literal["low", "medium", "high"]] = Field("medium", description="Priority flag")
    status: Optional[Literal["new", "in_progress", "closed"]] = Field("new", description="Workflow status")
