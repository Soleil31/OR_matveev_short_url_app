from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from schemas.urls import URLCreate, AllURLs, URLStat
from utils.urls import generate_short_id
from database.models import URLItem
from database.connect import get_db


router = APIRouter(tags=['urls'])


@router.post("/shorten")
def shorten_url(item: URLCreate, db: Session = Depends(get_db)):
    short_id = generate_short_id()
    existing = db.query(URLItem).filter(URLItem.short_id == short_id).first()
    if not existing:
        new_item = URLItem(short_id=short_id, full_url=str(item.url))
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return {"short_url": f"http://localhost:8000/{short_id}"}
    raise HTTPException(status_code=500, detail="Не удалось сгенерировать короткую ссылку")


@router.patch("/short-url")
def update_shor_url(short_id: str, db: Session = Depends(get_db)):
    url_item = db.query(URLItem).filter(URLItem.short_id == short_id).first()
    if not url_item:
        raise HTTPException(status_code=404, detail="Короткая ссылка не найдена")
    new_short_id = generate_short_id()
    url_item.short_id = new_short_id
    db.commit()
    db.refresh(url_item)
    return {"short_id": f"http://localhost:8000/{new_short_id}"}


@router.get("/all", response_model=list[AllURLs])
def get_all_urls(db: Session = Depends(get_db)):
    urls_items = db.query(URLItem).all()
    return urls_items


@router.get("/stats/{short_id}", response_model=URLStat)
def get_stats(short_id: str, db: Session = Depends(get_db)):
    url_item = db.query(URLItem).filter(URLItem.short_id == short_id).first()
    if not url_item:
        raise HTTPException(status_code=404, detail="Короткая ссылка не найдена")
    return url_item


@router.get("/{short_id}")
def redirect_to_full(short_id: str, db: Session = Depends(get_db)):
    url_item = db.query(URLItem).filter(URLItem.short_id == short_id).first()
    if not url_item:
        raise HTTPException(status_code=404, detail="Короткая ссылка не найдена")
    return RedirectResponse(url=str(url_item.full_url))
