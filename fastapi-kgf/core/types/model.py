from core.models import (
    ArchiveTender,
    Message,
    ParsingKeyword,
    Program,
    Project,
    Task,
    Tender,
    User,
    UserSettings,
)

Model = (
    User
    | Project
    | Task
    | ParsingKeyword
    | Program
    | Tender
    | ArchiveTender
    | Message
    | User
    | UserSettings
)
