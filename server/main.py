from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, Meeting
from schemas import UserCreate, UserResponse, MeetingResponse
from auth import hash_password
from fastapi import UploadFile, File
from uuid import uuid4
from fastapi.middleware.cors import CORSMiddleware
from services.upload import upload_file
from services.transcribe import run_batch_recognize
from services.transcript import get_transcript
from services.summarize import generate_summary
from services.upload import get_public_url
from auth import hash_password,verify_password, create_token
from schemas import LoginRequest, TokenResponse


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Backend running"}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@app.post("/meetings/upload")
def upload_meeting(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    meeting_id = str(uuid4())

    # 1. Upload audio to GCS
    audio_path = upload_file(
        file,
        meeting_id
    )

    # 2. Save meeting in DB
    new_meeting = Meeting(
        owner_id=1,                 # Temporary until login is added
        title=file.filename,
        audio_path=audio_path,
        status="processing"
    )

    db.add(new_meeting)
    db.commit()
    db.refresh(new_meeting)

    print("Meeting saved:", new_meeting.id, new_meeting.title)

    # 3. Transcribe audio
    result = run_batch_recognize(
        meeting_id,
        ".wav"
    )

    transcript_uri = (
        result.results[
            f"gs://meeting-summarizer-audio/meetings/{meeting_id}/audio.wav"
        ]
        .cloud_storage_result.uri
    )

    transcript = get_transcript(transcript_uri)

    print("TRANSCRIPT:")
    print(transcript)

    # 4. Generate summary
    
    summary = generate_summary(transcript)
    new_meeting.transcript = transcript
    print("SUMMARY:")
    print(summary)

    # 5. Save transcript + summary
    new_meeting.transcript_path = (
        f"gs://meeting-summarizer-audio/meetings/{meeting_id}/transcription"
    )

    new_meeting.summary = summary
    new_meeting.status = "completed"

    db.commit()
    db.refresh(new_meeting)

    return {
        "id": new_meeting.id,
        "title": new_meeting.title,
        "status": new_meeting.status,
        "audio_path": new_meeting.audio_path,
        "transcript_path": new_meeting.transcript_path,
        "summary": new_meeting.summary
    }
    
@app.post("/login", response_model=TokenResponse)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == data.email
    ).first()


    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )


    if not verify_password(
        data.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )


    token = create_token(user.id)


    return {
        "access_token": token,
        "token_type": "bearer"
    }
        
@app.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    existing = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )


    new_user = User(
        email=user.email,
        hashed_password=hash_password(user.password)
    )


    db.add(new_user)
    db.commit()
    db.refresh(new_user)


    return {
        "message": "User created",
        "id": new_user.id
    }
    
    
@app.get("/meetings", response_model=list[MeetingResponse])
def get_meetings(
    db: Session = Depends(get_db)
):
    meetings = db.query(Meeting).all()

    return meetings

@app.get("/meetings/{meeting_id}", response_model=MeetingResponse)
def get_meeting(
    meeting_id: int,
    db: Session = Depends(get_db)
):
    meeting = db.query(Meeting).filter(
        Meeting.id == meeting_id
    ).first()

    if not meeting:
        raise HTTPException(
            status_code=404,
            detail="Meeting not found"
        )

    return meeting

@app.get("/meetings/{meeting_id}", response_model=MeetingResponse)
def get_meeting(
    meeting_id: int,
    db: Session = Depends(get_db)
):
    meeting = db.query(Meeting).filter(
        Meeting.id == meeting_id
    ).first()

    if not meeting:
        raise HTTPException(
            status_code=404,
            detail="Meeting not found"
        )

    return meeting

@app.get("/meetings/{meeting_id}/audio")
def get_audio(
    meeting_id: int,
    db: Session = Depends(get_db)
):
    meeting = db.query(Meeting).filter(
        Meeting.id == meeting_id
    ).first()

    if not meeting:
        raise HTTPException(
            status_code=404,
            detail="Meeting not found"
        )

    url = get_public_url(meeting.audio_path)

    return {
        "audio_url": url
    }