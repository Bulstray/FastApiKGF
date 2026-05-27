from core.models import (
    ParsingKeyword,
    Project,
    Task,
    User,
    Program,
    Tender,
    ArchiveTender,
    Message,
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
