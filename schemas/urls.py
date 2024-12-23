from pydantic import BaseModel, HttpUrl, Field, model_serializer


class URLCreate(BaseModel):
    url: HttpUrl


class URLStat(BaseModel):
    full_url: HttpUrl
    short_id: str


class AllURLs(BaseModel):
    full_url: HttpUrl
    short_id: str = Field(exclude=True)
    short_url: str = Field(default="", examples=[])

    class Config:
        from_attributes = True

    @model_serializer
    def serialize_model(self):
        self.short_url = f"http://localhost:8000/{self.short_id}"
        return {"full_url": self.full_url, "short_url": self.short_url}
